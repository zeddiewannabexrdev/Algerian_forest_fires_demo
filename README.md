# Algerian Forest Fire Analytics & Early Warning Workstation `v1.0.0`

An end-to-end decision-support and climate-simulation workstation for wildfire risk prediction, built on the Algerian Forest Fires Dataset (2012). The system incorporates dual machine-learning engines: **Decision Tree** and **Random Forest**, balancing intuitive decision explainability with robust predictive accuracy.

---

## 1. Project Overview

The project models and analyzes meteorological and fire risk observations across two distinct bioclimatic zones in northern Algeria:
- **Bejaia Region**: A humid/sub-humid northeastern coastal region regulated by Mediterranean sea breezes and higher atmospheric moisture.
- **Sidi-Bel Abbes Region**: A semi-arid northwestern interior plateau characterized by high summer temperatures, low relative humidity, and dry wind regimes.

### Dataset Specifications
- **Total Records**: 244 daily observation instances (122 from Bejaia, 122 from Sidi-Bel Abbes).
- **Observation Period**: June 2012 through September 2012.
- **Feature Categories**:
  - *In-situ Meteorological Indices*: Temperature (°C), Relative Humidity (RH, %), Wind Speed (Ws, km/h), Precipitation (Rain, mm).
  - *Canadian Forest Fire Weather Index (FWI) System*:
    - **FFMC** (Fine Fuel Moisture Code): Moisture content of surface litter and fine fuels.
    - **DMC** (Duff Moisture Code): Moisture content of loosely compacted decomposing organic layers.
    - **DC** (Drought Code): Deep organic layer moisture content and root-level dryness.
    - **ISI** (Initial Spread Index): Expected rate of fire spread without fuel buildup effects.
    - **BUI** (Buildup Index): Total fuel volume available for active combustion.
    - **FWI** (Fire Weather Index): Comprehensive numerical rating of fire intensity.

---

## 2. Directory Architecture

```text
TTCS/
|-- data/
|   `-- Algerian_forest_fires_dataset_UPDATE.csv   # Cleaned source dataset
|-- models/
|   |-- __init__.py                               # Package exports for machine learning modules
|   |-- decision_tree_model.py                    # Pruned Decision Tree & If-Else rule extractor
|   |-- random_forest_model.py                    # Random Forest ensemble & consensus analyzer
|   `-- model_evaluator.py                        # Benchmark matrix, Confusion Matrix, ROC-AUC
|-- views/
|   |-- __init__.py                               # Package exports for functional views
|   |-- alert_view.py                             # Module 1: Real-time wildfire hazard alert
|   |-- climate_view.py                           # Module 2: Climate simulation & 2D transition phase
|   |-- regional_view.py                          # Module 3: Comparative regional analysis
|   |-- seasonal_view.py                          # Module 4: Seasonal risk tracking & DC buildup
|   `-- explainability_view.py                    # Module 5: Feature importances & tree rules
|-- .streamlit/
|   `-- config.toml                               # Streamlit server & runtime configuration
|-- .vscode/
|   `-- settings.json                             # VS Code Python environment & linter settings
|-- app.py                                        # Main Streamlit workstation entry point
|-- config.py                                     # System configurations, color palettes, risk thresholds
|-- data_loader.py                                # Data ingestion, cleaning, and preprocessing
|-- pyrightconfig.json                            # Pyright/Pylance path & diagnostic settings
|-- requirements.txt                              # Python package dependencies
|-- run_app.bat                                   # 1-click Windows application launcher
|-- setup_env.bat                                 # 1-click virtual environment setup script
|-- test_pipeline.py                              # Automated unit test suite
|-- .gitignore                                    # Production git ignore configuration
`-- README.md                                     # Project technical documentation
```

---

## 3. System Prerequisites

- **Python**: Version 3.10 or higher (Python 3.10 or 3.11 recommended).
- **Git**: Version 2.30 or higher.
- **Web Browser**: Chrome, Edge, Firefox, or Safari supporting HTML5 and WebGL.
- **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+).

---

## 4. Installation and Execution

### Method 1: Fast Launch on Windows (Recommended)

For Windows systems with Python installed, utilize the pre-configured automated batch scripts:

1. **Step 1: Create virtual environment and install packages**
   Double-click `setup_env.bat` or execute in Terminal:
   ```cmd
   setup_env.bat
   ```
   This script automatically initializes a `.venv` virtual environment and installs all dependencies from `requirements.txt`.

2. **Step 2: Start the application**
   Double-click `run_app.bat` or execute in Terminal:
   Your default web browser will open automatically at: `http://localhost:8501`.

3. **Step 3: Run as a Standalone Desktop Application (No browser tabs)**
   Run `desktop_app.py` directly:
   ```cmd
   python desktop_app.py
   ```
   This launches the software inside a clean, dedicated desktop application window without browser URL bars or navigation buttons.

---

### Method 2: Building Standalone Windows Executable (.exe)

To bundle the entire project into a standalone `.exe` desktop application for distribution:

1. Double-click `build_exe.bat` or execute in Terminal:
   ```cmd
   build_exe.bat
   ```
2. Upon build completion, the executable package will be generated at:
   ```text
   dist/ForestFireWorkstation/ForestFireWorkstation.exe
   ```
   You can distribute this folder to any Windows 10/11 machine.

