# 1. Keep logic out of the Streamlit frontend

## Status

**Accepted**

## Context

Streamlit reruns the whole script on every user interaction. It's easy to build the whole app in one script but it has the following problems:

- Analysis logic can only be tested by running the UI.
- Changing the export format, the charting library or the UI framework means rewriting code that has nothing to do with the change.
- Widget code and data code become tangled, so it is hard to see what a given chart or bit of data depends on.
- Managing how the logic to decide what should be displayed becomes very challenging to do efficiently as the application grows 

## Decision

The Streamlit app (`app.py`) is responsible only for display:

- It renders widgets and collects their values.
- It passes those values to the backend and renders what comes back (mostly Pandas dataframes and Matplotlib charts).
- It contains no data cleaning, filtering or calculation.

Everything else is in the backend that never imports `streamlit`:

- **Loader and cleaner:** turns raw JSON into a DataFrame and cleans it.
- **Analysis functions:** DataFrame in, DataFrame out.
- **`StreamingAnalyzer`:** the single object the frontend talks to. It applies filters and delegates to the analysis functions.

The backend returns data, not figures (charts). Building the charts is the frontend's job.

## Consequences

**Positives:**

- The analysis layer can be unit tested with small hand-built DataFrames, with no Streamlit involved.
- A change to the export format affects only the loader and cleaner.
- Swapping Matplotlib for another charting library affects only `app.py`.
- The frontend reads from one object, so variables do not need to be passed around the app.

**Accepted trade-offs:**

- More files and modules, this means that the system design and data passing around the system is more complex
  
## Alternatives considered

- **Single-script app.** Rejected because it is harder to test, change and scale.
- **Backend returns Matplotlib figures.** Rejected because it links the backend to a charting library and mixes presentation into the logic.
- **One large class that loads, cleans, analyses and plots.** Rejected because it becomes a "god object" with many reasons to change and becomes cumbersome and hard to manage. The facade is kept lightweight instead.
