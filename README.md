# Integrated Data & Web Application Core (VReiraum & Analytics)

⚠️ **Project Status: Monorepo Prototype (Academic Thesis & Data Evaluation)**  
This repository bundles the full-stack ecosystem as a work in prgoress and a data processing pipeline. It is structured as a Monorepo to showcase the connection.

🛠️ **Tech Stack**
* **Backend:** Python (FastAPI / Django)
* **Frontend:** React
* **Data Processing:** Pandas / NumPy

---

## Repository Guide & Architecture

To help with code review, here is the roadmap to the most important components:

### 1. The Web Ecosystem
*   `/backend` – The functional FastAPI core logic where API routing and state management live.
*   `/dev_frontend_dev` – The environment where the React frontend was engineered, with a switch for "a simulated backend". *Note: Due to typical package-lock changes, this environment is tricky to replicate locally and is shared as-is*
*   `/old_frontend` – The folder supposed to house the static build files served by the backend architecture.

### 2. Data Processing Pipeline (Analytics Core)
*This section contains the data processing flow, which was kept in localized scripts due to acute academic time constraints towards the end of my thesis:*

*   `DataVisualisation/Clustering.py` & `DataVisualisation/walk_map.py` (Initial Exercise) – A playground script used to explore the mathematical data visualisation, before I had the requirements for my Paper and research about the appropriate visualization.
*   `DataVisualisation/dataChange/convert.py` Because of being young I choose a weird way to save data in C, with alternating lines having different meaning without a identifier. This reshaped these into one line csv files with a header.
*   `DataVisualisation/dataChange/main.py` (Visualization Engine) – The final core processing layer utilizing Pandas and NumPy to generate the heatmaps and clusters, even if the data layer was lacking do too being "early in my studies comparativly.

---

## Key Architectural Insights & Academic Evolution

*   **Pragmatic Under Pressure:** Faced with strict deadlines due to an delayed thesis review, I chose a decoupled execution strategy. The core data parsing and mathematical analysis loops were intentionally kept as local standalone pipelines to ensure rapid iteration over the data sets and finishing my studies.
*   **The Blueprint for Scale:** Although the data pipelines run independently from the web backend in this prototype, their modular design makes them direct candidates for injection as service layers into the `/backend` FastAPI environment.