---

### Method 3: Manual Installation (Cross-Platform)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zeddiewannabexrdev/Algerian_forest_fires_demo.git
   cd Algerian_forest_fires_demo
   ```

2. **Create and activate a virtual environment:**
   - On Windows (Command Prompt / PowerShell):
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Upgrade pip and install dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit workstation:**
   ```bash
   streamlit run app.py
   ```
   Access the dashboard at the displayed local URL:
   ```text
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

---

## 5. Automated Unit Testing

The repository includes a comprehensive unit test suite covering data preprocessing, model training, feature calculation, and rule extraction. Run tests with:

```bash
python test_pipeline.py
```

Standard expected output:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.200s

OK
```

Test coverage includes:
1. `test_data_loader_shape_and_clean`: Verifies dataset completeness (244 rows, 15 columns, zero null values, corrected UCI delimiter offsets).
2. `test_decision_tree_manager`: Validates Decision Tree training, prediction, and probability outputs.
3. `test_random_forest_manager`: Verifies Random Forest training, OOB score availability, and tree agreement consensus calculations.
4. `test_model_evaluator`: Validates stratified 80/20 train/test evaluation, confusion matrices, and ROC metrics.
5. `test_rule_extraction`: Validates natural-language rule extraction and probability mapping from leaf nodes.

---

## 6. Workstation Functional Modules

### Module 1: Real-Time Hazard Monitoring & Alert Directives
- Ingests in-situ weather metrics (Temperature, RH, Wind Speed, Rain) and FWI indices via interactive controls or historical presets.
- Computes independent ignition probabilities using both Decision Tree and Random Forest.
- Aggregates risk through equal ensemble weighting into 4 standardized threat levels:
  - *Level 1 - Low* (Score: 0.00 - 0.25): Baseline patrolling.
  - *Level 2 - Moderate* (Score: 0.25 - 0.50): Increased inspection frequency and burn permits suspension.
  - *Level 3 - High* (Score: 0.50 - 0.75): 24/7 watchtower vigilance and emergency response staging.
  - *Level 4 - Extreme* (Score: 0.75 - 1.00): State of emergency mobilization and community evacuation.

### Module 2: Climate Scenario Simulation & 2D Transition Phase
- Simulates extreme meteorological events (Standard Summer, El Niño Heatwave, IPCC RCP 8.5 2050 Warming, Cooling Rain Storm).
- Renders temperature sensitivity curves (20°C to 45°C) comparing Decision Tree step responses with Random Forest continuous curves.
- Constructs 2D ignition phase-boundary matrices (Temperature vs. Relative Humidity) using Vectorized Batch Prediction for sub-second rendering.

### Module 3: Regional Comparative Analytics
- Side-by-side contrast between Bejaia (Coastal) and Sidi-Bel Abbes (Inland).
- Normalized 6-axis Radar Profile across Canadian FWI indices.
- Distribution boxplots for individual meteorological metrics conditioned on actual fire occurrence.
- Monthly fire day distribution and rate differentials.

### Module 4: Seasonal Risk Tracking & Drought Accumulation
- Continuous temporal trajectory across the 4-month observational window (June - September 2012).
- Tracks deep organic Drought Code (DC) accumulation, explaining peak fire risk concentration in August.
- Daily risk calendar heatmap mapping historical fire patterns.

### Module 5: Algorithm Explainability & Inference Rules
- Multi-metric benchmark matrix (Accuracy, Precision, Recall, F1-Score, ROC-AUC).
- Side-by-side Gini feature importance comparisons between greedy axis-aligned splits (DT) and feature-subsampling ensemble distributions (RF).
- Full Decision Tree architectural diagram with zoom/pan capabilities.
- Human-readable If-Else rule inspector with sample counts, confidence ratings, and condition filtering.

---

## 7. Display Themes (Dark & Light Mode)

The workstation features a theme switcher in the control sidebar:
- **Dark Mode**: High-contrast command-center aesthetic using deep slate tones (`#0b0f19`, `#131b2e`), hairline borders (`#2d3748`), and high-readability text (`#f8fafc`).
- **Light Mode**: Clean laboratory workstation aesthetic using neutral off-white surfaces (`#ffffff`, `#f8fafc`), crisp boundaries (`#cbd5e1`), and high-contrast charcoal text (`#090d16`).

All Plotly and Matplotlib visualizations automatically synchronize backgrounds, axes, grid lines, and labels with the active theme.

---

## 8. Dependencies and Frameworks

| Package | Minimum Version | Purpose |
| :--- | :--- | :--- |
| `streamlit` | >= 1.28.0 | High-density desktop workstation application interface |
| `pandas` | >= 2.0.0 | Tabular dataset manipulation, cleaning, and aggregation |
| `numpy` | >= 1.24.0 | Vectorized numerical computation and 2D grid generation |
| `scikit-learn` | >= 1.3.0 | Decision Tree and Random Forest classification and evaluation |
| `plotly` | >= 5.15.0 | Interactive charts: Gauges, Radar, Contours, Boxplots, ROC curves |
| `matplotlib` | >= 3.7.0 | High-resolution Decision Tree diagram rendering |
