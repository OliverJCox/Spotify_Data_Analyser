import pandas as pd
import json

class invalidStreamingHistoryError(Exception):
    '''Raised when the streaming history data is invalid.'''

def Load_Streaming_History_Data(file) -> pd.DataFrame:

    try:
        data = pd.read_json(file)
        
    except (json.JSONDecodeError) as e:       
        raise invalidStreamingHistoryError("Invalid streaming history data") from e
    
    if data.empty:
        raise invalidStreamingHistoryError("Empty streaming history data")
    
    if not all(col in data.columns for col in ["endTime", "artistName", "trackName", "msPlayed"]):
        raise invalidStreamingHistoryError("Missing required columns in streaming history data")
    return data