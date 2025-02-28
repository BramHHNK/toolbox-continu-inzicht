import pandas as pd
from pydantic.dataclasses import dataclass
from typing import Optional
from pathlib import Path

from probabilistic_piping import (
    ProbInput,
    ProbPipingFixedWaterlevelSimple,
)
from toolbox_continu_inzicht import FragilityCurve, DataAdapter, Config


# TODO: pas dit aan naar FragilityCurvePipingFixedWaterlevelSimplePerSection, en maak FragilityCurvePipingFixedWaterlevelSimple standaard voor meerdere secties
# (net als bij  calculate_combined_curve)
@dataclass(config={"arbitrary_types_allowed": True})
class FragilityCurvePipingFixedWaterlevelSimple(FragilityCurve):
    """
    Maakt een enkele fragility curve voor piping met een gegeven waterstand.

    De fragility curve wordt berekend met behulp van de probabilistic_piping package, zie de eigen documentatie voor meer informatie.
    Deze functie berekent fragility curves voor uplift, heave, Sellmeijer, en de gecombineerde mechanismes.
    Voor het combineren van de mechanismes wordt het minimum van de kansen van de drie sub-mechanismes genomen,
    De gecombineerde fragility curve is de standaard output, de andere kunnen worden opgevraagd met de df_result_uplift, df_result_heave, en df_result_sellmeijer attributen.

    Args:
        data_adapter (DataAdapter): DataAdapter object


    Options in config
    ------------------
    progress: bool
        Standaard is False

    debug: bool
        Standaard is False
    """

    data_adapter: DataAdapter
    df_prob_input: Optional[pd.DataFrame] | None = None
    df_waterlevels: Optional[pd.DataFrame] | None = None
    df_out: Optional[pd.DataFrame] | None = None

    df_result_uplift: Optional[pd.DataFrame] | None = None
    df_result_heave: Optional[pd.DataFrame] | None = None
    df_result_sellmeijer: Optional[pd.DataFrame] | None = None
    df_result_combined: Optional[pd.DataFrame] | None = None

    def run(self, input: list[str], output: str) -> None:
        """
        Runt de berekening van de fragility curve voor piping

        Parameters
        ----------
        input: list[str]
               [0] df_prob_input (pd.DataFrame),
               [1] df_waterlevels (pd.DataFrame),

        output: str
            Fragility curve (pd.DataFrame)

        Notes
        ------
        input: list[str]

               [0] df_prob_input (pd.DataFrame)

                    DataFrame met data voor de probabilistische berekening.
                    De benodigde kolommen zijn afhankelijk van de probabilistische berekening.
                    Zie de documentatie van probabilistic_piping.probabilistic_fixedwl.ProbPipingFixedWaterlevelSimple voor meer informatie.


               [1] df_waterlevels (pd.DataFrame):
                    DataFrame met waterlevel data.
                    Moet de volgende kolommen bevatten:
                    - waterlevels : float

        """
        self.calculate_fragility_curve(input, output)

    def calculate_fragility_curve(self, input: list[str], output: str) -> None:
        """
        Berekent de fragility curve op basis van de opgegeven input en slaat het resultaat op in het opgegeven outputbestand.
        """
        self.df_prob_input = self.data_adapter.input(input[0])
        self.df_waterlevels = self.data_adapter.input(input[1])

        # sommige opties niet direct nodig maar de probabilistic_piping package heeft ze wel nodig dus maak None
        for col in ["Afknot_links", "Afknot_rechts"]:
            if col not in self.df_prob_input.columns:
                self.df_prob_input[col] = None

        global_variables = self.data_adapter.config.global_variables
        progress: bool = False
        debug: bool = False
        if "FragilityCurvePipingFixedWaterlevelSimple" in global_variables:
            # neem opties over van de config
            options: dict = global_variables[
                "FragilityCurvePipingFixedWaterlevelSimple"
            ]

            if "progress" in options:
                progress: bool = options["progress"]

            if "debug" in options:
                debug: bool = options["debug"]

        prob_input = ProbInput().from_dataframe(self.df_prob_input)
        prob_piping_fixed_waterlevel_simple = ProbPipingFixedWaterlevelSimple(
            progress=progress,
            debug=debug,
        )
        settings, result_uplift, result_heave, result_Sellmeijer, result_combined = (
            prob_piping_fixed_waterlevel_simple.fixed_waterlevel_fragilitycurve(
                prob_input=prob_input,
                hlist=self.df_waterlevels["waterlevels"].to_numpy(),
            )
        )

        # zet de resultaten om in DataFrames voor elk mechanisme
        df_names = [
            "df_result_uplift",
            "df_result_heave",
            "df_result_sellmeijer",
            "df_result_combined",
        ]
        for name, result in zip(
            df_names, [result_uplift, result_heave, result_Sellmeijer, result_combined]
        ):
            self.__setattr__(
                name,
                pd.DataFrame(
                    data=[(res.h, res.prob_cond) for res in result.results],
                    columns=["waterlevels", "failure_probability"],
                ),
            )
        self.df_out = self.df_result_combined
        self.data_adapter.output(output, self.df_out)


