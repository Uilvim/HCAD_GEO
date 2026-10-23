import json
import pandas as pd

d = pd.read_csv(r"c:\Projects\HCAD_GEO\hcad_geocoded.csv", dtype=str, keep_default_na=False)
d = d[d.latitude != ""]
num = lambda s: pd.to_numeric(s, errors="coerce")
rows = []
for r in d.itertuples():
    mkt, prior, bld, yr = num(r.tot_mkt_val), num(r.prior_tot_mkt_val), num(r.bld_ar), num(r.yr_impr)
    f = lambda v: None if pd.isna(v) else int(v)
    rows.append([round(float(r.latitude), 5), round(float(r.longitude), 5), r.acct, r.geo_address,
                     "", f(mkt), f(prior), 1 if r.protest_status == "protested" else 0,
                 f(yr), f(bld), r.lgl_4.strip() or r.lgl_3.strip(), r.site_addr_3.strip()[:5],
                 sorted({t.strip() for t in r.exempt_categories.split(",")} - {"NONE", ""}),
                 1 if r.Present_in_2024 == "YES" else 0])
with open(r"c:\Projects\HCAD_GEO\docs\data.js", "w") as fh:
    fh.write("const DATA=" + json.dumps(rows, separators=(",", ":")) + ";")
print(len(rows))
