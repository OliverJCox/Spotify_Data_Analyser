# 3. Accept multiple streaming history files per upload

## Status

**Accepted**

## Context

The app analyses the Spotify account data export. For long listening histories, Spotify may split the streaming history across several JSON files rather than providing one. For shorter histories, including the my own, the export is a single file.

If the app accepted only one file, users with a split export would see results for just the file they uploaded. The app cannot detect this, so the numbers could look complete when they are not.

Three options were considered:

- **Single file upload.** The simplest loader and fingerprint, but silently incomplete for users with split exports.
- **Multiple file upload.** The user selects all their streaming history files at once and the app combines them.
- **Zip upload.** The user uploads the export as Spotify provides it. This is the most convenient, but the zip contains many unrelated files (containing even more personal data), so the loader would need to find the right entries, guard against oversized or malicious archives, and handle more error cases.

## Decision

Accept multiple streaming history JSON files in one upload. 

- The loader validates each file separately and combines the valid ones into a single DataFrame.
- If any file is invalid, the whole upload is rejected, and the error message names the file that failed.
- The cleaner sorts the combined data by time, so the result does not depend on the order the files were uploaded in.
- The fingerprint stored in `session_state` (see ADR 2) is a hash of the contents of all uploaded files.

## Consequences

**Positives:**

- Users with a split export can see their full history.
- Every layer after the loader is unchanged, because it only sees a DataFrame.
- No archive handling is needed, which avoids the extra security considerations that come with zip files.

**Accepted trade-offs:**

- Users must unzip the export and select the history files themselves.
- Rejecting the whole upload when one file is invalid is simple to explain and test, but it means one bad file blocks the others.

## Alternatives considered

- **Single file upload.** Rejected because it silently gives incomplete results for users with split exports.
- **Zip upload.** Rejected for now because it adds complexity and security concerns (finding the right entries, oversized archives) that are out of scope at this stage. It would also send more personal data to a hosted deployment, since the zip contains much more than listening history. It could be added later as a convenience, and only the loader would need to change.
