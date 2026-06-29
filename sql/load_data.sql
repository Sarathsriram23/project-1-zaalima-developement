-- SQL Script to import raw CSV data into telco_customers table
-- Target: PostgreSQL
-- Note: Replace '/path/to/WA_Fn-UseC_-Telco-Customer-Churn.csv' with the absolute path of the CSV on your PostgreSQL server.

COPY telco_customers(
    customerID, gender, SeniorCitizen, Partner, Dependents, tenure, 
    PhoneService, MultipleLines, InternetService, OnlineSecurity, 
    OnlineBackup, DeviceProtection, TechSupport, StreamingTV, 
    StreamingMovies, Contract, PaperlessBilling, PaymentMethod, 
    MonthlyCharges, TotalCharges, Churn
)
FROM 'WA_Fn-UseC_-Telco-Customer-Churn.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');
