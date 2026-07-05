# Customer Churn Prediction & Customer Lifetime Value (LTV) Engine

An end-to-end Data Engineering, Machine Learning, and Business Intelligence platform built to predict customer churn risk and estimate Customer Lifetime Value (LTV) for telecom operations. 

---

## 🚀 Project Overview & Architecture
This platform is structured to ingest customer billing history, run ETL cleaning pipelines, train optimized predictive classifiers and regressors, expose predictions via a FastAPI REST API, and visualize retention metrics in Metabase.

```
       [Raw CSV Data]
             │
             ▼
     [etl_pipeline.py] ───► [PostgreSQL Database] (Fallback: SQLite)
             │
             ▼
      [ML Pipelines] (OneHot + StandardScaler + FeatureEngineer)
      ├── Churn Classification Model: XGBoost (F1: 0.6307, Recall: 81.28%)
      └── LTV Regression Model: Random Forest Regressor (R²: 0.9992, MAE: $40.79)
             │
             ▼
     [FastAPI REST API] ───► Swagger Docs (/docs)
             │
             ▼
   [Metabase BI Tool] ───► KPI Dashboards
             │
             ▼
     [Docker Compose] (Single command deployment)
```

---

## 📁 Repository Structure
```
├── api/
│   ├── database.py         # SQLAlchemy DB connection helper & fallback session manager
│   ├── main.py             # FastAPI server with model loading and predictions
│   └── schemas.py          # Pydantic request/response schemas
├── data/
│   ├── cleaned_telco.csv   # Preprocessed clean dataset
│   └── churn_predictions.csv # Test set predictions for Metabase imports
├── docker/
│   └── Dockerfile          # Syllabus container layout
├── models/
│   ├── churn_model.pkl     # Serialized best churn pipeline (XGBoost)
│   └── ltv_model.pkl       # Serialized best LTV pipeline (Random Forest)
├── notebooks/
│   └── EDA.ipynb           # Exploratory Data Analysis & visual charts
├── reports/
│   ├── business_insights.md # Storytelling insights from EDA graphs
│   ├── ltv_analysis.md     # Revenue analysis per contract/payment methods
│   ├── shap_summary_plot.png # Explainable AI feature summary plot
│   └── churn_distribution.png # Distribution visual
├── scripts/
│   ├── custom_transformers.py # Pipeline FeatureEngineer class
│   ├── db_connection.py    # Database connection creator
│   ├── etl_pipeline.py     # Ingests and cleans CSV data
│   ├── evaluate_models.py  # Model scoring metric utilities
│   ├── preprocess.py       # Standalone dataset cleaner
│   ├── run_eda_plots.py    # Generates EDA images using Matplotlib
│   ├── shap_explain.py     # Calculates SHAP values
│   └── train_churn.py      # Grid-search classifier model trainer
├── sql/
│   └── create_tables.sql   # Relational database schema table definitions
├── Dockerfile              # Root container build instructions
├── docker-compose.yml      # Multi-container orchestration (FastAPI + PostgreSQL + Metabase)
└── requirements.txt        # Python dependency manifest
```

---

## 🛠️ Local Installation & Run Guide

### Option A: Running Containerized via Docker Compose (Recommended)
Ensure **Docker Desktop** is running, then execute:
```cmd
docker-compose up --build -d
```
*   **FastAPI endpoints (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Metabase BI Platform**: [http://localhost:3000](http://localhost:3000)

### Option B: Running Locally (Manual Setup)
1.  **Install dependencies**:
    ```cmd
    pip install -r requirements.txt
    ```
2.  **Run Ingestion (ETL Pipeline)**:
    ```cmd
    python scripts/etl_pipeline.py
    ```
3.  **Train Machine Learning Models**:
    ```cmd
    python scripts/train_churn.py
    python scripts/train_ltv.py
    ```
4.  **Start REST API Server**:
    ```cmd
    python -m uvicorn api.main:app --reload
    ```
    Access the Swagger interactive UI at `http://127.0.0.1:8000/docs`.

---

## 🌐 FastAPI REST Endpoints Description
*   `POST /predict_churn`: Ingests customer payload and returns churn classification (0 = Retained, 1 = Churn) and risk probability.
*   `POST /predict_ltv`: Returns predicted lifetime value in USD.
*   `POST /predict_all`: Returns stacked churn and LTV predictions.
*   `GET /predict_customer/{customer_id}`: Queries a customer row by ID directly from the database, feeds their features into the ML pipelines, and returns predictions.

---

## 👥 Team Allocations & Contributions
*   **Member 1 (Data Engineer)**: Schema setups, `db_connection.py`, `etl_pipeline.py` ingestion, Docker configurations, and multi-container docker-compose network.
*   **Member 2 (Data Analyst)**: Jupyter EDA Notebook, `business_insights.md` report, and LTV segment analysis.
*   **Member 3 (ML Engineer)**: Standalone preprocessing utility `preprocess.py`, classifier cross-validation training, regressor training pipeline (`train_ltv.py`), and model metric comparison.
*   **Member 4 (API Developer)**: FastAPI REST backend framework, lifespan model loaders, and endpoint controllers.
*   **Member 5 (BI & Deployment)**: Dashboard query layouts, Metabase connection pipelines, and README documentation.
