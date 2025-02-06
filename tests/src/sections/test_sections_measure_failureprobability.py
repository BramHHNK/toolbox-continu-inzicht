import os
from pathlib import Path

import pandas as pd

from toolbox_continu_inzicht.base.config import Config
from toolbox_continu_inzicht.base.data_adapter import DataAdapter
from toolbox_continu_inzicht.sections import SectionsMeasureFailureprobability


def create_data_adapter(config_file: str) -> DataAdapter:
    """
    Initialiseer een data adapter

    config:
    SectionsMeasureFailureprobability:
        MISSING_VALUE: -9999.0

    apdaters:
    in_section_fragilitycurves:
        type: csv
        path: "test_sections_measure_failureprobability_fragility_curves.csv"

    in_section_load:
        type: csv
        path: "test_sections_measure_failureprobability_load.csv"

    out_measure_failureprobability:
        type: csv
        path: "hidden_sections_measure_failureprobability.csv"

    Args:
        config_file (str): configuratie file

    Returns:
        DataAdapter: data adapter
    """

    test_data_sets_path = Path(__file__).parent / "data_sets"
    config = Config(config_path=test_data_sets_path / config_file)
    config.lees_config()

    return DataAdapter(config=config)


def get_output_file(data_adapter: DataAdapter, section_key: str) -> Path:
    # Bepaal uitvoerbestand
    output_info = data_adapter.config.data_adapters
    return Path(
        data_adapter.config.global_variables["rootdir"]
        / Path(output_info[section_key]["path"])
    )


def test_valid_run():
    """
    Test of een valide invoer een normaal uitkomst geeft.
    """

    # Aanmaken adapter
    data_adapter = create_data_adapter(
        "test_sections_measure_failureprobability_config.yaml"
    )

    # Bepaal uitvoerbestand
    output_file = get_output_file(data_adapter, "out_measure_failureprobability")

    # Oude gegevens verwijderen
    if os.path.exists(output_file):
        os.remove(output_file)

    # Initialiseer SectionsMeasureFailureprobability functie
    sections_failureprobability = SectionsMeasureFailureprobability(
        data_adapter=data_adapter
    )

    # normale invoerbestanden
    sections_failureprobability.run(
        input=["in_section_fragilitycurves", "in_section_load"],
        output="out_measure_failureprobability",
    )

    assert os.path.exists(output_file)
    df_output = pd.read_csv(output_file)

    assert df_output is not None
    assert len(df_output) == 4
