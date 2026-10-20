"""Streamlit frontend for Spotify Streaming History Analyser.

ADR1 - This file only collects the users choices and displays them or creates charts, does not 
apply any filters or carry out any analysis logic. 
ADR2 - The analyser is kept in session_state and rebuilt only when the uploaded files change.
"""
import hashlib
import streamlit as st
from matplotlib.figure import Figure
from src.analyser import StreamingAnalyser
from src.cleaner import CleaningError
from src.filters import Filters
from src.loader import InvalidStreamingHistoryError

QUICK_MENU = ["Most played artist", "Most played track", "Top 10 tracks", "Top 10 artists"]

# Black and green palette. The page colours live in .streamlit/config.toml.
# These are for the Matplotlib charts, which Streamlit's theme does not reach.
BG = "#121212"
MUTED = "#B3B3B3"
TEXT = "#FFFFFF"
GREEN = "#1DB954"
GRID = "#535353"
PALETTE = [GREEN, "#FFFFFF", "#8EE3A8", "#B3B3B3", "#0E9F47", "#D9D9D9"]

# Small touches the theme file cannot do. Selectors differ between Streamlit
# versions, so if a button looks unstyled, inspect it and adjust these.
STYLE = """
<style>
[data-testid="stMetricValue"] { color: #1DB954; }
.stButton > button { border-radius: 500px; font-weight: 700; }
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"],
.stButton > button[kind="primary"] p,
button[data-testid="stBaseButton-primary"] p { color: #121212; }
</style>
"""

st.set_page_config(page_title="Spotify Streaming History Analyser", layout="wide")
st.markdown(STYLE, unsafe_allow_html=True)


def fingerprint(files) -> str:
    """Hash of the uploaded files' contents, used to detect a new upload."""
    hash = hashlib.sha256()
    for f in files:
        hash.update(f.getvalue())
    return hash.hexdigest()


def new_figure():
    """Sets up figure and axes matching the page background."""
    figure = Figure(figsize=(6, 3.5), facecolor=BG)
    axis = figure.subplots()
    axis.set_facecolor(BG)
    axis.tick_params(colors=MUTED)
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axis.spines[side].set_color(GRID) 
    return figure, axis


def label_axes(axis, title: str, xlabel: str = "", ylabel: str = "") -> None:
    axis.set_title(title, color=TEXT)
    axis.set_xlabel(xlabel, color=MUTED)
    axis.set_ylabel(ylabel, color=MUTED)


def bar_chart(labels, values, title: str, xlabel: str) -> Figure:
    """Sets up horizontal bar chart with the largest value at the top."""
    figure, axis = new_figure()
    axis.barh(labels, values, color=GREEN)
    axis.invert_yaxis()
    label_axes(axis, title, xlabel)
    figure.tight_layout()
    return figure


