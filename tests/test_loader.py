from src.loader import Load_Streaming_History_Data, InvalidStreamingHistoryError
import pytest
from pathlib import Path

RESOURCES = Path(__file__).parent / "resources"     # Dynamically get the path to the resources folder relative to this test file

def test_loads_valid_json():
    #Test that a valid JSON file is loaded correctly into a DataFrame
    with open(RESOURCES / "valid_history_0.json", "rb") as file:
        df = Load_Streaming_History_Data([file])
        assert not df.empty
        assert all(col in df.columns for col in ["endTime", "artistName", "trackName", "msPlayed"])

def test_raises_error_on_invalid_json():
    with open(RESOURCES / "corrupted.json", "rb") as file:
        with pytest.raises(InvalidStreamingHistoryError):
            Load_Streaming_History_Data([file])

def test_raises_error_on_empty_json():
    with open(RESOURCES / "empty_list.json", "rb") as file:
        with pytest.raises(InvalidStreamingHistoryError):
            Load_Streaming_History_Data([file])

def test_raises_error_on_missing_columns():
    with open(RESOURCES / "missing_columns.json", "rb") as file:
        with pytest.raises(InvalidStreamingHistoryError):
            Load_Streaming_History_Data([file])

def test_raises_error_on_non_json_file():
    with open(RESOURCES / "valid_history.csv", "rb") as file:
        with pytest.raises(InvalidStreamingHistoryError):
            Load_Streaming_History_Data([file])

def test_raises_error_on_not_a_list():
    with open(RESOURCES / "not_a_list.json", "rb") as file:
        with pytest.raises(InvalidStreamingHistoryError):
            Load_Streaming_History_Data([file])

def test_loads_two_valid_json():
    with open(RESOURCES / "valid_history_0.json", "rb") as file1:
        with open(RESOURCES / "valid_history_1.json", "rb") as file2:
            df = Load_Streaming_History_Data([file1, file2])
            assert not df.empty
            assert all(col in df.columns for col in ["endTime", "artistName", "trackName", "msPlayed"])

def test_raises_error_on_one_valid_one_invalid_json():
    with open(RESOURCES / "valid_history_0.json", "rb") as file1:
        with open(RESOURCES / "corrupted.json", "rb") as file2:
            with pytest.raises(InvalidStreamingHistoryError):
                Load_Streaming_History_Data([file1, file2])