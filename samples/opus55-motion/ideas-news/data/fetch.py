"""Refresh the live data behind ideas-news: new GitHub repos of the past week + current temperatures.

    python3 data/fetch.py            # writes data/gh.json and data/temps.json next to this file

GitHub search needs the `gh` CLI (authenticated). Open-Meteo needs no key.
After fetching, read gh.json and choose the three repos in build.py's PICK by hand: keep to neutral
topics (no chat-reading tools, crypto, politics, disasters, or anything else sensitive).
"""
import datetime
import json
import pathlib
import subprocess
import urllib.request

HERE = pathlib.Path(__file__).parent

since = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
raw = subprocess.run(["gh", "api", f"search/repositories?q=created:>{since}&sort=stars&order=desc&per_page=15",
                      "--jq", "[.items[] | {name: .full_name, stars: .stargazers_count, forks: .forks_count, lang: .language, desc: .description}]"],
                     capture_output=True, text=True, check=True).stdout
(HERE / "gh.json").write_text(raw)

CITIES = [("Tokyo", 35.68, 139.69), ("Seoul", 37.57, 126.98), ("Beijing", 39.90, 116.40), ("Singapore", 1.35, 103.82),
          ("Sydney", -33.87, 151.21), ("Auckland", -36.85, 174.76), ("Mumbai", 19.08, 72.88), ("Dubai", 25.20, 55.27),
          ("Nairobi", -1.29, 36.82), ("Cairo", 30.04, 31.24), ("Lagos", 6.52, 3.38), ("Cape Town", -33.92, 18.42),
          ("London", 51.51, -0.13), ("Paris", 48.86, 2.35), ("Berlin", 52.52, 13.40), ("Moscow", 55.76, 37.62),
          ("Reykjavik", 64.15, -21.94), ("New York", 40.71, -74.01), ("Chicago", 41.88, -87.63), ("Los Angeles", 34.05, -118.24),
          ("Mexico City", 19.43, -99.13), ("São Paulo", -23.55, -46.63), ("Buenos Aires", -34.60, -58.38), ("Lima", -12.05, -77.04),
          ("Anchorage", 61.22, -149.90), ("Honolulu", 21.31, -157.86), ("Ushuaia", -54.80, -68.30), ("Jakarta", -6.21, 106.85)]
lat = ",".join(str(c[1]) for c in CITIES)
lon = ",".join(str(c[2]) for c in CITIES)
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
rows = json.load(urllib.request.urlopen(url, timeout=30))
temps = [{"city": c[0], "lat": c[1], "lon": c[2], "temp": r["current"]["temperature_2m"], "time": r["current"]["time"]} for c, r in zip(CITIES, rows)]
(HERE / "temps.json").write_text(json.dumps(temps, ensure_ascii=False, indent=1))
print("gh.json:", len(json.loads(raw)), "repos; temps.json:", len(temps), "cities")
