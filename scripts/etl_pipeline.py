import os
import pandas as pd
import logging
from db_connection import get_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_etl():
    # 1. Extract
    csv_path = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    if not os.path.exists(csv_path):
        logger.error(f"Raw CSV not found at {csv_path}!")
        return
        
    logger.info(f"Extracting raw data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 2. Load Raw into Database
    engine = get_engine()
    logger.info("Loading raw data into 'telco_customers' table...")
    df_raw = df.copy()
    df_raw.columns = [c.lower() for c in df_raw.columns]
    df_raw.to_sql("telco_customers", engine, if_exists="replace", index=False)
    logger.info("Raw table loaded successfully.")
    
    # 3. Transform (Data Cleaning & Preprocessing)
    logger.info("Starting data cleaning and transformation...")
    cleaned_df = df.copy()
    
    # Handle TotalCharges missing/blank values
    # Convert TotalCharges to numeric, empty strings become NaN
    cleaned_df["TotalCharges"] = pd.to_numeric(cleaned_df["TotalCharges"], errors="coerce")
    
    # Count missing values
    missing_count = cleaned_df["TotalCharges"].isnull().sum()
    logger.info(f"Found {missing_count} missing values in 'TotalCharges'. Filling with median...")
    
    # Fill missing values with median
    median_val = cleaned_df["TotalCharges"].median()
    cleaned_df["TotalCharges"] = cleaned_df["TotalCharges"].fillna(median_val)
    
    # Drop customerID (non-predictive)
    if "customerID" in cleaned_df.columns:
        cleaned_df.drop("customerID", axis=1, inplace=True)
        
    # Map target column Churn to 0/1
    if "Churn" in cleaned_df.columns:
        cleaned_df["Churn"] = cleaned_df["Churn"].map({"No": 0, "Yes": 1})
        
    logger.info("Transformation complete. Preprocessed shape: {}".format(cleaned_df.shape))
    
    # Save to CSV for subsequent modeling steps (maintaining original casing)
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    cleaned_csv_path = "data/cleaned_telco.csv"
    cleaned_df.to_csv(cleaned_csv_path, index=False)
    logger.info(f"Cleaned dataset saved locally at {cleaned_csv_path}")

    # 4. Load Cleaned Data into Database (lowercased)
    logger.info("Loading cleaned data into 'cleaned_telco_customers' table...")
    cleaned_db_df = cleaned_df.copy()
    cleaned_db_df.columns = [c.lower() for c in cleaned_db_df.columns]
    cleaned_db_df.to_sql("cleaned_telco_customers", engine, if_exists="replace", index=False)
    logger.info("Cleaned database table loaded.")

if __name__ == "__main__":
    run_etl()
