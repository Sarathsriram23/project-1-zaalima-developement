import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Customer Churn Prediction - Exploratory Data Analysis (EDA)\n",
    "This notebook contains the exploratory analysis of the Telco Customer Churn dataset. We will analyze target distribution, missing values, correlation, and analyze how features like tenure, contract type, payment method, and monthly charges affect customer churn."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Set style for visualizations\n",
    "plt.style.use('seaborn-v0_8-whitegrid')\n",
    "plt.rcParams[\"figure.figsize\"] = (10, 6)\n",
    "plt.rcParams[\"font.size\"] = 12"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Load the Preprocessed Dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('../data/cleaned_telco.csv')\n",
    "print(f\"Dataset Shape: {df.shape}\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Basic Dataset Info & Missing Values"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"--- Dataset Info ---\")\n",
    "print(df.info())\n",
    "\n",
    "print(\"\\n--- Descriptive Statistics ---\")\n",
    "print(df.describe())\n",
    "\n",
    "print(\"\\n--- Missing Values ---\")\n",
    "print(df.isnull().sum())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Target Variable Analysis: Churn Distribution"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "churn_counts = df['Churn'].value_counts()\n",
    "churn_pct = df['Churn'].value_counts(normalize=True) * 100\n",
    "print(\"Churn counts:\")\n",
    "print(churn_counts)\n",
    "print(\"\\nChurn percentage:\")\n",
    "print(churn_pct)\n",
    "\n",
    "plt.figure(figsize=(6, 5))\n",
    "plt.bar(['Retained (No)', 'Churned (Yes)'], churn_counts, color=['#2b6cb0', '#e53e3e'], width=0.6)\n",
    "plt.title('Distribution of Customer Churn')\n",
    "plt.ylabel('Count')\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/churn_distribution.png', dpi=300)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Key Numeric Features: Tenure & Monthly Charges"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Monthly Charges & Tenure distributions\n",
    "plt.figure(figsize=(12, 5))\n",
    "\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.hist(df['MonthlyCharges'], bins=30, color='skyblue', edgecolor='white', alpha=0.8)\n",
    "plt.title('Monthly Charges Distribution')\n",
    "plt.xlabel('Monthly Charges ($)')\n",
    "plt.ylabel('Frequency')\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
    "\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.hist(df['tenure'], bins=30, color='salmon', edgecolor='white', alpha=0.8)\n",
    "plt.title('Tenure Distribution')\n",
    "plt.xlabel('Tenure (Months)')\n",
    "plt.ylabel('Frequency')\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/numeric_distributions.png', dpi=300)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Contract Type vs. Customer Churn"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "contract_churn = df.groupby('Contract')['Churn'].mean() * 100\n",
    "print(contract_churn)\n",
    "\n",
    "plt.figure(figsize=(8, 5))\n",
    "plt.bar(contract_churn.index, contract_churn.values, color=['#319795', '#dd6b20', '#e53e3e'], width=0.5)\n",
    "plt.title('Churn Rate by Contract Type')\n",
    "plt.xlabel('Contract Type')\n",
    "plt.ylabel('Churn Rate (%)')\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/contract_vs_churn.png', dpi=300)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Payment Method vs. Customer Churn"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "pm_churn = df.groupby('PaymentMethod')['Churn'].mean().sort_values(ascending=True) * 100\n",
    "print(pm_churn)\n",
    "\n",
    "plt.figure(figsize=(10, 5))\n",
    "plt.barh(pm_churn.index, pm_churn.values, color='#805ad5', height=0.5)\n",
    "plt.title('Churn Rate by Payment Method')\n",
    "plt.xlabel('Churn Rate (%)')\n",
    "plt.ylabel('Payment Method')\n",
    "plt.grid(axis='x', linestyle='--', alpha=0.7)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/payment_vs_churn.png', dpi=300)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Numeric Feature Correlation Heatmap"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "numeric_df = df.select_dtypes(include=[np.number])\n",
    "corr = numeric_df.corr()\n",
    "\n",
    "plt.figure(figsize=(8, 6))\n",
    "cax = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)\n",
    "plt.colorbar(cax)\n",
    "ticks = np.arange(len(corr.columns))\n",
    "plt.xticks(ticks, corr.columns, rotation=45, ha='right')\n",
    "plt.yticks(ticks, corr.columns)\n",
    "\n",
    "# Annotate values\n",
    "for i in range(len(corr.columns)):\n",
    "    for j in range(len(corr.columns)):\n",
    "        plt.text(j, i, f\"{corr.iloc[i, j]:.2f}\", ha='center', va='center', color='black')\n",
    "\n",
    "plt.title('Correlation Matrix of Numeric Features', fontsize=14, pad=15)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/correlation_matrix.png', dpi=300)\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

# Ensure directories exist
os.makedirs("notebooks", exist_ok=True)
os.makedirs("reports", exist_ok=True)

output_file = "notebooks/EDA.ipynb"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print(f"Created notebook at {output_file} successfully.")
