import pandas as pd

df = pd.read_csv(
    r"D:\zaalima\Customer_Churn_LTV_Project\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

PROFIT_MARGIN = 0.30

# Historical revenue
df["Revenue_LTV"] = df["TotalCharges"]

# Estimated profit
df["Profit_LTV"] = df["Revenue_LTV"] * PROFIT_MARGIN

print(df[["customerID", "tenure", "MonthlyCharges",
          "TotalCharges", "Revenue_LTV", "Profit_LTV"]])

print("\nSummary")
print(f"Total Revenue LTV : ${df['Revenue_LTV'].sum():,.2f}")
print(f"Average Revenue LTV : ${df['Revenue_LTV'].mean():,.2f}")
print(f"Total Profit LTV : ${df['Profit_LTV'].sum():,.2f}")
print(f"Average Profit LTV : ${df['Profit_LTV'].mean():,.2f}")
