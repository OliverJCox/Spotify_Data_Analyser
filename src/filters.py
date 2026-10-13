from dataclasses import dataclass
import datetime

@dataclass(frozen=True) 
class Filters():

    '''The Filters dataclass holds different filter parameters in an organised way.
    Each instance is made by the frontend. The dataclass is immutable so there is no
    risk of selected filters being confused.
    
    artist_names holds the name(s) of the artist(s) being filtered for
    track_names holds the name(s) of the track(s) being filtered for
    min_minutes holds the minimum play length being filtered for
    start_bound holds the start of the date range to filter
    end_bound holds the end of the date range to filter
    BOTH START AND END BOUND ARE INCLUSIVE'''

    artist_names: tuple[str,...] | None = None
    track_names: tuple[str,...] | None = None
    min_minutes: float = 0.0
    start_bound: datetime.date | None = None
    end_bound: datetime.date | None = None

