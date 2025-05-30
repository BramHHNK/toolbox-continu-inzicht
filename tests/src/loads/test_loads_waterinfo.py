import os
import pandas as pd

from pathlib import Path
from toolbox_continu_inzicht.base.config import Config
from toolbox_continu_inzicht.base.data_adapter import DataAdapter
from toolbox_continu_inzicht.loads import LoadsWaterinfo


def test_run():
    test_data_sets_path = Path(__file__).parent / "data_sets"
    config = Config(
        config_path=test_data_sets_path / "test_loads_waterinfo_config.yaml"
    )
    config.lees_config()

    data_adapter = DataAdapter(config=config)

    # Oude gegevens verwijderen
    output_info = config.data_adapters
    output_file = Path(
        config.global_variables["rootdir"] / Path(output_info["waterstanden"]["path"])
    )
    if os.path.exists(output_file):
        os.remove(output_file)

    waterinfo = LoadsWaterinfo(data_adapter=data_adapter)
    waterinfo.run(input="locaties", output="waterstanden")

    assert os.path.exists(output_file)

    assert waterinfo.df_out is not None
    assert len(waterinfo.df_out) > 0


def test_run_luchttemperatuur():
    test_data_sets_path = Path(__file__).parent / "data_sets"
    config = Config(
        config_path=test_data_sets_path
        / "test_loads_waterinfo_config_luchttemperatuur.yaml"
    )
    config.lees_config()

    data_adapter = DataAdapter(config=config)

    # Oude gegevens verwijderen
    output_info = config.data_adapters
    output_file = Path(
        config.global_variables["rootdir"] / Path(output_info["waterstanden"]["path"])
    )
    if os.path.exists(output_file):
        os.remove(output_file)

    waterinfo = LoadsWaterinfo(data_adapter=data_adapter)
    waterinfo.run(input="locaties", output="waterstanden")

    assert os.path.exists(output_file)

    assert waterinfo.df_out is not None
    assert len(waterinfo.df_out) > 0


