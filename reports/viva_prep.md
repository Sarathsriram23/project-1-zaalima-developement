# Project Viva & Presentation Preparation Guide
**Prepared by**: Member 3 (ML Engineer) & Member 5 (Deployment Engineer)

Use this document to prepare for questions your guide or external examiners might ask during the final project evaluation.

---

## 📘 1. Data Engineering & Database Architecture

### Q1: Why did you implement a database fallback mechanism (PostgreSQL to SQLite)?
*   **Answer**: *"In a real-world enterprise setup, database connections might fail due to network disconnections, credentials updates, or local server maintenance. Hardcoding a single database link would crash our entire ingestion pipeline and FastAPI REST endpoints. We implemented a fallback to SQLite (`customer_churn_db.sqlite`) so that during local development or database outages, the application automatically switches to a local file-based database, maintaining 100% uptime."*

### Q2: What is the purpose of the `TotalCharges` column being a `VARCHAR` in the raw SQL table but `NUMERIC` in the clean table?
*   **Answer**: *"The raw telecom dataset has blank space values (`" "`) for customers who joined on the very same day (tenure = 0). If we set `TotalCharges` as `NUMERIC` in the raw table, the database copy import command would throw an error and crash due to formatting mismatch. Keeping it as `VARCHAR` allows ingestion to succeed. Our ETL pipeline then extracts the data, replaces the blank spaces with NaN, fills them with the median charges value, converts it to float, and loads it into the `cleaned_telco_customers` table as `NUMERIC`."*

---

## 🤖 2. Machine Learning & Preprocessing

### Q3: Why did you place the Preprocessors and Feature Engineering inside a Scikit-Learn `Pipeline`?
*   **Answer**: *"We wrapped our custom `FeatureEngineer` transformer, `OneHotEncoder`, and `StandardScaler` inside a Scikit-Learn `Pipeline`. Doing this prevents **data leakage** (leakage of test data parameters like scaling means/std into the training phase). Furthermore, it simplifies deployment: our saved `.pkl` pipeline model files ingest raw, un-transformed JSON payloads directly. Preprocessing is done internally, eliminating training-serving skew."*

### Q4: How did you handle class imbalance in the Churn dataset?
*   **Answer**: *"Customer churn was highly imbalanced: 26.54% churned vs 73.46% retained. To resolve this, we optimized our model class weights:
    1.  For **Logistic Regression**, we set `class_weight="balanced"`.
    2.  For **XGBoost**, we dynamically computed `scale_pos_weight` as the ratio of majority class to minority class (calculated as `2.7686`).
    This forced the models to pay extra attention to churned cases during training, which boosted the recall of our best model (XGBoost) from **67.91% to 81.28%**."*

### Q5: Why is XGBoost selected as the best Churn model, and why is Random Forest Regressor selected as the best LTV model?
*   **Answer**: 
    *   *"For Churn prediction (classification), **XGBoost** outperformed other models after 5-fold cross-validation grid search, achieving the highest F1-Score of **0.6307** and capturing **81.28%** of true churners (Recall)."*
    *   *"For LTV estimation (regression), **Random Forest Regressor** achieved a near-perfect $R^2$ of **0.9992** and a lower Mean Absolute Error ($40.79) compared to Linear Regression. Since LTV is calculated from tenure and MonthlyCharges, the non-linear decision trees in Random Forest captured this interaction perfectly."*

---

## 🌐 3. REST API & Stacked Inference

### Q6: How does the FastAPI REST API connect Churn and LTV models together (Stacked Inference)?
*   **Answer**: *"Our FastAPI application server implements a multi-stage stacked inference pipeline. When a payload is received, the API first predicts the churn risk category (0 or 1). Since customer churn is a critical indicator of customer lifetime value (churned customer relationships terminate, reducing LTV), we inject this predicted churn category as a feature (`Churn`) into the payload. The updated feature vector is then passed into the LTV model pipeline to predict the final Customer Lifetime Value. This replicates a realistic business scenario where future value is conditioned on churn probability."*

---

## 🐳 4. Containers & Deployment

### Q7: Explain the structure of your `docker-compose.yml` file.
*   **Answer**: *"Our Docker Compose configuration defines a multi-container network with three isolated services:
    1.  `db`: Runs a PostgreSQL database container initialized automatically using our SQL schema scripts mounted in `/docker-entrypoint-initdb.d/`.
    2.  `web`: Builds our Python REST API container which connects to the database container over the docker bridge network.
    3.  `metabase`: Launches the Metabase BI Dashboard service for immediate PostgreSQL reporting and KPI visualization.
    This architecture enables our entire infrastructure to deploy locally using a single shell command: `docker-compose up`."*
