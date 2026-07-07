# Academic Final Project Report: Telco Customer Churn & LTV Predictive Platform

**Course Milestone Project**  
**Team Contributions**:  
*   **Member 1 (Data Engineer)**: Schema setups, `db_connection.py`, `etl_pipeline.py` ingestion, Docker configurations, and multi-container docker-compose network.  
*   **Member 2 (Data Analyst)**: Jupyter EDA Notebook, `business_insights.md` report, and LTV segment analysis.  
*   **Member 3 (ML Engineer)**: Standalone preprocessing utility `preprocess.py`, classifier cross-validation training, regressor training pipeline (`train_ltv.py`), and model metric comparison.  
*   **Member 4 (API Developer)**: FastAPI REST backend framework, lifespan model loaders, and endpoint controllers.  
*   **Member 5 (BI & Deployment)**: Dashboard query layouts, Metabase connection pipelines, and README documentation.

---

## 📄 Table of Contents
1.  [Introduction](#1-introduction)
2.  [Problem Statement](#2-problem-statement)
3.  [Literature Review](#3-literature-review)
4.  [Dataset Description](#4-dataset-description)
5.  [Methodology](#5-methodology)
6.  [Exploratory Data Analysis (EDA)](#6-exploratory-data-analysis-eda)
7.  [Churn Prediction Models](#7-churn-prediction-models)
8.  [Customer Lifetime Value (LTV) Prediction](#8-customer-lifetime-value-ltv-prediction)
9.  [FastAPI Development & Stacked Inference](#9-fastapi-development--stacked-inference)
10. [Dashboard Development (Metabase)](#10-dashboard-development-metabase)
11. [Results & Model Comparison](#11-results--model-comparison)
12. [Conclusion](#12-conclusion)
13. [Future Scope](#13-future-scope)
14. [References](#14-references)

---

## 1. Introduction
Customer churn represents the percentage of subscribers to a service who discontinue their subscriptions within a given time frame. In the telecommunications sector, where subscriber growth rates are plateauing and acquisition costs are high, customer retention represents a critical strategic priority. 

This project details the development of an end-to-end predictive analytics platform that integrates:
1.  A robust ETL ingestion pipeline mapping raw billing data to relational PostgreSQL databases.
2.  A machine learning engine containing tuned classifiers for churn risk estimation and regression models for Customer Lifetime Value (LTV) forecasting.
3.  An industrial-grade FastAPI REST service to serve predictions instantly.
4.  An interactive Metabase Dashboard network to display key metrics for business intelligence.

---

## 2. Problem Statement
The telecom sector suffers from high customer acquisition costs (CAC). Acquiring a new customer is up to five times more expensive than retaining an existing subscriber. Telecom executives struggle with two main challenges:
1.  **Identifying High-Risk Customers**: Recognizing customer churn after the fact is too late. The company needs to proactively identify customers at risk of leaving.
2.  **Revenue Prioritization**: Not all customers are of equal value. To maximize the return on marketing campaigns, retention resources should be targeted at high-risk customers who also represent high Customer Lifetime Value (LTV).

Our goal is to build an automated pipeline that outputs **Churn Risk Probability** and **Estimated LTV** concurrently for any customer profile.

---

## 3. Literature Review
Academic literature on Customer Relationship Management (CRM) analytics emphasizes the superiority of predictive modeling over static rule-based segmentations. 

Historically, companies relied on simple rules (e.g., *"Flag customer if they call support twice"*). Modern research demonstrates that ensemble machine learning models, specifically **Extreme Gradient Boosting (XGBoost)** and **Random Forests**, capture non-linear interactions among demographics, billing structures, and service packages far more effectively. 

Additionally, current trends emphasize **Explainable AI (XAI)** frameworks like **SHAP (SHapley Additive exPlanations)**. SHAP values mathematically explain black-box models by allocating feature importance contributions to individual predictions based on cooperative game theory, ensuring transparency.

---

## 4. Dataset Description
The platform leverages the **WA_Fn-UseC_-Telco-Customer-Churn** dataset consisting of **7,043 customer records** with **21 attributes**.

### Key Feature Segments:
1.  **Demographics**: Gender, SeniorCitizen (0/1), Partner (Yes/No), Dependents (Yes/No).
2.  **Services Subscribed**: PhoneService, MultipleLines, InternetService (DSL/Fiber optic/No), OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies.
3.  **Billing & Contract Information**: Tenure (months), Contract type (Month-to-month, One year, Two year), PaperlessBilling, PaymentMethod (Electronic check, Mailed check, Bank transfer, Credit card), MonthlyCharges, and TotalCharges.

---

## 5. Methodology
The platform architecture utilizes a modular engineering layout:

```
[Raw Billing CSV] ──► [ETL Ingestion Pipeline] ──► [PostgreSQL Database]
                                                            │
  ┌─────────────────────────────────────────────────────────┘
  ▼
[ML Pipelines] (OneHotEncoding + StandardScaler + Custom Feature Engineering)
  ├── Churn Classifier: Tuned XGBoost (GridSearchCV)
  └── LTV Regressor: Random Forest Regressor
  │
  ▼
[FastAPI REST Application] (Model Lifespans, Pydantic Schema Validations)
  ├── POST /predict_churn
  ├── POST /predict_ltv
  ├── POST /predict_all (Stacked Inference)
  └── GET /predict_customer/{customer_id} (Live DB query and prediction)
  │
  ▼
[Metabase BI Dashboard & Docker Containers]
```

---

## 6. Exploratory Data Analysis (EDA)
Exploratory data analysis of the dataset revealed several key operational insights:
1.  **Contract Influence**: Customers on Month-to-Month contracts exhibit a churn rate of **~42.7%**, whereas customers on Two-Year contracts exhibit a churn rate of less than **3%**. Month-to-month contracts are highly volatile.
2.  **Payment Methods**: Electronic Check users show significantly higher churn levels compared to automated credit card or bank transfer cohorts.
3.  **Financial Impact**: Churn is concentrated in cohorts with higher Monthly Charges. Loyal customers have high tenures and lower average monthly rates, suggesting price sensitivity.

---

## 7. Churn Prediction Models
The classification task predicts the binary target `Churn` (0 = Retained, 1 = Churn).

### A. Handling Class Imbalance
The dataset contains a class split of **73.46% (Retained)** vs **26.54% (Churned)**. Standard classifiers trained on this dataset favor the majority class, leading to poor Churner Recall. To solve this:
*   We optimized Logistic Regression using `class_weight="balanced"`.
*   We calculated and configured XGBoost's `scale_pos_weight` parameter:
    $$\text{scale\_pos\_weight} = \frac{\text{Count of Majority Class}}{\text{Count of Minority Class}} = 2.7686$$

### B. Machine Learning Algorithms Compared
1.  **Logistic Regression (Class-Balanced)**: Establishes a linear classification baseline.
2.  **Random Forest Classifier**: Evaluates decision-tree ensemble boundaries.
3.  **XGBoost Classifier**: A gradient-boosting framework using regularization to minimize overfitting.

Hyperparameters were optimized using 5-fold cross-validated grid search (`GridSearchCV`) maximizing the **Recall** of the churn class.

---

## 8. Customer Lifetime Value (LTV) Prediction
LTV represents the estimated revenue a customer generates over their relationship lifetime. In this dataset, LTV is modeled as:
$$\text{LTV} = \text{MonthlyCharges} \times \text{tenure}$$

We trained and compared two regression models to forecast LTV for active customers:
1.  **Linear Regression**: Serves as a linear baseline.
2.  **Random Forest Regressor**: Captures non-linear feature splits and billing package interactions.

The models utilize the exact same feature preprocessing pipeline as the churn model, ensuring input consistency.

---

## 9. FastAPI Development & Stacked Inference
The REST API was built using **FastAPI** due to its async speed and automatic Swagger schema generations.

### Stacked Multi-Stage Inference
Since LTV is heavily conditioned on whether a customer churns (a churned customer generates no more revenue), we engineered a **stacked prediction workflow**:
1.  The API first feeds the user payload into the **XGBoost Churn Classifier** to get `predicted_churn` (`0` or `1`).
2.  This predicted churn status is dynamically inserted into the payload as a new feature: `df_input['Churn'] = predicted_churn`.
3.  The combined features are then fed into the **Random Forest Regressor** to predict the final Customer Lifetime Value.

---

## 10. Dashboard Development (Metabase)
We connected **Metabase** to the PostgreSQL database to support executive KPI reporting. 

### Key Dashboard Queries Implemented:
*   **Total Customers**:
    ```sql
    SELECT COUNT(*) FROM telco_customers;
    ```
*   **Churn Rate**:
    ```sql
    SELECT ROUND(100.0 * SUM(CASE WHEN churn = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate 
    FROM telco_customers;
    ```
*   **Average LTV per Contract Type**:
    ```sql
    SELECT contract, ROUND(AVG(monthlycharges * tenure), 2) AS avg_ltv 
    FROM telco_customers 
    GROUP BY contract;
    ```

---

## 11. Results & Model Comparison

### Churn Classification Results
XGBoost emerged as the best model, capturing over **81.28%** of true churners.

| Classification Model | Accuracy | Churn Precision | Churn Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression (Balanced) | 74.88% | 52.12% | 78.61% | 0.6266 |
| Random Forest Classifier | 79.06% | 61.34% | 49.20% | 0.5557 |
| **Tuned XGBoost (scale_pos_weight)** | **76.01%** | **53.90%** | **81.28%** | **0.6307** |

### LTV Regression Results
The Random Forest Regressor captured the non-linear calculation of LTV perfectly.

| Regression Model | $R^2$ Score | Mean Absolute Error (MAE) |
| :--- | :---: | :---: |
| Linear Regression | 0.9067 | $245.50 |
| **Random Forest Regressor** | **0.9992** | **$40.79** |

---

## 12. Conclusion
This project successfully demonstrates how raw operational database tables, machine learning models, REST APIs, and visualization dashboards integrate into a cohesive BI platform.
1.  **Ensemble models** (XGBoost & Random Forest) outperformed traditional linear models.
2.  **Addressing class imbalance** (via `scale_pos_weight = 2.7686`) boosted churner detection recall from ~49% to over **81%**.
3.  **Stacked inference** allows the business to predict lifetime value conditioned on active churn risk, giving marketing managers a precise tool for customer retention campaigns.

---

## 13. Future Scope
1.  **Deep Learning Sequence Models**: Transitioning from static models to Recurrent Neural Networks (RNNs) or LSTMs to process sequential billing events over time.
2.  **Automated Campaigns**: Integrating webhook triggers in FastAPI to automatically push retention coupons or discount emails to users whose predicted churn risk exceeds `75%`.
3.  **Real-Time Data Streaming**: Adding Apache Kafka to feed live clickstream and billing database logs directly to the model pipeline.

---

## 14. References
1.  Pedregosa, F. et al. (2011). *Scikit-learn: Machine learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
2.  Lundberg, S. M., & Lee, S.-I. (2017). *A unified approach to interpreting model predictions*. Advances in Neural Information Processing Systems, 4765-4774.
3.  FastAPI documentation: `https://fastapi.tiangolo.com/`
4.  XGBoost documentation: `https://xgboost.readthedocs.io/`
