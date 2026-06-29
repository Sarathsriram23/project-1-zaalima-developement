# Customer Churn Analysis - Business Insights Report

This document outlines key findings from our Exploratory Data Analysis (EDA) on the Telco Customer Churn dataset. It provides critical business insights, data-backed findings, and actionable recommendations. Additionally, it contains guidance for the presenter on how to explain each visualization.

---

## 1. Executive Summary & Core Metrics

Our dataset comprises **7,043 customers** and **21 initial features**. After preprocessing, the dataset has been cleaned, and blank values in the `TotalCharges` field (which occurred for new customers with `tenure = 0`) were resolved using the median.

*   **Overall Churn Rate**: **26.54%** (1,869 customers out of 7,043 have churned).
*   **Customer Retention Rate**: **73.46%** (5,174 customers remain active).

---

## 2. Key Insights & Visualization Interpretations

### Insight A: Churn Distribution
*   **Finding**: The dataset is imbalanced, with roughly 1 in 4 customers churned. This high rate (26.54%) poses a significant revenue risk.
*   **Presenter Guide for `churn_distribution.png`**:
    > *"In this slide, you see the count of active vs. churned customers. Out of 7,043 total records, 5,174 customers are active and 1,869 have left. This represents a 26.54% overall churn rate. In machine learning, this class imbalance is important because our classification model must be trained specifically to handle it (e.g., using stratified splits and looking at F1-score rather than accuracy alone)."*

### Insight B: Tenure and Monthly Charges
*   **Finding**: 
    1.  **Tenure**: There is a large spike of customers leaving within the first 1-5 months. After the initial period, churn drops, and another major group consists of loyal, long-term customers (70+ months).
    2.  **Monthly Charges**: High monthly charges correlate heavily with churn. Customers with low monthly charges ($20–$30) have high retention rates.
*   **Presenter Guide for `numeric_distributions.png`**:
    > *"Here we look at the distributions of tenure and monthly charges. Note the high density of customers with very low tenure (left peak on tenure chart)—this indicates a critical onboarding retention problem. On the right, the monthly charges histogram shows that while many customers enjoy cheap packages around $20, there is a large bulk of customers paying between $70 and $110, which matches our high-risk churn category."*

### Insight C: Contract Type Influence
*   **Finding**: Contract type is the strongest predictor of churn.
    *   **Month-to-month contracts**: **42.71%** churn rate.
    *   **One-year contracts**: **11.27%** churn rate.
    *   **Two-year contracts**: **2.83%** churn rate.
*   **Presenter Guide for `contract_vs_churn.png`**:
    > *"This chart clearly demonstrates the impact of contract structures. Customers on month-to-month contracts churn at an alarming rate of 42.71%. However, once they sign a one-year contract, that churn rate drops to 11.27%, and further to a negligible 2.83% for two-year contracts. The primary business strategy must be migrating month-to-month customers to long-term commitments through targeted incentives."*

### Insight D: Payment Method Preferences
*   **Finding**: Electronic check users have the highest churn rate by far (**45.29%**). Credit card auto-pay (**15.24%**) and bank transfer auto-pay (**16.71%**) have significantly lower churn rates.
*   **Presenter Guide for `payment_vs_churn.png`**:
    > *"We analyzed customer churn across payment methods. Electronic check users represent the highest risk, with a 45.29% churn rate. Conversely, automated payment options—like credit cards and bank transfers—show churn rates below 17%. Promoting auto-pay options during sign-up could drastically decrease involuntary churn."*

### Insight E: Correlation Analysis
*   **Finding**: 
    *   `tenure` and `TotalCharges` are strongly correlated (0.83), as expected.
    *   `tenure` has a moderate negative correlation with `Churn` (-0.35), meaning longer-term customers are less likely to churn.
*   **Presenter Guide for `correlation_matrix.png`**:
    > *"This correlation heatmap shows how numeric attributes relate. Notice the negative correlation of -0.35 between tenure and Churn—this confirms mathematically that as tenure increases, churn probability decreases. We also see that TotalCharges and tenure are strongly correlated (0.83), meaning we must be careful with collinearity in linear models like Logistic Regression."*

---

## 3. Strategic Business Recommendations

1.  **Incentivize Long-term Contracts**: Provide a small discount (e.g., 5% off monthly fee) for migrating month-to-month users to a 1-year contract.
2.  **Drive Auto-Pay Adoption**: Offer a one-time bill credit (e.g., $10) for signing up for automatic payment (credit card or bank transfer) to reduce electronic check transaction friction.
3.  **Early Intervention Program**: Establish an automated retention campaign targeting customers in their first 3 months who have monthly bills exceeding $80.
