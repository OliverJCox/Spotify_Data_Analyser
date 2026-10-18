from src.filters import Filters
import pandas as pd
from datetime import date

'''Files being used for these tests are "valid_history_0.json" and valid_history_1.json
See conftest.py for file handling.'''

def test_most_played_artist(analyser):
    df = pd.DataFrame({
            'artist': ["Test Artist A"],
            'minutes': [16.0],
    })
    assert analyser.Most_Played_Artist(filters=Filters()).equals(df)


def test_excluding_plays(analyser):
    assert analyser.Play_Count(filters=Filters(min_minutes=0.5)) == 11
    # tests Play_Count method works
            
def test_filtering_by_end_bound(analyser):
    df = analyser.Get_Data(Filters(end_bound=date(2024, 1, 5)))
    assert len(df) == 3

def test_get_data(analyser):
    assert analyser.Get_Data(Filters()).equals(analyser._df)

def test_most_played_track_for_filtered_artist(analyser):
    df = analyser.Most_Played_Track(filters=Filters(artist_names=("Test Artist A",)))
    expected = pd.DataFrame({
        'track': ["Song One"],
        'artist': ["Test Artist A"],
        'plays': [3],
    })
    assert df.equals(expected)

def test_get_data_returns_a_copy(analyser):
    # If there is no copy made and the internal dataframe is modified, the test fails
    data = analyser.Get_Data(Filters())
    data["minutes"] = 0
    assert analyser.Get_Data(Filters())["minutes"].sum() > 0

def test_filtering_by_start_bound(analyser):
    df = analyser.Get_Data(Filters(start_bound=date(2024, 1, 6)))
    assert len(df) == 9

def test_filtering_multiple_parameters(analyser):
    df = analyser.Get_Data(Filters(artist_names=("Test Artist A",), end_bound=date(2024, 1, 5)))
    assert len(df) == 2

def test_filtering_by_track(analyser):
    df = analyser.Get_Data(Filters(track_names=("Song One",)))
    assert len(df) == 3

def test_filtering_by_multiple_artists(analyser):
    filters = Filters(artist_names=("Test Artist A", "Test Artist B"))
    assert analyser.Play_Count(filters=filters) == 8

def test_filters_matching_nothing_give_empty_results(analyser):
    filters = Filters(artist_names=("Nobody",))
    assert analyser.Play_Count(filters=filters) == 0
    assert analyser.Most_Played_Artist(filters=filters).empty