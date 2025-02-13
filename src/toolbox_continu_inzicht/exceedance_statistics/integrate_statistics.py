import pandas as pd
from typing import Optional
from pydantic.dataclasses import dataclass
from toolbox_continu_inzicht.base.data_adapter import DataAdapter


@dataclass(config={"arbitrary_types_allowed": True})
class IntegrateStatisticsPerSection:
    """Integreert een waterniveau overschrijdingsfrequentielijn met een fragility curve"""

    data_adapter: DataAdapter
    df_exceedance_frequency: Optional[pd.DataFrame] | None = None
    df_fragility_curve: Optional[pd.DataFrame] | None = None
    df_out: Optional[pd.DataFrame] | None = None

    def run(self, input: list, output: str):
        """Runt de integratie van een waterniveau overschrijdingsfrequentielijn met een fragility curve

        Parameters
        ----------
        input: list[str]
               [0] df_exceedance_frequency (pd.DataFrame),
               [1] df_fragility_curve (pd.DataFrame),
        output: str
            output df

        Notes:
        ------
        input: list[str]

               [0] df_exceedance_frequency (pd.DataFrame)
                    DataFrame met waterstand overschrijdingsfrequentie statistiek.
                    Moet de volgende kolommen bevatten:
                    - hydraulicload : float
                    - probability_exceedance : float

               [1] df_fragility_curve (pd.DataFrame):
                    DataFrame met df_fragility_curve data.
                    Moet de volgende kolommen bevatten:
        """
        self.df_exceedance_frequency = self.data_adapter.input(input[0])
        self.df_fragility_curve = self.data_adapter.input(input[1])

        self.calculate_integration()

        self.data_adapter.output(output, self.df_out)

    @staticmethod
    def calculate_integration(df_exceedance_frequency, df_fragility_curve):
        return pd.DataFrame()


class IntegrateStatistics(IntegrateStatisticsPerSection):
    """Integreert een waterniveau overschrijdingsfrequentielijn met een fragility curve voor een heel gebied"""

    def run(self, input: list, output: str):
        self.df_exceedance_frequency = self.data_adapter.input(input[0])
        self.df_fragility_curves = self.data_adapter.input(input[1])

        self.calculate_integration()

        self.data_adapter.output(output, self.df_out)
