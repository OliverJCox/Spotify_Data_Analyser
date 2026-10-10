import pandas as pd


class CleaningError(Exception):
    """Raised when streaming history cannot be cleaned."""


def Clean(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a raw streaming history DataFrame into the clean schema.

    Rows with an unreadable timestamp or a missing track or artist are
    dropped. Duplicate plays are removed. The input is not modified.

    Returns:
        A DataFrame with columns ended_at, track, artist and minutes,
        sorted by time with a fresh index.

    Raises:
        CleaningError: If msPlayed is not numeric, or no valid plays remain.
            The frontend should catch this and show "No valid plays found"."""
    
    try:
        ms_played = pd.to_numeric(df["msPlayed"], errors="coerce")
    except (ValueError, TypeError) as e:
        raise CleaningError(f"'msPlayed' column is not in the expected format: {e}")

    cleaned_df = pd.DataFrame({
        "ended_at": pd.to_datetime(
            df["endTime"], format="%Y-%m-%d %H:%M", errors="coerce"
        ),
        "track": df["trackName"],
        "artist": df["artistName"],
        "minutes": ms_played / 60000,
    })

    cleaned_df = (
        cleaned_df.dropna()
        .drop_duplicates()
        .sort_values(["ended_at", "track", "artist", "minutes"])
        .reset_index(drop=True)
    )

    if cleaned_df.empty:
        raise CleaningError("No valid plays found after cleaning")
    
    return cleaned_df
