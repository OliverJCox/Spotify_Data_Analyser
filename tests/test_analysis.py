import pandas as pd
from src import analysis
import pytest

# Tests artists are sorted properly by total mins played, and that the artist names match time played
def test_top_artists_sorted_by_minutes():
    df = pd.DataFrame({
        "artist": ["aaa", "zzz", "zzz"],
        "minutes": [1.0, 5.0, 4.0],
    })
    result = analysis.Find_Top_Artists(df, number=2)
    assert result["artist"].tolist() == ["zzz", "aaa"]
    assert result["minutes"].tolist() == [9.0, 1.0]


def test_top_tracks_sorted_by_plays():
    '''Tests that top tracks are sorted on plays, that the function distinguishes between 
    different artists with the same track name, and that songs with the same plays are sorted
    by ascending track name order then by ascending artist name order.'''
    
    df = pd.DataFrame({
        "artist": ["ddd", "aaa", "bbb","ccc","ccc","ccc", "zzz", "zzz",],
        "track" : ["track2", "track2", "track3", "track1", "track1", "track1", "track1", "track1"],
    })
    result = analysis.Find_Top_Tracks(df, number=4)
    assert result['artist'].tolist() == ["ccc", "zzz", "aaa", "ddd"]
    assert result['track'].tolist() == ["track1", "track1", "track2", "track2"]
    assert result['plays'].tolist() == [3, 2, 1, 1]

def test_find_total_mins_played():
    df = pd.DataFrame({
        'artist': ["aaa", "bbb", "ccc", "ccc"],
        'minutes': [0.5, 3, 2.25, 4],
    })
    result = analysis.Find_Mins_Played(df)
    assert result == pytest.approx(9.75) # Using pytest.appros for good practice

def test_find_number_of_plays():
    df = pd.DataFrame({
        'artist': ["aaa", "bbb", "aaa"],
        'track': ["track1", "track2", "track1"],
    })
    result = analysis.Track_Play_Count(df)
    assert result == 3