import pandas as pd

'''Artists are ranked based on the number of minutes they have been played for.
Tracks are ranked on the number of times they have been listened to, the
minimum duration for a play to count can be set by user by delfult all plays including
instant skips are counted. If there are equals for minutes played (atrists) or times played
(tracks) then values will be sorted in deccending order.

Find_Top_Artists() - This function is responsible for returning the top artists from the dataframe
passed to it. The number of items to show can be set by the parameter: number - which 
defaults to 10.
Find_Top_Tracks() - Returns the most played tracks in the dataframe. The number to return can be
passed through the parameter: number - which defaults to 10.
Find_Mins_Played() - Returns the total number of minutes played for the dataframe passed to it.
Track_Play_Count() - Returns the number of tracks played in the dataframe that is passed to it, 
repeats of tracks are counted as new plays.'''



def Find_Top_Artists(df: pd.DataFrame, number: int = 10) -> pd.DataFrame:
    return (df.groupby('artist')['minutes'].sum()
            .sort_values(ascending=False)
            .head(number).reset_index())

def Find_Top_Tracks(df: pd.DataFrame, number: int = 10) -> pd.DataFrame:
    return (df.groupby(['track','artist']).size()
            .sort_values(ascending=False)
            .head(number).reset_index(name = 'plays'))

def Find_Mins_Played(df: pd.DataFrame) -> float:
    return float(df['minutes'].sum())

def Track_Play_Count(df: pd.DataFrame) -> int:
    return len(df)