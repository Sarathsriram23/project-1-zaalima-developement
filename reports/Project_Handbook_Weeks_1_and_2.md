# Customer Churn Prediction & LTV Engine
## Detailed Project Handbook & Code Explanations (Weeks 1 & 2)

---

## 1. Project Overview & Team Structure

This handbook details the codebase, implementation pipeline, and individual responsibilities for the Customer Churn Prediction project. The project is structured across a 5-member team to deliver a robust Data Engineering, Data Analysis, and Machine Learning workflow. This volume focuses on Setup, Week 1 (Data Engineering & EDA), and Week 2 (Churn Modeling & SHAP Explainability).

### Team Allocations - Weeks 1 & 2

| Member Role | Week 1 Responsibilities | Week 2 Responsibilities |
| :--- | :--- | :--- |
| **Member 1: Data Engineer** | PostgreSQL Schema Setup; `db_connection.py` creation; `etl_pipeline.py` ingestion script. | Refactoring preprocessing; support model preprocessors (`preprocess.py`). |
| **Member 2: Data Analyst** | Jupyter EDA Notebook (`EDA.ipynb`); Business Insights Report (`business_insights.md`). | Evaluate model outputs; verify F1 and ROC AUC metrics; write presenter explanations. |
| **Member 3: ML Engineer** | Verify raw data structure; align schemas for machine learning input variables. | Model pipeline creation; model training (Logistic Regression, Random Forest, XGBoost); select best classifier. |
| **Member 4: SHAP Explainer** | Pre-modeling feature analysis; identify potential collinearity in correlation heatmap. | Calculate SHAP explainability values; generate global summary plots (`shap_explain.py`). |
| **Member 5: BI & Testing** | Setup dashboard data templates; outline database loading validation metrics. | Generate target prediction outputs; export `churn_predictions.csv`; prepare dashboard inputs. |

---

## 2. Week 1 Code & Component Explanations

### A. SQL Schema Setup (`sql/create_tables.sql` & `sql/load_data.sql`)
*   **Responsible**: Member 1 (Data Engineer)
*   **Description**: Sets up raw and cleaned relational structures in the PostgreSQL database.
*   **Code Logic**:
    *   Creates the `telco_customers` table with text/numeric types matching the CSV format. `TotalCharges` is imported as `VARCHAR` to allow blank space ingestion.
    *   Creates the `cleaned_telco_customers` table where `Churn` is mapped to `INTEGER` (0/1) and `TotalCharges` is parsed into `NUMERIC`.
    *   Specifies the `COPY` SQL command inside `load_data.sql` to ingest the local dataset.

### B. Database Connector Setup (`scripts/db_connection.py`)
*   **Responsible**: Member 1 (Data Engineer)
*   **Description**: Establishes a database engine using SQLAlchemy.
*   **Code Logic**:
    *   Attempts to build a PostgreSQL connection engine using variables: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_NAME`.
    *   Gracefully falls back to `sqlite:///customer_churn_db.sqlite` if connection fails (e.g. database offline during local dev).

### C. Data Ingestion Pipeline (`scripts/etl_pipeline.py`)
*   **Responsible**: Member 1 (Data Engineer)
*   **Description**: Implements Extract, Transform, and Load (ETL) mechanics.
*   **Code Logic**:
    1.  **Extract**: Loads raw CSV data into a Pandas DataFrame.
    2.  **Load Raw**: Saves raw records to table `telco_customers`.
    3.  **Transform**: Coerces `TotalCharges` to float, fills blanks with median, drops non-predictive `customerID`, maps `Churn` (`No`/`Yes`) to (`0`/`1`).
    4.  **Load Cleaned**: Saves processed rows to `cleaned_telco_customers` and writes `data/cleaned_telco.csv`.

