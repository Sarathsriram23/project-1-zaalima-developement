<<<<<<< HEAD
#Import Metrics
=======
# Import Metrics
>>>>>>> 8cfaf524b409ceba89eedf99ff41032df670dd66
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
<<<<<<< HEAD
#Evaluation Function
=======
________________________________________
# Evaluation Function
>>>>>>> 8cfaf524b409ceba89eedf99ff41032df670dd66
def evaluate(y_true, y_pred, y_prob):
    print("Accuracy:",
          accuracy_score(y_true,y_pred))

    print("Precision:",
          precision_score(y_true,y_pred))

    print("Recall:",
          recall_score(y_true,y_pred))

    print("F1:",
          f1_score(y_true,y_pred))

    print("ROC AUC:",
          roc_auc_score(y_true,y_prob))

<<<<<<< HEAD
=======
          

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")

# Load dataset
df = pd.read_csv("cleaned_telco.csv")
print(df.head())
print(df.info())
print(df.describe())
plt.figure(figsize=(6,4))
sns.countplot(x='Churn', data=df)
plt.title('Churn Distribution')
plt.show()

# Percentage
print(df['Churn'].value_counts(normalize=True) * 100)
<<<<<<< HEAD

#Checking for missing values
print(df.isnull().sum())
missing_values = df.isnull().sum()/len(df) * 100
print(missing_values)

#checking for duplicates
print(df.duplicated().sum())

#churn percentage
churn_percentage = df['Churn'].value_counts(normalize=True) * 100
print("Churn Percentage:")
print(churn_percentage)

#Contract Analysis
contract_counts = df['Contract'].value_counts() 
print("Contract Distribution:")
print(contract_counts)  

#Monhly charges distribution
plt.figure(figsize=(6,4))
sns.histplot(df['MonthlyCharges'], bins=30, kde=True)
plt.title('Monthly Charges Distribution')
plt.xlabel('Monthly Charges')
plt.ylabel('Frequency')
plt.show()  

#Tenure analysis
plt.figure(figsize=(6,4))
sns.histplot(df['Tenure'], bins=30, kde=True)
plt.title('Tenure Distribution')
plt.xlabel('Tenure')
plt.ylabel('Frequency')
plt.show()  

#Correlation Heatmap
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

#Revenue Analysis
plt.figure(figsize=(6,4))
sns.histplot(df['Revenue'], bins=30, kde=True)
plt.title('Revenue Distribution')
plt.xlabel('Revenue')
plt.ylabel('Frequency')
plt.show()        

#Business Insights
# Churn Rate by Contract Type
plt.figure(figsize=(6,4))
sns.barplot(x='Contract', y='Churn', data=df, estimator=lambda x: sum(x==1)/len(x))
plt.title('Churn Rate by Contract Type')  
plt.xlabel('Contract Type')
plt.ylabel('Churn Rate')
plt.show()


plt.figure(figsize=(6,4))
sns.barplot(x='PaymentMethod', y='Churn', data=df, estimator=lambda x: sum(x==1)/len(x))
plt.title('Churn Rate by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Churn Rate')
plt.show()
=======
>>>>>>> 8cfaf524b409ceba89eedf99ff41032df670dd66
>>>>>>> 03ccc8918f508c0760e12bbffaa632fd0ea45201
