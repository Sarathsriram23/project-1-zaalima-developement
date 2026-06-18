# Load dataset
import pandas as pd

df = pd.read_csv(
    r"D:\zaalima\Customer_Churn_LTV_Project\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

print(df.head())

# Check missing values
print(df.isnull().sum())

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Fill missing values using median
df["TotalCharges"] = df["TotalCharges"].fillna(
    df["TotalCharges"].median()
)

# Drop customerID
df.drop("customerID", axis=1, inplace=True)

# Encode target variable
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Verify missing values again
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv(
    r"D:\zaalima\Customer_Churn_LTV_Project\data\cleaned_telco.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Shape:", df.shape)
print(df.head())