### D. Exploratory Data Analysis (`notebooks/EDA.ipynb`)
*   **Responsible**: Member 2 (Data Analyst)
*   **Description**: Runs statistical inspections and generates visualization charts.
*   **Code Logic**:
    *   **Target Check**: Measures Churn class distribution (26.54% Churn vs 73.46% Retained).
    *   **Numeric Distributions**: Plots histplots for `tenure` (identifies onboarding spike) and monthly charges.
    *   **Relationship Bars**: Computes churn rate across Contract Type (month-to-month contracts have 42.71% churn) and Payment Method (Electronic check has 45.29% churn).
    *   **Heatmap**: Correlates numeric attributes, showing that tenure and Churn are negatively correlated (-0.35).

### E. Presentation Insights (`reports/business_insights.md`)
*   **Responsible**: Member 2 (Data Analyst)
*   **Description**: Summarizes insights and presentation speaking scripts for each graph.
*   **Contents**:
    *   Highlights major retention blockers (onboarding stage churn, high bills).
    *   **Speaking scripts**: Provides specific speaking points for the PPT slides to explain distributions, contract barriers, and payment friction.
    *   **Actions**: Recommends incentives for migrating users to auto-pay and long-term contracts.

---

## 3. Week 2 Code & Component Explanations

### A. Preprocessing Refactoring (`scripts/preprocess.py`)
*   **Responsible**: Member 1 (Data Cleaning & Preprocessing)
*   **Description**: Contains the standalone cleaning workflow to resolve file path dependencies.
*   **Code Logic**:
    *   Refactored the hardcoded local absolute paths into relative paths.
    *   Converts `TotalCharges` to numeric, handles blank fields, drops `customerID`, maps `Churn`, and outputs `data/cleaned_telco.csv`.

### B. Scoring Interface Setup (`scripts/evaluate_models.py`)
*   **Responsible**: Member 2 (Model Evaluation)
*   **Description**: Utility scoring code for consistent metrics computation.
*   **Code Logic**:
    *   Resolves the Git conflicts present in the initial templates.
    *   Defines an `evaluate()` function calculating: Accuracy, Precision, Recall, F1-Score, and ROC-AUC score.
    *   Returns the scores as a dictionary to facilitate model comparison.

### C. ML Pipeline Training (`scripts/train_churn.py`)
*   **Responsible**: Member 3 (ML Churn Model Development)
*   **Description**: Trains and compares 3 models to select the best predictor.
*   **Code Logic**:
    1.  **Feature Engineering**: Computes `AvgChargePerMonth` = `TotalCharges` / (`tenure` + 1).
    2.  **Pipeline Design**: Implements a Scikit-Learn Pipeline wrapping a `ColumnTransformer` (`OneHotEncoder` for object columns, `StandardScaler` for numeric columns) and the Classifier. This prevents data leakage during training.
    3.  **Splitting**: Stratifies the train-test split (80/20) to preserve target ratios.
    4.  **Inits**: Trains Logistic Regression, Random Forest, and XGBoost.
    5.  **Selection**: Evaluates test metrics. Logistic Regression is selected as the best overall classifier (F1: 0.6039, ROC AUC: 0.8473) and saved as `models/churn_model.pkl`.
    6.  **Prediction Export**: Saves `data/churn_predictions.csv` containing probabilities for dashboard usage.

### D. SHAP Explainability Script (`scripts/shap_explain.py`)
*   **Responsible**: Member 4 (SHAP Explainability)
*   **Description**: Quantifies individual feature impact on model decisions.
*   **Code Logic**:
    *   Loads `models/churn_model.pkl` and the cleaned dataset.
    *   Extracts features and transforms them using the pipeline's preprocessor.
    *   Obtains post-encoding feature names (e.g. `Contract_One year`, `PaymentMethod_Electronic check`).
    *   Instantiates `shap.Explainer`, calculates SHAP values, and saves a summary plot to `reports/shap_summary_plot.png`.

### E. Predictions Dataset Generation (`data/churn_predictions.csv`)
*   **Responsible**: Member 5 (Testing & Dashboard Dataset)
*   **Description**: Exports the predictions dataset containing probabilities.
*   **Code Logic**:
    *   Created during the execution of `train_churn.py`.
    *   Concatenates test set features with `ActualChurn`, `PredictedChurn`, and `ChurnProbability`.
    *   Used directly as input for BI tools (Metabase, PowerBI) to analyze customer churn risk levels.
