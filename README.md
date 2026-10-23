# HCAD Property Map

Interactive Leaflet map of geocoded HCAD properties (colored by value, value change, or protest status; filter by Protested YES/NO, value range, and text search).

## Publish with GitHub Pages
1. Push this repo to GitHub.
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main`, folder: `/docs`.
3. The map is served at `https://<user>.github.io/<repo>/`.

## Rebuild data
- `python geocode.py` – geocodes `geo_address` via the US Census batch geocoder (CSVs are git-ignored).
- `python make_webmap_data.py` – regenerates `docs/data.js`.
