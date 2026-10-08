# 2. Choosing to use `session_state` instead of `cache_data`

## Status

**Accepted**

## Context

`streamlit` re-runs the entire frontend code on each update of the application. This means that the script re-parses and re-cleans the data on each re-run. This is likely to cause serious performance problems with large datasets.
To prevent frustration for users, caching will be implemented for the initial dataframe made from the cleaned uploaded data (held by the analyser). There are two main ways I looked at doing this in `streamlit`:
 
- **Using `cache_data`** - Cached data is held across the whole server for all users, data is held until removed or the server crashes/restarts. Caches a function's return value, and is keyed on the arguments passed into that function. It updates automatically only when the arguments change
- **Using `session_state`** - Cached data held specifically to each user's session, data disappears after the session is ended

The app may be deployed publicly, and listening history is personal data, so it should not sit in a store shared between users.

## Decision

`session_state` will be used to cache the initial dataframe:

- Cached data will be held by the user's session only, when the session is ended the data disappears
- The analyser (holds the cleaned dataframe) as well as a fingerprint for the file (means changes to the uploaded file can be detected) will be cached. The analyser will be rebuilt if the fingerprint changes.

## Consequences

**Positives:**

- Data stays scoped only to the user in a specific session, and is removed as soon as the session ends

**Accepted trade-offs:**

- Less convenient as all data to be cached, or removed from cache (during the session) has to be managed manually
- Memory use grows with the number of active sessions, because each holds its own cached data
- A second tab, or a returning user, has to re-parse the file, since nothing is shared between sessions
