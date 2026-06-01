# Cascade Packaging & CLI Architecture Implementation Plan (Declarative Pseudocode Edition)

This plan outlines the restructuring of the **Cascade** framework into a declarative, modular package. Instead of standard Python code (`.py`), the codebase will be written in **Cascade Declarative Pseudocode (CDP)** using the `.psc` file extension. The SPA frontend (`index.html`) will be written in standard, fully implemented HTML/CSS/JS, as it does not require pseudocode.

The goal is to provide highly detailed, compact, yet zero-fidelity-loss architectural specifications and steps so that any AI engine can perfectly generate the final operational codebase from this framework.

---

## 1. Meta-Definition of Cascade Declarative Pseudocode (CDP)

CDP is a domain-specific, highly declarative pseudocode designed to specify Python-based web servers, dynamic loading systems, data converters, and user templates with absolute logical precision and minimal syntax clutter.

### CDP Syntax Rules & Keywords

#### A. Modules & Dependencies
* `MODULE <name>`: Establishes the current file's namespace.
* `IMPORT <library>`: Imports a standard module.
* `FROM <library> IMPORT <names>`: Imports specific members from a library.

#### B. Class & Object Definitions
* `CLASS <Name> [INHERITS <Parent>]:`: Declares a class structure.
* `CONSTRUCTOR(<params>):`: Declares the initialization block.
* `FIELD <name> [= <default>]`: Declares a class-level or instance-level property.
* `METHOD <name>(<params>) [-> <return_type>]:`: Declares an instance routine.

#### D. Functions & Decorators
* `DECORATOR <name>(<params>):`: Defines a functional decorator wrapper.
* `FUNC <name>(<params>) [-> <return_type>]:`: Defines a standard routine.
* `<@decorator>`: Applies a decorator to a function.

#### E. Highly Declarative Control Flows
* `IF <condition> THEN <expression> [ELSE <expression>]` (support for both inline and block formats).
* `FOR EACH <item> IN <collection> DO:`: Loop iterator.
* `MATCH <value> WITH:`: Pattern matching control block:
  ```
  MATCH value WITH:
      CASE <pattern_1> => <action_1>
      CASE <pattern_2> => <action_2>
      CASE _ => <default_action>
  ```

#### F. Local Web Services & Routing
* `ROUTE <path> [<HTTP_METHOD>]:`: Declares an HTTP server router endpoint mapping.
  - `INPUT:` Maps expected HTTP requests, headers, or query parameters.
  - `PROCESS:` Core server logical routines.
  - `RESPONSE:` Returns payload format (e.g. `JSON`, `HTML`, or `HEADER`).
* `START_SERVER(host, port, handler)`: Synthesizes multi-threaded HTTP server execution.
* `OPEN_BROWSER(url)`: Triggers host system default web browser.

#### G. Core Operations & Formatters
* `NORMALIZE_DATA(raw)`: Standardizes various data inputs (lists of dicts, lists of lists, DataFrames) into uniform list-of-dictionary records.
* `PARSE_PATH(path)`: Dynamically resolves file path variables.
* `COMPILER_IIFE(html, js, css, data)`: Bundles custom markup and isolates JS operations inside local container queries.

---

## 2. Directory Layout & Proposed Changes

All Python components are specified as `.psc` files. The frontend SPA and layout JSON specs remain as actual files.

```
c:\Projects\gemini\cascade\
├── setup.psc                     # Declarative installer configuration
└── cascade/                     # Main Package Namespace
    ├── __init__.psc              # Re-exports clean public API
    ├── __main__.psc              # CLI Router & Initializer
    ├── core.psc                  # Framework core runner & HTTP server
    ├── table_render.psc          # Table data formatter
    ├── candlestick_render.psc    # Candlestick parser
    ├── custom_render.psc         # Custom IIFE panel wrapper
    ├── index.html               # Frontend SPA (Full standard HTML/CSS/JS)
    └── templates/               # Config Templates
        ├── demo_study_config.psc # Trading Backtest Study template
        └── demo_system_study_config.psc # 4-Level Server Performance template
```

---

## 3. Implementation Specifications (.psc Files)

### A. Library Packaging Config
#### [NEW] [setup.psc](file:///c:/Projects/gemini/cascade/setup.psc)
Declarative setup configurations providing metadata, target paths, and instructions to package and copy `index.html` and `templates/*.psc` as critical non-Python assets.

### B. Core Library Package (`cascade/`)

#### [NEW] [__init__.psc](file:///c:/Projects/gemini/cascade/cascade/__init__.psc)
Re-exports clean API namespace: `Cascade`, `Table`, `CandlestickChart`, `CustomPanel`, `format_currency`, `format_percent`.

