import numpy as np
import pandas as pd

from scipy.stats import lognorm

# TODO: shorten imports to be more user friendly
import pydra_core
import pydra_core.location
from pydra_core.location.model.statistics.stochastics.model_uncertainty import (
    ModelUncertainty,
    DistributionUncertainty,
)
from toolbox_continu_inzicht.fragility_curves.fragility_curve_overtopping.pydra_legacy import (
    bretschneider,
    get_qcr_dist,
)


class WaveOvertoppingCalculation:
    """
    Variant op de Pydra berekening die gebruikt wordt om on-the-fly
    fragility curves te berekenen voor Continu inzicht rivierenland
    """

    def __init__(self, profile, options):
        self.profile: pydra_core.Profile = profile
        # Stel standaardonzekerheden voor bretschneider in
        standaard_model_onzekerheden = {}
        # gh =  golf hoogte onzerherheid mu/sigma/aantal;

        standaard_model_onzekerheden["gh_onz_mu"] = 0.96
        standaard_model_onzekerheden["gh_onz_sigma"] = 0.27

        standaard_model_onzekerheden["gp_onz_mu_tp"] = 1.03
        standaard_model_onzekerheden["gp_onz_sigma_tp"] = 0.13

        standaard_model_onzekerheden["gp_onz_mu_tspec"] = 1.03
        standaard_model_onzekerheden["gp_onz_sigma_tspec"] = 0.13

        standaard_model_onzekerheden["gh_onz_aantal"] = 7
        standaard_model_onzekerheden["gp_onz_aantal"] = 7

        standaard_model_onzekerheden["closing_situation"] = profile.closing_situation

        # overwrite default values with user input
        for onzekerheid in standaard_model_onzekerheden:
            if onzekerheid in options:
                standaard_model_onzekerheden[onzekerheid] = options[onzekerheid]

        self.modelonzekerheid: CustomModelUncertainty = CustomModelUncertainty(
            standaard_model_onzekerheden
        )
        # TODO: verwijder DEBUG properties
        self.qov = []
        self.kansen = []

    @classmethod
    def calculate_overtopping_curve(
        cls,
        windspeed,
        sectormin,
        sectorsize,
        overtopping,
        basis_profiel,
        qcr,
        richtingen,
        bodemhoogte,
        strijklengte,
        closing_situation,
        options,
    ):
        # Pas profiel aan voor maatregel (via kruinhoogte)
        overtopping.closing_situation = (
            closing_situation  # niet zo netjes maar het werkt
        )
        # Berekening
        berekening = cls(overtopping, options)

        # Bereken fragility curve
        windrichtingen = (
            np.linspace(sectormin, sectormin + sectorsize, int(round(sectorsize))) % 360
        )
        bedlevel = np.interp(windrichtingen, richtingen, bodemhoogte, period=360)
        fetch = np.interp(windrichtingen, richtingen, strijklengte, period=360)

        # Voor dominante windrichting bepalen gebruik(te)/(en) we het profiel zonder voorland
        basis_profiel.closing_situation = (
            closing_situation  # niet zo netjes maar het werkt
        )
        # Maak een berekening object met het basis profiel aan (WaveOvertoppingCalculation)
        berekening_basis = cls(basis_profiel, options)
        t_tspec = 1.1
        if "tp_tspec" in options:
            t_tspec = options["tp_tspec"]

        # Bepaal dominante windrichting
        ir = berekening_basis.bepaal_dominante_richting(
            overtopping.dike_crest_level - 0.5,
            windspeed,
            windrichtingen,
            bedlevel,
            fetch,
            t_tspec,
        )
        # Calculate fragility curve
        niveaus, ovkansqcr = berekening.bereken_fc_cond(
            richting=windrichtingen[ir],
            windsnelheid=windspeed,
            bedlevel=bedlevel[ir],
            fetch=fetch[ir],
            qcr=qcr,
            crestlevel=overtopping.dike_crest_level,
            closing_situation=closing_situation,
            t_tspec=t_tspec,
            options=options,
        )

        return niveaus, ovkansqcr

    def bepaal_dominante_richting(
        self, level, windspeed, richtingen, bedlevels, fetches, t_tspec
    ):
        # Bereken golfcondities met Bretschneider
        hss, tps = bretschneider(
            d=level - bedlevels, fe=fetches, u=np.ones_like(bedlevels) * windspeed
        )
        # bereken overslagdebieten
        qov = []
        for r, hs, tp in zip(richtingen, hss, tps):
            qov.append(
                self.profile.calculate_overtopping(
                    water_level=level,
                    significant_wave_height=hs,
                    spectral_wave_period=tp / t_tspec,
                    wave_direction=r,
                )
            )

        return np.argmax(qov)

    def bereken_fc_cond(
        self,
        richting,
        windsnelheid,
        bedlevel,
        fetch,
        qcr,
        t_tspec,
        crestlevel,
        closing_situation,
        options,
    ):
        # TODO: configurabele defaults?
        # Set default values
        hstap = options.get("hstap", 0.05)
        lower_limit_coarse = options.get("lower_limit_coarse", 4)
        upper_limit_coarse = options.get("upper_limit_coarse", 2)
        upper_limit_fine = options.get("upper_limit_fine", 1.01)
        # Leidt golfcondities af voor de richting
        cl_rnd = np.round(crestlevel / hstap) * hstap  # crest level rounded
        # refine grid around crest level
        waterlevels = np.r_[
            np.arange(
                cl_rnd - lower_limit_coarse, cl_rnd - upper_limit_coarse, hstap * 2
            ),
            np.arange(cl_rnd - upper_limit_coarse, cl_rnd + upper_limit_fine, hstap),
        ][:, None]

        # Bereken de golfhoogte en piekgolfperiode met Bretschneider
        hs_dw, tp_dw = bretschneider(
            d=waterlevels - bedlevel,
            fe=np.ones_like(waterlevels) * fetch,
            u=np.ones_like(waterlevels) * windsnelheid,
        )
        tspec_dw = tp_dw / t_tspec
        richting = np.ones_like(waterlevels) * richting

        # Alloceer lege array om kansen aan toe te kennen
        ovkansqcr = np.zeros(len(waterlevels))

        prob_qcr = not isinstance(qcr, int | float | np.integer)

        # Voor elke combinatie van modelonzekerheid
        for (
            factor_hs,
            factor_tspec,
            onzkans,
        ) in self.modelonzekerheid.iterate_model_uncertainty_wave_conditions(
            closing_situation=closing_situation
        ):
            self.kansen.append((factor_hs, factor_tspec, onzkans))
            hs, tspec = (
                hs_dw * factor_hs,
                tspec_dw * factor_tspec,
            )
            qov = self.profile.calculate_overtopping(
                water_level=waterlevels.flatten(),
                significant_wave_height=hs.flatten(),
                spectral_wave_period=tspec.flatten(),
                wave_direction=richting.flatten(),
                tp_tspec=t_tspec,
                dll_settings=None,
            )
            self.qov.append(np.array(qov) * 1000)
            # Als overslagdebiet probabilistisch
            if prob_qcr:
                qov = np.array(qov) * 1000
                # Bepaal per overslagdebiet de faalkans
                hs_1d = hs.ravel()
                for lower, upper in zip([0.0, 1.0, 2.0], [1.0, 2.0, np.inf]):
                    idx = (hs_1d >= lower) & (hs_1d < upper) & (qov > 0.0)
                    if not idx.any():
                        continue

                    mu, sigma = get_qcr_dist(lower + 0.5, qcr)
                    ovkansqcr[idx] += (
                        lognorm._cdf(qov[idx] / np.exp(mu), sigma) * onzkans
                    )

            # Als deterministisch
            else:
                ovkansqcr[np.array(qov) > qcr] += onzkans
        return waterlevels.squeeze(), ovkansqcr