##### Unused for now, but might be useful in the future #####
# @dataclass(config={"arbitrary_types_allowed": True})
# class FragilityCurvePipingFixedWaterlevel(FragilityCurve):
#     """
#     Maakt één fragility curve voor piping met een gegeven waterstand.
#     De fragility curve wordt berekend met behulp van de probabilistic_piping package.
#     Deze functie berekent fragility curves voor één mechanisme, standaard is dit sellmeijer.
#     Het mechanisme kan worden aangepast met de z_type parameter in de config.
#     Het combineren van de mechanismes gebruikt hier een andere methode dan de simple versie,
#     hier wordt de het minimum van de drie sub-mechanismes genomen in de grenstoestand functie.

#     Args:
#         data_adapter (DataAdapter): DataAdapter object

#     Options in config
#     ------------------
#     z_type: str
#         'sellmeijer', 'heave', 'uplift' of 'combi'
#         Standaard is 'combi'

#     progress: bool
#         Standaard is False

#     debug: bool
#         Standaard is False
#     """

#     data_adapter: DataAdapter
#     df_prob_input: Optional[pd.DataFrame] | None = None
#     df_waterlevels: Optional[pd.DataFrame] | None = None
#     df_out: Optional[pd.DataFrame] | None = None

#     # TODO: add, first think about what to do with ids
#     # input_prob_input = {
#     #  ...
#     # }

#     # input_waterlevels = {
#     #  ...
#     # }

#     def run(self, input: list[str], output: str) -> None:
#         """
#         Runt de berekening van de fragility curve voor piping

#         Parameters
#         ----------
#         input: list[str]
#                [0] df_prob_input (pd.DataFrame),
#                [1] df_waterlevels (pd.DataFrame),

#         output: str
#             Fragility curve (pd.DataFrame)

#         Notes
#         ------
#         input: list[str]

#                [0] df_prob_input (pd.DataFrame)

#                     DataFrame met data voor de probabilistische berekening.
#                     De benodigd kolommen zijn afhankelijk van de probabilistische berekening.
#                     Zie de documentatie van probabilistic_piping.probabilistic_fixedwl.ProbPipingFixedWaterlevel voor meer informatie.


#                [1] df_waterlevels (pd.DataFrame):
#                     DataFrame met waterlevel data.
#                     Moet de volgende kolommen bevatten:
#                     - waterlevels : float

#         """
#         self.calculate_fragility_curve(input, output)

#     def calculate_fragility_curve(self, input: list[str], output: str) -> None:
#         """
#         Bereken de fragiliteitscurve op basis van de opgegeven input en sla het resultaat op in het opgegeven outputbestand.
#         """
#         self.df_prob_input = self.data_adapter.input(input[0])
#         self.df_waterlevels = self.data_adapter.input(input[1])

#         # sommige opties niet nodig maar kan wel gaan zeuren dus maak None
#         for col in ["Afknot_links", "Afknot_rechts", "Min", "Step", "Max"]:
#             if col not in self.df_prob_input.columns:
#                 self.df_prob_input[col] = None

#         global_variables = self.data_adapter.config.global_variables
#         z_type = "combi"  # by default
#         progress: bool = False
#         debug: bool = False
#         if "FragilityCurvePipingFixedWaterlevel" in global_variables:
#             # can be used to set options for the calculation
#             options: dict = global_variables["FragilityCurvePipingFixedWaterlevel"]

#             if "z_type" in options:
#                 z_type = options["z_type"]

#             if "progress" in options:
#                 progress = options["progress"]

#             if "debug" in options:
#                 debug = options["debug"]

#         prob_input = ProbInput().from_dataframe(self.df_prob_input)
#         prob_piping_fixed_waterlevel = ProbPipingFixedWaterlevel(
#             progress=progress,
#             debug=debug,
#         )

#         settings, result = prob_piping_fixed_waterlevel.fixed_waterlevel_fragilitycurve(
#             prob_input=prob_input,
#             hlist=self.df_waterlevels["waterlevels"].to_numpy(),
#             z_type=z_type,
#         )

