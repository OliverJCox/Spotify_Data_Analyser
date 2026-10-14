import pandas as pd
import loader 
import cleaner
from filters import Filters

class StreamingAnalyser:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @classmethod
    def load_files(cls, files) -> StreamingAnalyser:
        # Sets up class with correct Dataframe, interfacing with loading and cleaning modules
        return cls(cleaner.Clean(loader.Load_Streaming_History_Data(files)))

    def _Apply_Filters(self, filters: Filters) -> pd.DataFrame: # Underscore is internal method convention

        '''Apllies all the relevant filters to the clean dataframe and returns the result'''

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

    def Most_Played_Aritst(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)
    
    def Most_Played_Song(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)

    def Top_10_Most_Played_Artists(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)

    def Top_10_Most_Played_Artists(self, filters: Filters) -> pd.DataFrame:
        df = self._Apply_Filters(filters=filters)

    def Get_Data(self, filters: Filters) -> pd.DataFrame:
        return self._Apply_Filters(filters=filters)