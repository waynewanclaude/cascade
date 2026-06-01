# Cascade ◫

**Cascade** is a lightweight, zero-dependency, local-only Python-to-Web visual audit and drill-down framework. It coordinates a cascading chain of visual panels (Columns), displaying them in an overlapping, draggable staircase stack. 

It is designed for researchers, auditors, and developers who want to build custom interactive visual data explorers rapidly, with **zero package dependencies**, **stateless backends**, and **zero local disk clutter**.

---

## Key Features

* 🚀 **Zero Third-Party Dependencies:** Runs strictly on standard Python library modules (`http.server`, `threading`, `json`, `webbrowser`, etc.). No Flask, no FastAPI, no node_modules, no npm.
* 🛡️ **Local-Only Security:** Loops and binds exclusively to local loopback address `127.0.0.1` to prevent exposing local systems.
* 📦 **Stateless Layout Persistence:** Automatically saves your drags coordinates, custom panel dimensions, and compact staircase positions inside your browser profile (`localStorage`), keyed uniquely to your study's title. The Python backend remains 100% stateless and file-free.
* 📐 **Staircase Stacking Flow:** Serves columns in flex-rows that grow naturally. Highlights focus actively via `z-index` bubbling, and includes a **Compact ◫** staircase stacking button that automatically organizes panels by size.
* 📊 **Built-In High-Fidelity Components:**
  * **Interactive Tables:** Character-matching search filters, alphanumeric/percent column headers sorting, and click highlights that trigger dynamic callback cascades.
  * **SVG Candlestick Charts:** Computes coordinate bounds to draw wicks, candles, and transaction price overlays, complete with real-time hover price HUDs.
  * **Custom Scoped Panels:** Sandboxes bespoke HTML, scoped CSS variables, and custom JavaScript loops using safe functional constructors IIFE with automatic memory cleanup.

---

## Directory Structure

```
cascade/
├── setup.py                     # Standard module installer config
├── demo_study_config.py         # Workspace Trade Backtest Auditor study config
├── demo_system_study_config.py  # Workspace 4-Level Server Infrastructure study config
└── cascade/                     # Main Package Namespace
    ├── __init__.py              # Unified public API exports
    ├── __main__.py              # CLI router & templates bootstrapper
    ├── core.py                  # Loopback multi-threaded HTTP server, routes & decorators
    ├── table_render.py          # Table widget normalizer & formatters
    ├── candlestick_render.py    # Candlestick series charts coordinate parser
    ├── custom_render.py         # Scoped Custom panel wrapper (html, isolated css/js)
    ├── index.html               # SPA visual engine presentation shell
    └── templates/               # Packaged reusable template files
        ├── demo_study_config.py
        └── demo_system_study_config.py
```

---

## Installation

To install Cascade globally in your python environment (in editable mode so changes are reflected instantly):

1. Navigate to the root directory containing `setup.py`:
   ```bash
   pip install -e .
   ```

2. Once installed, you can launch a study configuration from *any* folder:
   ```bash
   python -m cascade <study_config_file>.py
   ```

---

## Quick Start

### 1. Initialize Starter Templates
To copy starter templates directly into your active working directory:
```bash
python -m cascade --init
```
This generates `demo_study_config.py` (Trading auditor) and `demo_system_study_config.py` (4-Level performance monitor) in your local folder to use as starting templates.

### 2. Run a Study Config
Start the server and automatically launch the visual workspace:
```bash
python -m cascade demo_study_config.py
```

---

## Basic Concept & Code Example

To build a cascade, create a Python configuration file that instantiates `Cascade`, registers a starting callback via `@app.root_panel()`, and registers deeper cascading steps using `@app.panel("callback_name")`. 

### `simple_study.py` Example:
```python
from cascade import Cascade, Table, CandlestickChart

# 1. Instantiate the workspace
app = Cascade(title="My Analytical Study", orientation="horizontal")

# Mock database records
COMPANIES_DATA = [
    {"Name": "TechCorp", "Sector": "Technology", "Price": 420.50},
    {"Name": "HealthCo", "Sector": "Healthcare", "Price": 185.20}
]

# 2. Define the starting Level 0 panel
@app.root_panel()
def show_companies():
    return Table(
        data=COMPANIES_DATA,
        title="Sectors Overview",
        on_click=show_market_history,  # Triggers show_market_history upon row click
        width="400px"
    )

# 3. Define the Level 1 cascade callback
@app.panel("show_market_history")
def show_market_history(clicked_row):
    company_name = clicked_row["Name"]
    base_price = float(clicked_row["Price"])
    
    # Generate mock daily candle list
    candles = [
        {"time": f"Day {i+1}", "open": base_price + i, "high": base_price + i + 2,
         "low": base_price + i - 1, "close": base_price + i + 1, "volume": 50000}
        for i in range(10)
    ]
    
    return CandlestickChart(
        data=candles,
        title=f"{company_name} - Historical Timeline",
        width="500px",
        height=250
    )
```
Run this config: `python -m cascade simple_study.py`. Clicking a company row in the Level 0 table will instantly slide open a Level 1 price candlestick chart beside it!

---

## Visual Shell UI Interaction Guidelines

* **Focusing Panels:** Click anywhere inside a panel card to bubble its `z-index` layer focus to the top.
* **Drags & Positions:** Drag panel headers to float translation coordinates. Refresh the page—positions are preserved safely inside the browser profile!
* **Resets:** Double-click any panel header handle to clear its coordinates cache and snap it back to standard grid flow.
* **Resizing:** Drag the bottom-right handles to resize cards lag-free. Candlestick SVG vector graphs automatically redraw to fit the new sizes.
* **Compact Staircase Stacking:** Click **Compact ◫** in the header. All active panels are measured, sorted in ascending order of visual area, and aligned in a staircase cascade starting with the smallest card.

---

## Core Technologies
* **Python Backend:** Standard library `http.server`, `threading`, `json`, `webbrowser`, `socket`, `importlib`.
* **Frontend UI Visual Shell:** HTML5, Vanilla CSS, Custom SVG generators, JavaScript (ES6+).
* **UI Typography:** Outfit (Headings) and JetBrains Mono (Auditing details).

---

## License
MIT License. Created by Advanced Agentic Coding teams.
