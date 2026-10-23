import io, os, sys, time
import pandas as pd
import requests

SRC = r"c:\Projects\HCAD_GEO\bq-results-20261023-145040-1792767070179.csv"
OUT = r"c:\Projects\HCAD_GEO\hcad_geocoded.csv"
CACHE = r"c:\Projects\HCAD_GEO\geocode_cache.csv"
URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
BATCH = 5000

df = pd.read_csv(SRC, dtype=str, keep_default_na=False)
addrs = df["geo_address"].str.strip()
unique = sorted(a for a in addrs.unique() if a)

if os.path.exists(CACHE):
    cache = pd.read_csv(CACHE, dtype=str, keep_default_na=False)
else:
    cache = pd.DataFrame(columns=["geo_address", "match", "lat", "lon"])
done = set(cache["geo_address"])
todo = [a for a in unique if a not in done]
print(f"{len(unique)} unique addresses, {len(todo)} to geocode", flush=True)


def parse(a):
    parts = [p.strip() for p in a.split(",")]
    street = parts[0]
    city = parts[1] if len(parts) > 2 else ""
    zipc = parts[-1] if len(parts) > 1 else ""
    return street, city, zipc


for i in range(0, len(todo), BATCH):
    chunk = todo[i:i + BATCH]
    lines = []
    for j, a in enumerate(chunk):
        s, c, z = parse(a)
        lines.append(f'{j},"{s.replace(chr(34), "")}","{c}",TX,{z[:5]}')
    for attempt in range(4):
        try:
            r = requests.post(URL, files={"addressFile": ("a.csv", "\n".join(lines))},
                              data={"benchmark": "Public_AR_Current"}, timeout=600)
            r.raise_for_status()
            break
        except Exception as e:
            print("retry", e, flush=True)
            time.sleep(10 * (attempt + 1))
    else:
        sys.exit("failed")
    res = pd.read_csv(io.StringIO(r.text), header=None, dtype=str, keep_default_na=False,
                      names=["id", "in", "match", "mtype", "maddr", "coord", "tlid", "side"])
    rows = []
    for _, x in res.iterrows():
        lon = lat = ""
        if x["match"] == "Match" and "," in x["coord"]:
            lon, lat = x["coord"].split(",")
        rows.append((chunk[int(x["id"])], x["match"], lat, lon))
    got = {r_[0] for r_ in rows}
    rows += [(a, "No_Response", "", "") for a in chunk if a not in got]
    cache = pd.concat([cache, pd.DataFrame(rows, columns=cache.columns)])
    cache.to_csv(CACHE, index=False)
    print(f"{i + len(chunk)}/{len(todo)}", flush=True)

out = df.merge(cache.drop_duplicates("geo_address"), on="geo_address", how="left")
out.rename(columns={"match": "geocode_match", "lat": "latitude", "lon": "longitude"}).to_csv(OUT, index=False)
print("matched:", (out["match"] == "Match").sum(), "of", len(out))
