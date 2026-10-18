import pandas as pd
from . import analysis, loader, cleaner
from .filters import Filters


class StreamingAnalyser:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @classmethod
    def load_files(cls, files) -> "StreamingAnalyser":
        # Sets up class with correct Dataframe, interfacing with loading and cleaning modules
        return cls(cleaner.Clean(loader.Load_Streaming_History_Data(files)))

    def _Apply_Filters(self, filters: Filters) -> pd.DataFrame: # Underscore is internal method convention

        '''Applies all the relevant filters to the clean dataframe and returns the result
        
        The min_minutes filter specifies the minimum length a track has to be to count as 
        a play.'''

        df = self._df
        if filters.artist_names:
            df = df[df['artist'].isin(filters.artist_names)]
        if filters.track_names:
            df = df[df['track'].isin(filters.track_names)]
        if filters.min_minutes:
            df = df[df['minutes'] >= filters.min_minutes]
        if filters.start_bound:
            df = df[df['ended_at'].dt.date >= filters.start_bound]
        if filters.end_bound:
            df = df[df['ended_at'].dt.date <= filters.end_bound]

        return df

    def Most_Played_Artist(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)
        return analysis.Find_Top_Artists(df=df, number=1)
    
    def Most_Played_Track(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)
        return analysis.Find_Top_Tracks(df=df, number=1)

    def Top_10_Most_Played_Artists(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)
        return analysis.Find_Top_Artists(df=df)

    def Top_10_Most_Played_Tracks(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)
        # Return a copy to prevent internal dataframe being accessed
        return analysis.Find_Top_Tracks(df=df)

    def Get_Data(self, filters: Filters) -> pd.DataFrame:
        return self._Apply_Filters(filters=filters).copy()

    def Total_Minutes_Played(self, filters: Filters) ->float:
        df = self._Apply_Filters(filters=filters)
        return analysis.Find_Mins_Played(df)

    def Play_Count(self, filters: Filters) ->int:
        df = self._Apply_Filters(filters=filters)
        return analysis.Track_Play_Count(df)