class CustomModelUncertainty(ModelUncertainty):
    """
    Custom version of the original Model uncertainties class. Containing all model uncertainties for each closing situation.
    The original class leans heavily on database interactions, which we avoid here

    Attributes
    ----------
    model_uncertainties : dict
        A dictionary with
    """

    model_uncertainties = {}
    correlations = {}

    def __init__(self, standaard_model_onzekerheden):
        self.step_size = {
            "hs": standaard_model_onzekerheden["gh_onz_aantal"],
            "tspec": standaard_model_onzekerheden["gp_onz_aantal"],
        }

        mu = pd.DataFrame(columns=["k", "rvid", "mean", "stdev"])
        mu.loc[0, "k"] = standaard_model_onzekerheden["closing_situation"]
        mu.loc[0, "rvid"] = "hs"
        mu.loc[0, "mean"] = standaard_model_onzekerheden["gh_onz_mu"]
        mu.loc[0, "stdev"] = standaard_model_onzekerheden["gh_onz_sigma"]

        mu.loc[1, "k"] = standaard_model_onzekerheden["closing_situation"]
        mu.loc[1, "rvid"] = "tp"
        mu.loc[1, "mean"] = standaard_model_onzekerheden["gp_onz_mu_tp"]
        mu.loc[1, "stdev"] = standaard_model_onzekerheden["gp_onz_sigma_tp"]

        mu.loc[2, "k"] = standaard_model_onzekerheden["closing_situation"]
        mu.loc[2, "rvid"] = "tspec"
        mu.loc[2, "mean"] = standaard_model_onzekerheden["gp_onz_mu_tspec"]
        mu.loc[2, "stdev"] = standaard_model_onzekerheden["gp_onz_sigma_tspec"]

        # ensure the index is same for all points to match original implementation
        mu.index = [0, 0, 0]
        mu.index.name = "HRDLocationId"

        for comb, uncertainty in mu.groupby(["k", "rvid"]):
            self.model_uncertainties[comb] = DistributionUncertainty(
                uncertainty.to_numpy()[0]
            )
