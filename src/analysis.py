import pandas as pd
import datetime

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
repeats of tracks are counted as new plays.
Find_Share_Of_Listening() - Returns minutes played per artist selected, plus one row for all
other listening. Used to generate pie charts
Find_Listening_Over_Time() - Returns minutes listened per time period, one column per artist'''



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

def Find_Listening_Over_Time(df: pd.DataFrame) -> pd.DataFrame:
    """Uses days as axis label when the data spans 90 days or less, otherwise months. Periods
    with no listening are filled with 0 so charts won't skip gaps. The index
    is named "Day" or "Month" so the axis can be labeled propperly."""
    if df.empty:
        return pd.DataFrame()
    day_span = (df["ended_at"].max() - df["ended_at"].min()).days
    frequency, label = ("D", "Day") if day_span <= 90 else ("MS", "Month") 
    # Sets the correct format and axis label for the data so it can be put on chart easily
    result = (df.groupby([pd.Grouper(key="ended_at", freq=frequency), "artist"])["minutes"]
             .sum().unstack(fill_value=0))
    # Extracts and groups the data to have artist names as columns and 
    result = result.reindex(pd.date_range
        (result.index.min(), result.index.max(), freq=frequency), fill_value=0)
    # Fills in any NaN cells values with 0 and sets the index to the date range. 
    result.index.name = label # Renames the index from ended_at to Month or Day
    result.columns.name = None
    return result


def Find_Share_Of_Listening(selected: pd.DataFrame, everything: pd.DataFrame) -> pd.DataFrame:

    shares_data = (selected.groupby("artist")["minutes"].sum()
                 .sort_values(ascending=False).reset_index())
    # Gets dataframe with artist as the index with the corresponding minutes played for that artist
    others = everything.loc[~everything["artist"].isin(shares_data["artist"]), "minutes"].sum()
    # Gets sum of minutes for the artists not selected
    if others > 0:
        extra = pd.DataFrame({"artist": ["All other artists"], "minutes": [others]})
        shares_data = pd.concat([shares_data, extra], ignore_index=True)
        # Now two rows exist, one for selcted artists and one for all others, with minute values for each
    return shares_data