# Clean and Preprocess Telco Churn Dataset
import pandas as pd
import os

def preprocess_data():
    raw_csv = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    cleaned_csv = "data/cleaned_telco.csv"
    
    if not os.path.exists(raw_csv):
        print(f"Raw CSV not found at: {raw_csv}")
        return
        
    print(f"Reading dataset: {raw_csv}")
    df = pd.read_csv(raw_csv)
    
    # Check missing values
    print("Initial shape:", df.shape)
    print("Initial missing values:\n", df.isnull().sum())
    
    # Convert TotalCharges to numeric
    print("Converting TotalCharges to numeric...")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    
    # Fill missing values using median
    median_val = df["TotalCharges"].median()
    print(f"Filling missing TotalCharges with median: {median_val}")
    df["TotalCharges"] = df["TotalCharges"].fillna(median_val)
    
    # Drop customerID
    if "customerID" in df.columns:
        print("Dropping customerID column...")
        df.drop("customerID", axis=1, inplace=True)
    
    # Encode target variable Churn (No -> 0, Yes -> 1)
    if "Churn" in df.columns:
        print("Encoding target column Churn...")
        df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})
        
    # Verify missing values again
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    
    # Save cleaned dataset
    df.to_csv(cleaned_csv, index=False)
    print(f"\nCleaned dataset saved successfully to {cleaned_csv}!")
    print("Preprocessed Shape:", df.shape)

if __name__ == "__main__":
    preprocess_data()
