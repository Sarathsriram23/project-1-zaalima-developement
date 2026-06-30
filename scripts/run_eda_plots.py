import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set style for visualizations
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12

os.makedirs("reports", exist_ok=True)

df = pd.read_csv('data/cleaned_telco.csv')

# 1. Churn Distribution
plt.figure(figsize=(6, 5))
counts = df['Churn'].value_counts()
plt.bar(['Retained (No)', 'Churned (Yes)'], counts, color=['#2b6cb0', '#e53e3e'], width=0.6)
plt.title('Distribution of Customer Churn', fontsize=14, pad=15)
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('reports/churn_distribution.png', dpi=300)
plt.close()

# 2. Key Numeric Features
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df['MonthlyCharges'], bins=30, color='skyblue', edgecolor='white', alpha=0.8)
plt.title('Monthly Charges Distribution', fontsize=12)
plt.xlabel('Monthly Charges ($)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.subplot(1, 2, 2)
plt.hist(df['tenure'], bins=30, color='salmon', edgecolor='white', alpha=0.8)
plt.title('Tenure Distribution', fontsize=12)
plt.xlabel('Tenure (Months)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('reports/numeric_distributions.png', dpi=300)
plt.close()

# 3. Contract vs Churn
contract_churn = df.groupby('Contract')['Churn'].mean() * 100
plt.figure(figsize=(8, 5))
plt.bar(contract_churn.index, contract_churn.values, color=['#319795', '#dd6b20', '#e53e3e'], width=0.5)
plt.title('Churn Rate by Contract Type', fontsize=14, pad=15)
plt.xlabel('Contract Type')
plt.ylabel('Churn Rate (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('reports/contract_vs_churn.png', dpi=300)
plt.close()

# 4. Payment Method vs Churn
pm_churn = df.groupby('PaymentMethod')['Churn'].mean().sort_values(ascending=True) * 100
plt.figure(figsize=(10, 5))
plt.barh(pm_churn.index, pm_churn.values, color='#805ad5', height=0.5)
plt.title('Churn Rate by Payment Method', fontsize=14, pad=15)
plt.xlabel('Churn Rate (%)')
plt.ylabel('Payment Method')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('reports/payment_vs_churn.png', dpi=300)
plt.close()

# 5. Correlation Heatmap
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
plt.figure(figsize=(8, 6))
cax = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(cax)
ticks = np.arange(len(corr.columns))
plt.xticks(ticks, corr.columns, rotation=45, ha='right')
plt.yticks(ticks, corr.columns)
# Annotate values
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha='center', va='center', color='black')
plt.title('Correlation Matrix of Numeric Features', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig('reports/correlation_matrix.png', dpi=300)
plt.close()

print("All EDA plots generated successfully using Matplotlib.")