#         self.df_out = pd.DataFrame(
#             data=[(res.h, res.prob_cond) for res in result.results],
#             columns=["waterlevels", "failure_probability"],
#         )
#         self.data_adapter.output(output, self.df_out)


# Dit is nu nog heel traag: in de toekomst kijken of we dit met cache kunnen versnellen?
@dataclass(config={"arbitrary_types_allowed": True})
class FragilityCurvesPiping:
    """
    Maakt een set van fragility curves voor piping voor een dijkvak.
    De fragility curve wordt berekend met behulp van de probabilistic_piping package, zie de eigen documentatie voor meer informatie.

    Deze functie berekent één gecombineerde fragility curve voor de mechanismes uplift, heave en Sellmeijer.

    Args:
        data_adapter (DataAdapter): DataAdapter object

    """

    data_adapter: DataAdapter

    df_prob_input: Optional[pd.DataFrame] | None = None
    df_waterlevels: Optional[pd.DataFrame] | None = None
    df_out: Optional[pd.DataFrame] | None = None

    fragility_curve_function_simple: FragilityCurve = (
        FragilityCurvePipingFixedWaterlevelSimple
    )

    def run(self, input: list[str], output: str) -> None:
        """
        Runt de berekening van de fragility curves voor piping

        Parameters
        ----------
        input: list[str]
               [0] df_prob_input (pd.DataFrame),
               [1] df_waterlevels (pd.DataFrame),

        output: str
            Fragility curves (pd.DataFrame)

        Notes
        ------
        input: list[str]

               [0] df_prob_input (pd.DataFrame)

                    DataFrame met data voor de probabilistische berekening.
                    De benodigde kolommen zijn afhankelijk van de probabilistische berekening.
                    Zie de documentatie van probabilistic_piping.probabilistic_fixedwl.ProbPipingFixedWaterlevel voor meer informatie.


               [1] df_waterlevels (pd.DataFrame):
                    DataFrame met waterlevel data.
                    Moet de volgende kolommen bevatten:
                    - waterlevels : float

        """
        self.df_prob_input = self.data_adapter.input(input[0])
        self.df_waterlevels = self.data_adapter.input(input[1])

        global_variables = self.data_adapter.config.global_variables
        if "FragilityCurvesPiping" in global_variables:
            options = global_variables["FragilityCurvesPiping"]

        self.df_out = pd.DataFrame(
            columns=[
                "section_id",
                "scenario_id",
                "waterlevel",
                "failure_probability",
            ]
        )
        # loop over alle secties
        for section_id in self.df_prob_input.section_id.unique():
            df_prob_section = self.df_prob_input[
                self.df_prob_input.section_id == section_id
            ]
            # loop over alle scenario's in de sectie
            for scenario_id in df_prob_section.scenario_id.unique():
                df_prob_scenario = df_prob_section[
                    df_prob_section.scenario_id == scenario_id
                ].copy()
                # loop over alle mechanismes
                df_prob_scenario.set_index("Naam", inplace=True)
                df_prob_scenario.drop(
                    columns=["section_id", "scenario_id", "mechanism"], inplace=True
                )

                # maak een placeholder DataAdapter aan, dit zorgt dat je de modules ook los kan aanroepen
                temp_config = Config(config_path=Path.cwd())
                temp_data_adapter = DataAdapter(config=temp_config)

                temp_data_adapter.set_dataframe_adapter(
                    "df_prob", df_prob_scenario, if_not_exist="create"
                )
                temp_data_adapter.set_dataframe_adapter(
                    "waterlevels", self.df_waterlevels, if_not_exist="create"
                )
                temp_data_adapter.set_dataframe_adapter(
                    "output", pd.DataFrame(), if_not_exist="create"
                )

                temp_data_adapter.config.global_variables[
                    "FragilityCurvePipingFixedWaterlevelSimple"
                ] = update_options_dict_debug_progress(options)

                fragility_curve = self.fragility_curve_function_simple(
                    data_adapter=temp_data_adapter
                )

                fragility_curve.run(input=["df_prob", "waterlevels"], output="output")
                df_fc = fragility_curve.df_out
                df_fc["section_id"] = section_id
                df_fc["scenario_id"] = scenario_id
                if len(self.df_out) == 0:
                    self.df_out = df_fc
                else:
                    self.df_out = pd.concat([self.df_out, df_fc])

        self.df_out.reset_index(drop=True, inplace=True)
        self.data_adapter.output(output, self.df_out)


def update_options_dict_debug_progress(options):
    new_options = {}
    for key in ["progress", "debug"]:
        if key in options:
            new_options[key] = options[key]
    return new_options
