import pandas as pd
import json

class InvalidStreamingHistoryError(Exception):
    '''Raised when the streaming history data is invalid.'''

def Load_Streaming_History_Data(files) -> pd.DataFrame:

    if not files:
        raise InvalidStreamingHistoryError("No files provided")
    
    dataframes = [load_one_file(f) for f in files] # Take each file and load it into a DataFrame using the load_one_file function
    return pd.concat(dataframes, ignore_index=True)


def load_one_file(file) -> pd.DataFrame:

    name = getattr(file, "name", "uploaded file")

    try:
        data = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        '''JSONDecodeError is raised when the JSON is invalid, and UnicodeDecodeError is raised when the bytes are not valid text.'''
        raise InvalidStreamingHistoryError(f"{name} is not valid JSON") from e

    if not isinstance(data, list):
        raise InvalidStreamingHistoryError(
            f"{name} must contain a list of records"
        )
    if not data:
        raise InvalidStreamingHistoryError(f"{name} contains no records")

    df = pd.DataFrame(data)

    if not all(col in df.columns for col in ["endTime", "artistName", "trackName", "msPlayed"]):
        #   Check if the required columns are present in the DataFrame
        raise InvalidStreamingHistoryError(f"{name} is missing required columns in streaming history data")
    
    return df