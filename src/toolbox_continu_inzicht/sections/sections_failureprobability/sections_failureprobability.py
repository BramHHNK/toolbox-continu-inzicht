"""
Bepaal de faalkans van een dijkvak
"""

from pydantic.dataclasses import dataclass
from toolbox_continu_inzicht.base.data_adapter import DataAdapter
from typing import Optional

import pandas as pd


@dataclass(config={"arbitrary_types_allowed": True})
class SectionsFailureprobability:
    """
    Bepaal de faalkans van een dijkvak

    ## Input schema's
    **input_schema_failureprobability (DataFrame): schema voor de lijst met dijkvakken\n
    - section_id: int64                 : id van de dijkvak
    - failuremechanism_id: int64        : id van het faalmechanisme
    - value_parameter_id: int64         : id van de belastingparameter (1,2,3,4)
    - parameter_id: int64               : id van de faalkans parameter (5,100,101,102)
    - date_time: datetime64[ns, UTC]    : datum/ tijd van de tijdreeksitem
    - value: float64                    : belasting van de tijdreeksitem

    ## Output schema
    **df_out (DataFrame): uitvoer\n
    - section_id: int64                 : id van het dijkvak
    - failuremechanism_id: int64        : id van het faalmechanisme
    - value_parameter_id: int64         : id van de belastingparameter (1,2,3,4)
    - parameter_id: int64               : id van de faalkans parameter (5,100,101,102)
    - date_time: datetime64[ns, UTC]    : datum/ tijd van de tijdreeksitem
    - failureprobability: float64       : faalkans van de tijdreeksitem
    """

    data_adapter: DataAdapter

    df_in_failureprobability: Optional[pd.DataFrame] | None = None
    """DataFrame: lijst met faalkansen op een dijkvak voor verschillende faalmechanisms en maatregelen."""

    df_out: Optional[pd.DataFrame] | None = None
    """DataFrame: uitvoer."""

    # faalkans per moment per dijkvak
    input_schema_failureprobability = {
        "section_id": "int64",
        "failuremechanism_id": "int64",
        "value_parameter_id": "int64",
        "parameter_id": "int64",
        "date_time": "datetime64[ns, UTC]",
        "value": "float64",
    }

    def run(self, input: str, output: str) -> None:
        """
        Bepaal de faalkans van een dijkvak.

        Args: \n
            input  (str): faalkans per dijkvak, faalmechanisms en maatregel
            output (str): maatgevende faalkans per dijkvak
        """

        # invoer: faalskans per dijkvak
        self.df_in_failureprobability = self.data_adapter.input(
            input, self.input_schema_failureprobability
        )

        # uitvoer: belasting per dijkvak
        self.df_out = pd.DataFrame()

        df = self.df_in_failureprobability.copy()
        df = df[
            [
                "section_id",
                "failuremechanism_id",
                "value_parameter_id",
                "parameter_id",
                "date_time",
                "value",
            ]
        ].reset_index(drop=True)
        df = df.loc[
            df.groupby(
                ["section_id", "failuremechanism_id", "value_parameter_id", "date_time"]
            )["parameter_id"].idxmax()
        ]
        df = df.assign(measureid=0)

        self.df_out = df[
            [
                "section_id",
                "failuremechanism_id",
                "parameter_id",
                "value_parameter_id",
                "date_time",
                "value",
            ]
        ].reset_index(drop=True)
        self.df_out = self.df_out.rename(columns={"value": "failureprobability"})

        self.data_adapter.output(output=output, df=self.df_out)
