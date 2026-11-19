# HCAD Property Map

Interactive Leaflet map of geocoded HCAD properties (colored by value, value change, or protest status; filter by Protested YES/NO, value range, and text search).

## Quick tutorial
(Also available in the app via the **?** button.)

**Inspect a property**
- *Hover* a dot for a preview (address, account #, value). Hit areas are larger than the dots, so you don't need pixel-perfect aim.
- *Click* a dot to pin its details. The popup stays open until you click the map or its ×, so you can select/copy text.
- Press **Copy** next to *Acct* to copy the account number for the HCAD or Harris County Tax Office search. Account numbers are always 13 characters (padded with leading zeros).

**Filter** – Protested, Present in 2024, market value, year of improvement, zip code, exemptions. *Matching filters* shows the remaining count.

**Display** – *View*: points or heatmap; *Cluster points* groups dots; top-left layer control switches basemaps; ⌂ resets to the whole county, ◎ finds your location, ⛶ fullscreen.

**Whole-county screenshots**
- Click **«** in the panel header (or press `P`) to collapse the panel and legend; click **☰ Panel** to restore it.
- Press `H` to hide every overlay (panel, controls, credit box); press `H` again to restore.

**Shortcuts** – `P` panel, `H` clean view, `?` help, `Esc` close help.

## Publish with GitHub Pages
1. Push this repo to GitHub.
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main`, folder: `/docs`.
3. The map is served at `https://<user>.github.io/<repo>/`.

## Rebuild data
- `python geocode.py` – geocodes `geo_address` via the US Census batch geocoder (CSVs are git-ignored).
- `python make_webmap_data.py` – regenerates `docs/data.js`.
