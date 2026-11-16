"""Dependency-free web server and illustrative Climate Imagination Lab API."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import json
import os

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"

# These are deliberately illustrative teaching inputs, not measured city data.
CITIES = {
    "Chennai": {"state": "Tamil Nadu", "coastal": .88, "heat": .82, "rain": .76, "urban": .73, "eco": .58, "lat": 13.08, "lon": 80.27},
    "Mumbai": {"state": "Maharashtra", "coastal": .94, "heat": .69, "rain": .88, "urban": .86, "eco": .55, "lat": 19.08, "lon": 72.88},
    "Kolkata": {"state": "West Bengal", "coastal": .76, "heat": .79, "rain": .82, "urban": .82, "eco": .62, "lat": 22.57, "lon": 88.36},
    "Delhi": {"state": "Delhi", "coastal": .04, "heat": .94, "rain": .55, "urban": .88, "eco": .68, "lat": 28.61, "lon": 77.21},
    "Bengaluru": {"state": "Karnataka", "coastal": .05, "heat": .61, "rain": .65, "urban": .72, "eco": .50, "lat": 12.97, "lon": 77.59},
    "Kochi": {"state": "Kerala", "coastal": .90, "heat": .65, "rain": .91, "urban": .61, "eco": .46, "lat": 9.93, "lon": 76.27},
    "Ahmedabad": {"state": "Gujarat", "coastal": .22, "heat": .92, "rain": .43, "urban": .77, "eco": .71, "lat": 23.02, "lon": 72.57},
    "Hyderabad": {"state": "Telangana", "coastal": .08, "heat": .83, "rain": .62, "urban": .78, "eco": .61, "lat": 17.39, "lon": 78.49},
}
RAINFALL_SCENARIOS = {70, 85, 100, 115, 130}
TIME_HORIZONS = {2030: .55, 2040: .72, 2050: 1, 2070: 1.23, 2090: 1.45}
ADAPTATIONS = {"none", "shade", "cool_roofs", "drainage", "wetlands", "permeable",
               "cooling_centres", "early_warning", "transit", "water_saving"}

def scenario(city="Chennai", warming=2, rainfall=100, year=2050, adaptation="none", investment=65):
    """Return transparent 0–100 classroom signals; values are not forecasts."""
    if city not in CITIES:
        raise ValueError("Choose one of the listed cities.")
    if warming not in (1, 2, 3):
        raise ValueError("Warming must be 1, 2, or 3 °C.")
    if rainfall not in RAINFALL_SCENARIOS:
        raise ValueError("Choose one of the listed rainfall scenarios: 70, 85, 100, 115, or 130 percent.")
    if year not in TIME_HORIZONS:
        raise ValueError("Choose a listed time horizon.")
    if adaptation not in ADAPTATIONS:
        raise ValueError("Choose a listed adaptation action.")
    if not 0 <= investment <= 100:
        raise ValueError("Investment must be between 0 and 100 percent.")
    p = CITIES[city]
    horizon = TIME_HORIZONS[year]
    heat = 19 + p["heat"] * 37 + warming * 9 * horizon
    flood = 12 + p["coastal"] * 31 + p["rain"] * 20 + (rainfall - 100) * .43 + warming * 3.5 * horizon - investment * .29
    extreme = 14 + p["rain"] * 36 + (rainfall - 100) * .55 + warming * 4 * horizon
    urban = 15 + p["urban"] * 50 + warming * 4 * horizon + max(0, rainfall - 100) * .11
    eco = 12 + p["eco"] * 43 + warming * 7 * horizon + max(0, rainfall - 100) * .1
    reductions = {
        "shade": {"Heat stress": 15, "Urban vulnerability": 3},
        "cool_roofs": {"Heat stress": 12, "Urban vulnerability": 4},
        "drainage": {"Flood exposure": 17, "Extreme rainfall": 10, "Urban vulnerability": 8},
        "wetlands": {"Flood exposure": 13, "Extreme rainfall": 6, "Ecological pressure": 9},
        "permeable": {"Flood exposure": 10, "Extreme rainfall": 8, "Ecological pressure": 3},
        "cooling_centres": {"Heat stress": 10, "Urban vulnerability": 9},
        "early_warning": {"Flood exposure": 7, "Extreme rainfall": 9, "Urban vulnerability": 8},
        "transit": {"Heat stress": 3, "Urban vulnerability": 8, "Ecological pressure": 8},
        "water_saving": {"Heat stress": 4, "Ecological pressure": 9},
    }
    raw = {"Heat stress": heat, "Flood exposure": flood, "Extreme rainfall": extreme,
           "Urban vulnerability": urban, "Ecological pressure": eco}
    for key, amount in reductions.get(adaptation, {}).items():
        raw[key] -= amount
    risks = {key: max(0, min(100, round(value))) for key, value in raw.items()}
    curve = risk_curve(city, rainfall, year, investment, adaptation)
    return {"city": city, "state": p["state"], "warming": warming, "rainfall": rainfall,
            "year": year, "adaptation": adaptation, "investment": investment, "risks": risks, "curve": curve,
            "profile": {"coastal_influence": p["coastal"], "heat_sensitivity": p["heat"],
                        "rainfall_sensitivity": p["rain"], "urban_pressure": p["urban"],
                        "ecological_sensitivity": p["eco"]}}

def risk_curve(city, rainfall, year, investment, adaptation="none"):
    """Create the illustrative multi-hazard curve used by the dashboard chart."""
    p, horizon = CITIES[city], TIME_HORIZONS[year]
    action_reductions = {
        "shade": {"Flood exposure": 0}, "cool_roofs": {"Flood exposure": 0},
        "drainage": {"Flood exposure": 17}, "wetlands": {"Flood exposure": 13},
        "permeable": {"Flood exposure": 10}, "cooling_centres": {"Flood exposure": 0},
        "early_warning": {"Flood exposure": 7}, "transit": {"Flood exposure": 0},
        "water_saving": {"Flood exposure": 0},
    }
    action_flood_reduction = action_reductions.get(adaptation, {}).get("Flood exposure", 0)
    points = [round(i * .5, 1) for i in range(9)]
    series = {"temperature": [], "flood_unmitigated": [], "people_affected": [], "flood_invested": []}
    rain_shift = rainfall - 100
    for warming in points:
        temp = 22 + p["heat"] * 27 + warming * 10.2 * horizon
        flood = 17 + p["coastal"] * 14 + p["rain"] * 12 + rain_shift * .18 + warming * 8.8 * horizon
        people = 19 + p["urban"] * 17 + p["coastal"] * 3 + rain_shift * .1 + warming * 8.5 * horizon
        values = {"temperature": temp, "flood_unmitigated": flood, "people_affected": people,
                  "flood_invested": flood - investment * .29 - action_flood_reduction}
        for key, value in values.items():
            series[key].append({"warming": warming, "risk": max(0, min(100, round(value)))})
    return series

def json_bytes(value):
    return json.dumps(value, ensure_ascii=False).encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self'; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, value, status=200):
        self.send_bytes(json_bytes(value), "application/json; charset=utf-8", status)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self.send_json({"ok": True})
        if parsed.path == "/api/cities":
            return self.send_json({"cities": [{"name": name, "state": data["state"], "lat": data["lat"], "lon": data["lon"]} for name, data in CITIES.items()]})
        if parsed.path == "/api/scenario":
            q = parse_qs(parsed.query)
            try:
                result = scenario(q.get("city", ["Chennai"])[0], int(q.get("warming", ["2"])[0]),
                                  int(q.get("rainfall", ["100"])[0]), int(q.get("year", ["2050"])[0]),
                                  q.get("adaptation", ["none"])[0], int(q.get("investment", ["65"])[0]))
                return self.send_json(result)
            except (ValueError, TypeError) as error:
                return self.send_json({"error": str(error)}, 400)
        # Serve only files inside frontend, including nested assets.
        requested = unquote(parsed.path).lstrip("/") or "index.html"
        target = (FRONTEND / requested).resolve()
        if not target.is_relative_to(FRONTEND.resolve()) or not target.is_file():
            target = FRONTEND / "404.html"
            status = 404
        else:
            status = 200
        types = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml", ".webmanifest": "application/manifest+json; charset=utf-8", ".png": "image/png", ".ico": "image/x-icon"}
        self.send_bytes(target.read_bytes(), types.get(target.suffix, "application/octet-stream"), status)

    def log_message(self, fmt, *args):
        print("[web] " + fmt % args)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Climate Imagination Lab listening on http://127.0.0.1:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()

