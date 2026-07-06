import pandas as pd

df = pd.read_csv(
    r"D:\zaalima\Customer_Churn_LTV_Project\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(subset=["TotalCharges"], inplace=True)

# Revenue-based estimated LTV
df["Estimated_LTV"] = df["MonthlyCharges"] * df["tenure"]

print(df[["customerID",
          "tenure",
          "MonthlyCharges",
          "Estimated_LTV"]])

print("\n----- Estimated LTV Summary -----")
print(f"Average Estimated LTV : ${df['Estimated_LTV'].mean():,.2f}")
print(f"Maximum Estimated LTV : ${df['Estimated_LTV'].max():,.2f}")