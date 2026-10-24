# City and local cultural places

`landmarks.json` is the complete Wikidata CC0 snapshot, retained in source for audit and regeneration. It is intentionally outside `public/`: the uncompressed export exceeds the host's 25 MiB single-file limit. The website loads the lossless compact index at `public/data/landmarks-index.json` and generates shared display fields in the client.

Refresh public query exports with `python3 scripts/download-landmarks.py` (or `--only china-local global-museums global-places`), then run `python3 scripts/prepare-landmarks.py` and `node scripts/prepare-landmark-regions.mjs`. The pipeline preserves existing records, original item URLs, country memberships, data classes and coordinates. Query batch limits are recorded in the coverage manifest; this is a sourced selection, not a complete or live directory of every attraction.

Wikidata structured data is CC0. Image rights remain with their Wikimedia Commons authors; Wikipedia summaries are fetched with an attribution link and the CC BY-SA notice. The tests compare the full snapshot and compact index, check administrative containment, and verify deduplication and coverage counts. The build also checks the hosting asset-size limit.