def test_create_dataframe():
    test_data_sets_path = Path(__file__).parent / "data_sets"
    config = Config(config_path=test_data_sets_path / "test_loads_fews_config.yaml")
    config.lees_config()

    data_adapter = DataAdapter(config=config)
    waterinfo = LoadsWaterinfo(data_adapter=data_adapter)

    options = {
        "datatype": "waterhoogte",
        "observedhours": 48,
        "predictionhours": 48,
        "momentsupdate": True,
        "MISSING_VALUE": -9999.0,
        "moments": [-24, 0, 24, 48],
    }

    measuringstations = pd.DataFrame.from_dict(
        {
            "measurement_location_id": 1,
            "measurement_location_description": "Rottedamse hoek",
            "measurement_location_code": "Rotterdamse-hoek(FL02)-1",
        },
        orient="index",
    )

    json_data = {
        "t0": "2024-10-21T07:50:00Z",
        "offsetText": None,
        "series": [
            {
                "unit": "cm",
                "color": "#0178ca",
                "isDirection": False,
                "isPrediction": False,
                "data": [
                    {"dateTime": "2024-10-19T08:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T08:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T08:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T08:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T09:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T10:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T10:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T10:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T10:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T10:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T10:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T11:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T11:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T11:20:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T11:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T11:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T11:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T12:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T12:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T12:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T12:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T12:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T12:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T13:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T13:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T13:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T13:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T13:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T13:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T14:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T14:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T14:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T14:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T14:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T14:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T15:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-19T15:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T15:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T15:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T15:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T15:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T16:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T16:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T16:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T16:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T16:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T16:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T17:50:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:00:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:20:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:30:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:40:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T18:50:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T19:00:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T19:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T19:20:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-19T19:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T19:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T19:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T20:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T20:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T20:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T20:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T20:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T20:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T21:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T21:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T21:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T21:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T21:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T21:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T22:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T22:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T22:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-19T22:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T22:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T22:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-19T23:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T00:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T00:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T00:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T00:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T00:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T00:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T01:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T02:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T03:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T03:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T03:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T03:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T03:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T03:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T04:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T05:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T05:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T05:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T05:30:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T05:40:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T05:50:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T06:00:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T06:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T06:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T06:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T06:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T06:50:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T07:00:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T07:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T07:20:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T07:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T07:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T07:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T08:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T08:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T08:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T08:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T08:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T08:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T09:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T09:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T09:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T09:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T09:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T09:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T10:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T10:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T10:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T10:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T10:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T10:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T11:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T11:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T11:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T11:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T11:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T11:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T12:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:10:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T13:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T14:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T14:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T14:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T14:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T14:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T14:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T15:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T15:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T15:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T15:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T15:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T15:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T16:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T16:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T16:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T16:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T16:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T16:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T17:00:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T17:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T17:20:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T17:30:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T17:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T17:50:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T18:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T18:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T18:20:00Z", "value": -34.0, "sign": None},
                    {"dateTime": "2024-10-20T18:30:00Z", "value": -34.0, "sign": None},
                    {"dateTime": "2024-10-20T18:40:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T18:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T19:00:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T19:10:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T19:20:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T19:30:00Z", "value": -33.0, "sign": None},
                    {"dateTime": "2024-10-20T19:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T19:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-20T20:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T20:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T20:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T20:30:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-20T20:40:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-20T20:50:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-20T21:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T21:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T21:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-20T21:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-20T21:40:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-20T21:50:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-20T22:00:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-20T22:10:00Z", "value": -25.0, "sign": None},
                    {"dateTime": "2024-10-20T22:20:00Z", "value": -24.0, "sign": None},
                    {"dateTime": "2024-10-20T22:30:00Z", "value": -24.0, "sign": None},
                    {"dateTime": "2024-10-20T22:40:00Z", "value": -25.0, "sign": None},
                    {"dateTime": "2024-10-20T22:50:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-20T23:00:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-20T23:10:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-20T23:20:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-20T23:30:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-20T23:40:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-20T23:50:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T00:00:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T00:10:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T00:20:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T00:30:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T00:40:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T00:50:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T01:00:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T01:10:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T01:20:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T01:30:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T01:40:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T01:50:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T02:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T02:10:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T02:20:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T02:30:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T02:40:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T02:50:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T03:00:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T03:10:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-21T03:20:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-21T03:30:00Z", "value": -26.0, "sign": None},
                    {"dateTime": "2024-10-21T03:40:00Z", "value": -27.0, "sign": None},
                    {"dateTime": "2024-10-21T03:50:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:00:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:10:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:20:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:30:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:40:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T04:50:00Z", "value": -28.0, "sign": None},
                    {"dateTime": "2024-10-21T05:00:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T05:10:00Z", "value": -29.0, "sign": None},
                    {"dateTime": "2024-10-21T05:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T05:30:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T05:40:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T05:50:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T06:00:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T06:10:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T06:20:00Z", "value": -30.0, "sign": None},
                    {"dateTime": "2024-10-21T06:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T06:40:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-21T06:50:00Z", "value": -32.0, "sign": None},
                    {"dateTime": "2024-10-21T07:00:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T07:10:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T07:20:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T07:30:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T07:40:00Z", "value": -31.0, "sign": None},
                    {"dateTime": "2024-10-21T07:50:00Z", "value": -32.0, "sign": None},
                ],
                "extremes": None,
                "mooncycle": None,
                "meta": {
                    "locationName": "Rotterdamse hoek",
                    "parameterName": "Waterhoogte Oppervlaktewater t.o.v. Normaal Amsterdams Peil in cm",
                    "displayName": "Waterhoogte Oppervlaktewater t.o.v. Normaal Amsterdams Peil in cm",
                },
            }
        ],
        "limits": [
            {
                "from": None,
                "to": -45.0,
                "softColor": "#F5F1F0",
                "color": "#673327",
                "label": "Verlaagd (<-45cm)",
                "isNormal": False,
            },
            {
                "from": -45.0,
                "to": -10.0,
                "softColor": "#F2F7EE",
                "color": "#39870C",
                "label": "Normaal (-30 tot -10cm)",
                "isNormal": False,
            },
            {
                "from": -10.0,
                "to": 10.0,
                "softColor": "#F7F8EE",
                "color": "#CDDC39",
                "label": "Licht verhoogd (>-10cm)",
                "isNormal": False,
            },
            {
                "from": 10.0,
                "to": 30.0,
                "softColor": "#FFFAEF",
                "color": "#FFDE12",
                "label": "Verhoogd (>10cm)",
                "isNormal": False,
            },
            {
                "from": 30.0,
                "to": 100.0,
                "softColor": "#FDF5ED",
                "color": "#E17000",
                "label": "Hoog water (>30cm)",
                "isNormal": False,
            },
            {
                "from": 100.0,
                "to": None,
                "softColor": "#FDF1F0",
                "color": "#D52B1E",
                "label": "Extreem hoog water (>100cm)",
                "isNormal": False,
            },
        ],
        "extremesY": {"min": -54.0, "max": -4.0},
        "isCombined": False,
    }

    maptype_schema = {
        "maptype": "waterhoogte",
        "parameter_id": 4724,
        "parameter_code": "WATHTE",
        "values": [
            {"observedhours": 48, "predictionhours": 48, "query": "-48,48"},
            {"observedhours": 6, "predictionhours": 3, "query": "-6,3"},
            {"observedhours": 216, "predictionhours": 48, "query": "-216,48"},
            {"observedhours": 672, "predictionhours": 0, "query": "-672,0"},
        ],
    }

    df_out = waterinfo.create_dataframe(
        options=options,
        maptype_schema=maptype_schema,
        measuringstation=measuringstations[0],
        json_data=json_data,
    )
    assert df_out is not None
    assert len(df_out) == 286