def line_chart(over_time) -> Figure:
    """Minutes listened against time, one line per artist."""
    period = over_time.index.name  # "Day" or "Month", named by the backend
    figure, axis = new_figure()
    for i, artist in enumerate(over_time.columns):
        axis.plot(over_time.index, over_time[artist], marker="o", markersize=3,
                color=PALETTE[i % len(PALETTE)], label=artist)
    if len(over_time.columns) > 1:
        axis.legend(facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
    label_axes(axis, "Listening over time", period, f"Minutes per {period.lower()}")
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure


def pie_chart(share) -> Figure:
    """Shows shares of total listening time, with colours so small slices stay readable."""
    figure, axis = new_figure()
    wedges, *_ = axis.pie(
        share["minutes"], startangle=90, counterclock=False,
        colors=[PALETTE[i % len(PALETTE)] for i in range(len(share))],
        wedgeprops={"edgecolor": BG, "linewidth": 2},
        autopct=lambda p: f"{p:.0f}%" if p >= 3 else "",
        textprops={"color": BG, "fontweight": "bold"},
    )
    axis.legend(wedges, share["artist"], loc="center left", bbox_to_anchor=(1, 0.5),
              facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
    label_axes(axis, "Share of total listening time")
    figure.subplots_adjust(left=0.02, right=0.6)
    return figure


def toggle_table() -> None:
    st.session_state.show_table = not st.session_state.show_table


def reset_filters() -> None:
    """New widget keys make Streamlit create the widgets afresh, at their defaults."""
    st.session_state.filter_version += 1


st.session_state.setdefault("show_table", False) 
# Stores whether data table is to be shown, adds to session_state if doesnt already exist
st.session_state.setdefault("filter_version", 0) 
# Stores the current itteration of filters, adds to session_state if it doesnt already exist
# Each time filter version is incremented filters are reset 


st.title("Spotify Streaming History Analyser")
st.sidebar.header("Quick menu")
choice = st.sidebar.radio("Quick menu", QUICK_MENU, label_visibility="collapsed")

left, right = st.columns([1, 1.4]) 
# Creates the left and right columns, right column takes up 40% more of the page than the left


with left:
    uploaded = st.file_uploader(
        "Upload JSON", type="json", accept_multiple_files=True,
        help="Select every StreamingHistory_music_*.json file from your Spotify export.",
    )
    st.caption("Your files are processed in memory for this session only.")

if not uploaded:
    # Remove cached data and stop this run of the app
    st.session_state.pop("analyser", None)
    st.session_state.pop("fingerprint", None)
    left.info("Upload your streaming history JSON files to see your listening stats.")
    st.stop()

finger_print = fingerprint(uploaded) # Hash value to track if uploaded files change
if st.session_state.get("fingerprint") != finger_print: 
    # If the uploaded files change update the cache (Analyser instance and fingerprint)
    try:
        with st.spinner("Reading your history..."): # Shows loading sign
            st.session_state.analyser = StreamingAnalyser.load_files(uploaded) # Create intance of streaming analyser set up with correct data
        st.session_state.fingerprint = finger_print
        reset_filters()  # A new file could have a new date range and artist list
    except (InvalidStreamingHistoryError, CleaningError) as e:
        st.session_state.pop("analyser", None)
        st.session_state.pop("fingerprint", None)
        left.error(str(e))
        st.stop()

analyser = st.session_state.analyser
version = st.session_state.filter_version


with left:
    selected_artists = st.multiselect(
        "Search for artist", analyser.Artist_List(), key=f"artists_{version}")
    # Artist search bar
    with st.expander("Filter selection"):
        first_day, last_day = analyser.Date_Range()
        dates = st.date_input(
            "Date range", value=(first_day, last_day),
            min_value=first_day, max_value=last_day, key=f"dates_{version}",
        )
        # date_input returns one date while the user is still picking the second

        min_minutes = st.slider(
            "Ignore plays shorter than (minutes)", 0.0, 2.0, 0.0, 0.1,
            key=f"min_minutes_{version}",
        )
    st.button("Reset filters", on_click=reset_filters)

start, end = dates if len(dates) == 2 else (None, None)

filters = Filters(
    artist_names=tuple(selected_artists) or None,
    min_minutes=min_minutes,
    start_bound=start,
    end_bound=end,
)

plays = analyser.Play_Count(filters)
if plays == 0:
    left.warning("No plays match these filters. Widen the date range or reset the filters.")
    st.stop()

top_artists = analyser.Top_10_Most_Played_Artists(filters)
top_tracks = analyser.Top_10_Most_Played_Tracks(filters)


with left:
    st.subheader("Statistics and info")
    st.metric("Plays", f"{plays:,}")
    if choice == "Most played artist":
        row = analyser.Most_Played_Artist(filters).iloc[0] 
        # Convert to pandas series so individual elements can be accessed easily
        st.metric("Most played artist", row["artist"])
        st.caption(f"{row['minutes']:.0f} minutes listened")
    elif choice == "Most played track":
        row = analyser.Most_Played_Track(filters).iloc[0]
        st.metric("Most played track", row["track"])
        st.caption(f"{row['artist']}, {row['plays']} plays")
    elif choice == "Top 10 tracks":
        st.dataframe(top_tracks, hide_index=True)
    else:
        st.dataframe(top_artists, hide_index=True)


with right:
    if selected_artists:
        st.pyplot(line_chart(analyser.Listening_Over_Time(filters)))
        st.pyplot(pie_chart(analyser.Listening_Share(filters)))
    else:
        st.pyplot(bar_chart(top_artists["artist"], top_artists["minutes"],
                            "Top 10 artists", "Minutes played"))
        st.pyplot(bar_chart(top_tracks["track"] + " - " + top_tracks["artist"],
                            top_tracks["plays"], "Top 10 tracks", "Plays"))
    st.button(
        "Hide data table" if st.session_state.show_table else "See data table",
        on_click=toggle_table,
        type="primary",
    )

if st.session_state.show_table:
    st.divider()
    st.dataframe(analyser.Get_Data(filters), hide_index=True)