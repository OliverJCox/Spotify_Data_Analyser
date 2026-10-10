import pandas as pd
import src.cleaner as cleaner
import src.loader as loader
import pytest
from pathlib import Path

RESOURCES = Path(__file__).parent / "resources"     # Dynamically get the path to the resources folder relative to this test file

def test_cleaning_bad_date(): # Should remove one invalid date, making length of each column 3
    with open(RESOURCES / "cleaning_bad_date.json", "rb") as file:
        df = loader.Load_Streaming_History_Data([file])
        clean_df = cleaner.Clean(df)
        assert not df.empty
        assert len(clean_df['artist']) == 3 

def test_null_track_and_artist():
    # Should remove one null artist and one null track, making length of each column 2
    with open(RESOURCES / "cleaning_null_track_artist.json", "rb") as file:
        df = loader.Load_Streaming_History_Data([file])
        clean_df = cleaner.Clean(df)
        assert not df.empty
        assert len(clean_df['artist']) == 2

def test_cleaning_null_msPlayed():
    with open(RESOURCES / "cleaning_null_ms_played.json", "rb") as file:
            df = loader.Load_Streaming_History_Data([file])
            clean_df = cleaner.Clean(df)
            assert not df.empty
            assert len(clean_df['artist']) == 2

def test_cleaning_non_numeric_msPlayed():
    with open(RESOURCES / "cleaning_non_numeric_ms_played.json", "rb") as file:
            df = loader.Load_Streaming_History_Data([file])
            clean_df = cleaner.Clean(df)
            assert not df.empty
            assert len(clean_df['artist']) == 1

def test_cleaning_duplicates():
     with open(RESOURCES / "cleaning_duplicates.json", "rb") as file:
        df = loader.Load_Streaming_History_Data([file])
        clean_df = cleaner.Clean(df)
        assert not df.empty
        assert len(clean_df['artist']) == 4

def test_cleaning_extra_null_column():
        with open(RESOURCES / "cleaning_extra_null_column.json", "rb") as file:
            df = loader.Load_Streaming_History_Data([file])
            clean_df = cleaner.Clean(df)
            assert not df.empty
            assert len(clean_df.columns) == 4

def test_cleaning_all_invalid():
    with open(RESOURCES / "cleaning_all_invalid.json", "rb") as file:
        df = loader.Load_Streaming_History_Data([file])
        with pytest.raises(cleaner.CleaningError):
             cleaner.Clean(df)

def test_cleaning_unsorted():
     with open(RESOURCES / "cleaning_unsorted.json", "rb") as file:
          df = loader.Load_Streaming_History_Data([file])
          df = cleaner.Clean(df)
          assert not df.empty
          assert df['ended_at'].is_monotonic_increasing