#### [NEW] [__main__.psc](file:///c:/Projects/gemini/cascade/cascade/__main__.psc)
Implements CLI Argument Router:
- If `--init` or `-i`: Resolves local package templates directory and copies all `.psc` templates to current working directory, printing instructions.
- If file path specified: Dynamically imports using `importlib.util`. Resolves the active `Cascade` instance inside the imported namespace and runs the server.

#### [NEW] [core.psc](file:///c:/Projects/gemini/cascade/cascade/core.psc)
Implements the central framework engine:
- `Cascade` class containing constructors for `title`, `orientation`.
- Sets class variable `Cascade.active_instance = SELF`.
- Exposes decorators `@root_panel` and `@panel(name)`.
- Threaded loopback server binding exclusively to `127.0.0.1`.
- Aggressive cache-control headers (`Pragma`, `Expires`, `Cache-Control`).
- Endpoints:
  - `GET /`: Injects and serves `index.html`.
  - `GET /api/layout`: Returns title, orientation, and browser profile persistence indicators.
  - `POST /api/callback`: Resolves arguments, executes designated callback, and returns JSON serialization of the widget (Table, Chart, Custom).

#### [NEW] [table_render.psc](file:///c:/Projects/gemini/cascade/cascade/table_render.psc)
Handles table widget building:
- Normalizes rows from dicts, lists, or DataFrames.
- Implements `format_currency` and `format_percent` cell decorators.

#### [NEW] [candlestick_render.psc](file:///c:/Projects/gemini/cascade/cascade/candlestick_render.psc)
Structures candlestick series data:
- Prepares `time`, `open`, `high`, `low`, `close`, `volume`, `entry_target`, and `exit_target` values into compliant charts dictionaries.

#### [NEW] [custom_render.psc](file:///c:/Projects/gemini/cascade/cascade/custom_render.psc)
Encapsulates HTML/JS/CSS scopes and raw data states into a custom renderer model.

### C. Visual Engine SPA
#### [NEW] [index.html](file:///c:/Projects/gemini/cascade/cascade/index.html)
*(Standard HTML File—No Pseudocode Required)*
Fully implemented Obsidian-dark SPA. Key mechanics:
1. **Style System:** outfits and JetBrains Mono typography, slate grey opaque cards `#0f1422`, cyan/emerald/red accents.
2. **Flex Grid Stacking:** no-compression cards using `flex-shrink: 0`, expanding naturally vertically/horizontally without overflow clippping.
3. **Focus Click Z-Ordering:** mouse bubbling to assign `z-index: 100` to active card, `10` to siblings.
4. **Drag Coordinates Persistence:** Header mouse handles modifying CSS `translate(x, y)` transform. Anim-lock releases by clearing `animation` inline property. Persists coordinate arrays to `localStorage` (browser profile) keyed by workspace title.
5. **Interactive Drag-Resizing:** Lag-free sizing disabling CSS transition animations temporarily. Auto-triggers SVG redraws.
6. **Staircase Stack Compactness:** Computes visual areas, sorts in ascending order, projects `TargetX = i * 35px`, `TargetY = i * 35px`, where slot 0 is the smallest card. Sets translates and saves to browser profile database.
7. **Widgets Renders:**
   - **Table:** Real-time column search filtering, numeric/string header sorting with visual indicators, row highlight triggering deep callback API requests (clearing downstream columns $N+1$).
   - **Candlestick SVG:** Translates data bounds into SVG paths. Renders volume bars, bullish bodies in green, bearish in red. Horizontal target wicks labeled on Y-axis. Implements real-time mono-font HUD tracker. Resizes SVG elements automatically upon parent card dimensions modifications.
   - **Custom IIFE compiler:** Injects scripts. Instantiates script sandbox with functional constructors: `new Function("container", "data", code)(element, payload)`. Cleans up old container intervals before executing new ones using `container.dataset.intervalId`.

### D. Study Config Templates (`cascade/templates/`)

#### [NEW] [demo_study_config.psc](file:///c:/Projects/gemini/cascade/cascade/templates/demo_study_config.psc)
Declarative Trading auditor study config showing off table formats, target candles, and custom JS intervals.

#### [NEW] [demo_system_study_config.psc](file:///c:/Projects/gemini/cascade/cascade/templates/demo_system_study_config.psc)
Declarative 4-level server performance study config starting with candlestick, cascading to node tables, process listings, and simulated thread stacktraces.

---

## 4. Verification Plan

### Automated/Local Execution Tests

How to initialize and run the pseudocode configurations:

#### 1. Initializing Templates in Your Directory
```powershell
python -m cascade --init
```
*   CLI processes templates copying, generating starter configurations in current working folder.

#### 2. Translation & Running
Since these files are written in declarative pseudocode (`.psc`), we verify that the logical transitions have 100% fidelity.
*   Confirm `index.html` loads and parses all custom panels, SVGs, intervals, Z-Index stacking, and Compact layouts.
*   Verify that double-clicking clears `localStorage` and falls back directly to default sizes from the study configuration files.
