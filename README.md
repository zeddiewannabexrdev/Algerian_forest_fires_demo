# Algerian Forest Fire Analytics & Early Warning Workstation `v1.0.0`

An end-to-end decision-support and climate-simulation workstation for wildfire risk prediction, built on the Algerian Forest Fires Dataset (2012). The system incorporates dual machine-learning engines: **Decision Tree** and **Random Forest**, balancing intuitive decision explainability with robust predictive accuracy.

---

## 1. Project Overview

The system models and analyzes meteorological and fire risk observations across two distinct bioclimatic zones in northern Algeria:
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
|   `-- Algerian_forest_fires_dataset_UPDATE.csv   # Source dataset (244 records, 2 regions)
|-- models/
|   |-- __init__.py                               # Package exports for machine learning modules
|   |-- decision_tree_model.py                    # Pruned Decision Tree classifier & rule extractor
|   |-- random_forest_model.py                    # Random Forest ensemble & consensus analyzer
|   `-- model_evaluator.py                        # Stratified benchmark matrix, ROC-AUC, Confusion Matrix
|-- views/
|   |-- __init__.py                               # Package exports for UI view modules
|   |-- alert_view.py                             # Module 1: Real-time hazard monitoring & alert directives
|   |-- climate_view.py                           # Module 2: Climate simulation & 2D transition phase boundary
|   |-- regional_view.py                          # Module 3: Comparative regional analytics & FWI radar
|   |-- seasonal_view.py                          # Module 4: Seasonal risk tracking & DC drought buildup
|   `-- explainability_view.py                    # Module 5: Gini feature importances & tree rule inspector
|-- docs/
|   |-- Tai_Lieu_Thiet_Ke_Va_Huong_Dan_He_Thong.docx # Comprehensive Word engineering documentation
|   `-- generate_docs.py                          # Automated docx document generator script
|-- .streamlit/
|   `-- config.toml                               # Streamlit server & runtime configuration
|-- .vscode/
|   `-- settings.json                             # VS Code Python workspace settings
|-- app.py                                        # Main Streamlit workstation application entry point
|-- config.py                                     # System configurations, typography, and risk thresholds
|-- data_loader.py                                # Data ingestion, cleaning, and preprocessing pipeline
|-- desktop_app.py                                # Standalone native desktop window runner (Edge/Chrome)
|-- pyrightconfig.json                            # Pyright/Pylance diagnostic configuration
|-- requirements.txt                              # Python package dependencies
|-- test_pipeline.py                              # Automated unit test suite (5 test cases)
|-- .gitignore                                    # Production git ignore configuration
`-- README.md                                     # Project technical documentation
```

---

## 3. System Prerequisites

- **Python**: Version 3.10 or higher (Python 3.10 or 3.11 recommended).
- **Git**: Version 2.30 or higher.
- **Web Browser**: Microsoft Edge, Google Chrome, Mozilla Firefox, or Apple Safari supporting HTML5 and WebGL.
- **Operating System**: Windows 10/11 (64-bit), macOS (12+), or Linux (Ubuntu 20.04+).

---

## 4. Installation and Execution

### Method 1: Running from Source (Cross-Platform)

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

3. **Install dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit workstation:**
   ```bash
   streamlit run app.py
   ```
   Access the dashboard at: `http://localhost:8501`.

5. **Optional: Run in Standalone Desktop Window Mode:**
   To run the software in a clean desktop application window without browser URL bars or navigation buttons:
   ```bash
   python desktop_app.py
   ```

---

### Method 2: Pre-compiled Windows Standalone Application (No Python Required)

For deployment to field stations or workstations without a Python runtime:

1. Download `ForestFireWorkstation-v1.0.0-windows-x64.zip` from the **[GitHub Releases](https://github.com/zeddiewannabexrdev/Algerian_forest_fires_demo/releases)** section.
2. Extract the `.zip` archive to a local directory.
3. Double-click `ForestFireWorkstation.exe`.

---

## 5. Automated Unit Testing

The repository includes a comprehensive unit test suite covering data ingestion, model fitting, feature calculations, and rule extraction. Execute the suite with:

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

Test coverage details:
1. `test_data_loader_shape_and_clean`: Verifies dataset completeness (244 rows, 15 columns, zero missing values, whitespace stripping, and UCI delimiter normalization).
2. `test_decision_tree_manager`: Validates Decision Tree training, binary prediction, probability outputs, and leaf node constraints.
3. `test_random_forest_manager`: Verifies Random Forest ensemble training, probability estimation, and tree agreement consensus calculations.
4. `test_model_evaluator`: Validates stratified 80/20 train/test evaluation, confusion matrix generation, and ROC-AUC metrics.
5. `test_rule_extraction`: Validates natural-language rule extraction, confidence scores, and sample coverage mapping from leaf nodes.

---

## 6. Workstation Functional Modules

### Module 1: Real-Time Hazard Monitoring & Alert Directives
- Accepts in-situ meteorological metrics (Temperature, RH, Wind Speed, Rain) and FWI indices via interactive slider controls or historical record presets.
- Computes independent ignition probabilities using both Decision Tree and Random Forest engines.
- Combines risk probabilities into a unified Gauge Indicator (0 - 100%) mapped to 4 operational threat levels:
  - *Level 1 - Low* (Score: 0.00 - 0.25): Baseline patrolling; maintain routine public fire-safety awareness.
  - *Level 2 - Moderate* (Score: 0.25 - 0.50): Increased inspection frequency; suspend open burning permits.
  - *Level 3 - High* (Score: 0.50 - 0.75): 24/7 watchtower vigilance; stage rapid-response equipment at forest margins.
  - *Level 4 - Extreme* (Score: 0.75 - 1.00): State of emergency; coordinate multi-agency resources and prepare community evacuations.

### Module 2: Climate Scenario Simulation & 2D Transition Phase
- Simulates pre-configured meteorological scenarios: Standard Summer, El Niño Heatwave (+5°C, -35% RH), IPCC RCP 8.5 2050 Warming (+3°C, -15% RH), and Cooling Rain Storm (10mm, -4°C).
- Generates continuous temperature sensitivity curves (20°C to 45°C) contrasting the orthogonal step response of Decision Tree against the smooth transition curve of Random Forest.
- Computes 2D ignition phase-boundary matrices (Temperature vs. Relative Humidity) using vectorized batch prediction.

### Module 3: Regional Comparative Analytics
- Contrast analysis between coastal Bejaia and inland Sidi-Bel Abbes across all metrics.
- Normalized 6-axis Radar Profile comparing Canadian FWI indices between regions.
- Distribution boxplots for individual environmental parameters conditioned on actual fire occurrence.
- Historical monthly fire-day frequency and rate differentials.

### Module 4: Seasonal Risk Tracking & Drought Accumulation
- Continuous temporal trajectory across the 4-month observational window (June - September 2012).
- Traces deep organic Drought Code (DC) accumulation, explaining why wildfire intensity peaks in August despite similar ambient temperatures to July.
- Daily risk calendar heatmap mapping historical fire patterns across each day of the season.

### Module 5: Algorithm Explainability & Inference Rules
- Multi-metric benchmark matrix comparing Decision Tree and Random Forest (Accuracy, Precision, Recall, F1-Score, ROC-AUC).
- Gini feature importance analysis showing greedy root-node concentration (ISI in Decision Tree) versus distributed weighting (FFMC, Temperature, FWI in Random Forest).
- Interactive Decision Tree architectural diagram visualizing tree depth and splits.
- Human-readable If-Else rule inspector with sample counts, confidence ratings, and condition filtering.

---

## 7. Machine Learning Performance Benchmark

Evaluated on an independent 20% stratified test set (49 instances):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Decision Tree (CART)** | 93.9% | 93.8% | 96.8% | 95.2% | 0.963 |
| **Random Forest (100 Trees)** | 98.0% | 96.9% | 100.0% | 98.4% | 0.998 |

*Key Forestry Insight*: Random Forest achieves 100.0% Recall on the test set with zero False Negatives, ensuring no critical wildfire ignition events are overlooked.

---

## 8. UI/UX Design and Typography Standards

The application adheres to a high-density, professional workstation aesthetic:
- **Dual-Theme Engine**:
  - *Dark Mode*: High-contrast operational palette with deep slate surfaces (`#0b0f19`, `#131b2e`), muted borders (`#2d3748`), and clean text (`#f8fafc`).
  - *Light Mode*: Clean laboratory palette with off-white backgrounds (`#f8fafc`, `#ffffff`), subtle borders (`#cbd5e1`), and high-contrast text (`#090d16`).
- **Typography Hierarchy**:
  - *Headings & Navigation Tabs*: **SF Pro Display** / **Montserrat** (`'SF Pro Display', 'SF Pro Text', 'Montserrat', sans-serif`).
  - *Body Text & Controls*: **Lato** (`'Lato', 'Segoe UI', Roboto, sans-serif`).
  - *Telemetry & Metrics*: **Consolas** / **Monospace** (`Consolas, 'Courier New', monospace`).
- Automatic synchronization across all Plotly interactive figures and Matplotlib diagrams.

---

## 9. Dependencies and Frameworks

| Package | Minimum Version | Purpose |
| :--- | :--- | :--- |
| `streamlit` | >= 1.28.0 | High-density analytical dashboard and UI component framework |
| `pandas` | >= 2.0.0 | Tabular dataset manipulation, cleaning, and aggregation |
| `numpy` | >= 1.24.0 | Vectorized numerical operations and 2D grid matrix generation |
| `scikit-learn` | >= 1.3.0 | Decision Tree and Random Forest classification and evaluation |
| `plotly` | >= 5.15.0 | Interactive charting: Gauges, Radar, Contours, Boxplots, ROC curves |
| `matplotlib` | >= 3.7.0 | High-resolution Decision Tree architectural diagram rendering |
| `python-docx` | >= 1.1.0 | Technical report and engineering documentation generation |
