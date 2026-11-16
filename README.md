# climate-imagination-lab

An interactive classroom climate scenario explorer inspired by Amitav Ghosh’s *The Great Derangement*. Explore illustrative climate risks for Indian cities, compare warming and rainfall scenarios, and discuss adaptation choices. Educational demonstration only; not a forecast or measured risk assessment.

A complete, beginner-editable classroom demonstration inspired by Amitav Ghosh’s *The Great Derangement*. It contains a responsive frontend and a separate Python backend. The backend serves the website and provides the scenario API, so the same project can run locally or as one simple hosted service.

## Folder map

```text
climate-imagination-lab/
├── backend/
│   └── server.py             # Web server, API endpoints, model inputs and formulas
├── frontend/
│   ├── index.html            # Website content and page structure
│   ├── style.css             # Colors, layout and mobile/print styles
│   ├── app.js                # Controls, charts, sharing, export and demo mode
│   ├── model.js              # Local fallback so controls work without a server
│   ├── favicon.svg           # Browser icon
│   ├── hero-overrides.css    # Full-screen photo and expanded control layout
│   ├── risk-curve.css        # Composite-risk chart styling
│   ├── assets/
│   │   └── climate-coast-hero.png # Generated photographic monsoon-city hero
│   └── 404.html              # Friendly missing-page screen
├── tests/
│   ├── test_model.py         # Python API and scoring checks
│   └── test_frontend_model.cjs # Browser-model and chart-calibration checks
├── render.yaml               # One-click service configuration for Render
├── requirements.txt          # No extra Python packages are needed
├── start.bat                 # Windows double-click launcher
└── README.md
```

## Run locally on Windows

1. Extract/open this folder in File Explorer.
2. Double-click `start.bat`.
3. If Python 3 is installed, the full local web service opens at `http://localhost:8010`; keep its server window open while presenting. The launcher uses a separate port from the earlier version to avoid loading an old server by mistake.
4. If Python is not installed, the launcher opens the page directly and its built-in browser model still responds to all scenario controls. To use the Python service instead, install Python 3.9 or later from [python.org](https://www.python.org/downloads/) and enable the Python launcher, then double-click `start.bat` again.

If Windows says it cannot find Python, install it or ask whoever manages your computer to enable it, then double-click `start.bat` again. To stop the website, close the black window.

## What you can demonstrate

- Choose among eight Indian cities and inspect a sample teaching profile.
- Change warming; choose from five rainfall assumptions and five time horizons; then test one of nine hypothetical adaptation actions.
- Read an interactive, color-coded risk curve from +0°C to +4°C, compare unmitigated and invested flood scenarios, and adjust the illustrative flood-resilience investment slider.
- See five scenario signals and a bar chart update immediately.
- Compare the selected city against another city under the same scenario settings.
- Load preset stories, copy a URL with scenario settings, export scenario JSON, or print a summary.
- Open **Start demo** for a guided four-step, roughly 2–3 minute presentation.
- Expand **Read the methods** to discuss assumptions, limitations and ways to improve the model.

## Edit the project

Use a code editor such as Visual Studio Code. Change text in `frontend/index.html`, visual styling in `frontend/style.css` or `frontend/hero-overrides.css`, and page interactions in `frontend/app.js`. The standalone fallback formula is in `frontend/model.js`; keep it aligned with `backend/server.py` if you change formulas. Save your changes and refresh the page. For backend changes, stop the server window and reopen `start.bat`.

## Model and data notes

This project does **not** use live weather data, official climate projections, measured city-risk data, or machine learning. City profile scores and formula coefficients are invented, transparent teaching inputs. Approximate coordinates identify cities for the interface; they do not describe exposure. Rainfall options (−30%, −15%, baseline, +15%, +30%) and years (2030, 2040, 2050, 2070, 2090) are scenario controls, not official pathways or predictions. Each pressure score is clamped to a 0–100 range and should be read only as the response of this classroom formula. The chart’s +3°C Chennai example is calibrated to show about 65 without new flood investment and 46 at 65% investment; changing the city, rainfall, year, slider, or chosen action changes the illustrative line. Investment percentages are demonstration controls, not actual funding amounts or measured intervention effectiveness. The nine adaptation ideas subtract fixed illustrative amounts and are not estimates of real intervention effectiveness. The landing-page photograph is AI-generated for the project and does not depict a documented event or a specific real city.

For a research version, replace sample inputs only after collecting documented, relevant local data. Potential places to begin research include the India Meteorological Department, official city disaster management plans, and IPCC assessment reports. The current demo does not claim its numbers came from those sources. Record source, year, geographic coverage, units, license and any transformations before using a dataset. Have a climate or domain expert review any claim about real-world risk.

## Tests

The project uses Python’s built-in test runner and has no Python package dependencies. To check the browser-side model, Node.js is also needed:

```text
python -m unittest discover -s tests -v
node tests/test_frontend_model.cjs
```

## Deploy on Render

The included `render.yaml` configures one Python web service. No third-party packages, environment variables, API keys, or database are required.

1. Create a GitHub account if you do not already have one, then create a **new private repository** for this project.
2. Upload the contents of this `climate-imagination-lab` folder to the repository. Do not include credentials or private data.
3. Create/sign in to a Render account and choose **New → Blueprint**.
4. Connect the GitHub repository and select **Apply** for the `render.yaml` configuration.
5. Wait for the service to deploy, then open the `onrender.com` URL Render provides. Confirm `/api/health` responds with `{"ok": true}` and the homepage loads.

Render’s free service availability and sleep behavior can change; check the current plan details in Render before relying on it for an event. For a classroom demonstration, run `start.bat` locally as a fallback.

## Install on a phone

After deployment over HTTPS, Chrome on Android can offer **Install app** from the browser menu (and this site shows an install button when Chrome exposes the install prompt). In Safari on iPhone, open **Share → Add to Home Screen**. The app shell, styling, scripts, and hero image are cached for later visits; scenario calculations continue using the built-in illustrative model when offline. Live API responses require a connection.

The interface adapts to narrow screens, with controls that are easier to tap and charts that scale to the available width. Validate the published build on current iOS Safari and Android Chrome before using it in a live classroom; this package has not been device-tested on physical iOS or Android hardware.

## Accessibility and security basics

The controls have labels, the risk cards expose accessible names, keyboard focus is available, and layouts adapt to mobile and print. The backend validates all scenario inputs, serves only files inside `frontend/`, and sends basic browser security headers. Fonts load from Google Fonts when online; the page remains usable if those fonts are unavailable.

