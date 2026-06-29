import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12

os.makedirs("reports", exist_ok=True)

df = pd.read_csv('data/cleaned_telco.csv')

# 1. Churn Distribution
plt.figure(figsize=(6, 5))
sns.countplot(x='Churn', data=df, palette='viridis')
plt.title('Distribution of Customer Churn')
plt.xlabel('Churn (0 = No, 1 = Yes)')
plt.ylabel('Count')
plt.xticks([0, 1], ['Retained (No)', 'Churned (Yes)'])
plt.tight_layout()
plt.savefig('reports/churn_distribution.png')
plt.close()

# 2. Key Numeric Features
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['MonthlyCharges'], bins=30, kde=True, color='skyblue')
plt.title('Monthly Charges Distribution')
plt.xlabel('Monthly Charges ($)')

plt.subplot(1, 2, 2)
sns.histplot(df['tenure'], bins=30, kde=True, color='salmon')
plt.title('Tenure Distribution')
plt.xlabel('Tenure (Months)')

plt.tight_layout()
plt.savefig('reports/numeric_distributions.png')
plt.close()

# 3. Contract vs Churn
contract_churn = df.groupby('Contract')['Churn'].mean().reset_index()
contract_churn['Churn'] = contract_churn['Churn'] * 100
plt.figure(figsize=(8, 5))
sns.barplot(x='Contract', y='Churn', data=contract_churn, palette='coolwarm')
plt.title('Churn Rate by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Churn Rate (%)')
plt.tight_layout()
plt.savefig('reports/contract_vs_churn.png')
plt.close()

# 4. Payment Method vs Churn
pm_churn = df.groupby('PaymentMethod')['Churn'].mean().reset_index()
pm_churn['Churn'] = pm_churn['Churn'] * 100
pm_churn = pm_churn.sort_values(by='Churn', ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x='Churn', y='PaymentMethod', data=pm_churn, palette='magma')
plt.title('Churn Rate by Payment Method')
plt.xlabel('Churn Rate (%)')
plt.ylabel('Payment Method')
plt.tight_layout()
plt.savefig('reports/payment_vs_churn.png')
plt.close()

# 5. Correlation Heatmap
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title('Correlation Matrix of Numeric Features')
plt.tight_layout()
plt.savefig('reports/correlation_matrix.png')
plt.close()

print("All EDA plots generated successfully in reports/ directory.")
