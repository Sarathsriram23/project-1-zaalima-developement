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

#Monthly charges distribution
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

#internet service vs churn
plt.figure(figsize=(6,4))
sns.barplot(x='InternetService', y='Churn', data=df, estimator=lambda x: sum(x)/len(x))         
plt.title('Churn Rate by Internet Service')  
plt.xlabel('Internet Service')
plt.ylabel('Churn Rate')
plt.show()

#gender vs churn
plt.figure(figsize=(5,4))
sns.barplot(x='gender', y='Churn', data=df, estimator=lambda x: sum(x)/len(x))
plt.title('Churn Rate by Gender')
plt.xlabel('Gender')
plt.ylabel('Churn Rate')
plt.show()

#Senior Citizen vs churn
plt.figure(figsize=(5,4))
sns.barplot(x='SeniorCitizen', y='Churn', data=df, estimator=lambda x: sum(x)/len(x))
plt.title('Churn Rate by Senior Citizen Status')
plt.xlabel('Senior Citizen')
plt.ylabel('Churn Rate')      
plt.show()

#Partner vs churn
plt.figure(figsize=(5,4))
sns.barplot(x='Partner', y='Churn', data=df, estimator=lambda x: sum(x)/len(x))
plt.title('Churn Rate by Partner Status')
plt.xlabel('Partner')
plt.ylabel('Churn Rate')
plt.show()

#dependents vs churn
plt.figure(figsize=(5,4))     
sns.barplot(x='Dependents', y='Churn', data=df, estimator=lambda x: sum(x)/len(x))
plt.title('Churn Rate by Dependents Status')
plt.xlabel('Dependents')
plt.ylabel('Churn Rate')
plt.show()

#MONTHLY CHARGES VS CHURN
plt.figure(figsize=(6,4))   
sns.histplot(df[df['Churn']==1]['MonthlyCharges'], bins=30, kde=True)
plt.title('Distribution of Monthly Charges for Churned Customers')
plt.xlabel('Monthly Charges')
plt.ylabel('count')
plt.show()
 
 #tenure distribution
plt.figure(figsize=(6,4))
sns.histplot(df[df['tenure']<=12]['tenure'], bins=30, kde=True)
plt.title('customer tenure distribution')
plt.xlabel('Tenure')    
plt.ylabel('customers')
plt.show()

#monthly charges vs churn
plt.figure(figsize=(6,4))
sns.histplot(df[df['Churn']==1]['MonthlyCharges'], bins=30, kde=True)
plt.title('Distribution of Monthly Charges for Churned Customers')
plt.xlabel('Monthly Charges')
plt.ylabel('count')
plt.show()

#tenure vs churn
plt.figure(figsize=(6,4))
sns.boxenplot(x='Churn', y='tenure', data=df)
plt.title('Tenure Distribution by Churn Status')
plt.xlabel('Churn')
plt.ylabel('Tenure')
plt.show()

#correlation heatmap
plt.figure(figsize=(10,8))
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

#revenue by contract type
plt.figure(figsize=(6,4))
revenue_by_contract = df.groupby('Contract')['Revenue'].mean().reset_index()
sns.barplot(x='Contract', y='Revenue', data=revenue_by_contract)  
plt.title('Average Revenue by Contract Type')   
plt.xlabel('Contract Type')
plt.ylabel('Average Revenue')       


#churn percentage by contract type
plt.figure(figsize=(6,4))           
plt.pie(churn_percentage, labels=churn_percentage.index, autopct='%1.1f%%', startangle=90)
plt.title('Churn Percentage by Contract Type')
plt.show()

print("business insights completed successfully")
print("month-to-month customers have the highest churn rate, while two-year contract customers have the lowest churn rate")
print("customer with longer tenure are less likely to churn, while customers with shorter tenure are more likely to churn")
print("higher monthly charges are associated with higher churn rates, while lower monthly charges are associated with lower churn rates")
print("electronic check users have the highest churn rate, while fiber optic users have the lowest churn rate")
print("long term contracts improve customer retention, while month-to-month contracts increase churn risk")

EstimatedLTV= MonthlyCharges * tenure
df['EstimatedLTV'] = df['MonthlyCharges'] * df['tenure']
print(df[['MonthlyCharges', 'tenure', 'EstimatedLTV']].head())

contract_ltv = df.groupby('Contract')['EstimatedLTV'].mean()
print(contract_ltv)

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(6,4))
sns.barplot(x="Contract", y="EstimatedLTV", data=df, estimator=lambda x: x.mean())
plt.title('Average Estimated LTV by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Average Estimated LTV')
plt.show()


internet_ltv = df.groupby('InternetService')['EstimatedLTV'].mean()
print(internet_ltv)

plt.figure(figsize=(6,4))
sns.barplot(x="InternetService", y="EstimatedLTV", data=df, estimator=lambda x: x.mean())
plt.title('Average Estimated LTV by Internet Service Type')
plt.show()

payment_ltv = df.groupby('PaymentMethod')['EstimatedLTV'].mean()
print(payment_ltv)


top_customers = df.nlargest(10, 'EstimatedLTV')
print(top_customers[['customer_id', 'EstimatedLTV']])

df.to_csv('cleaned_telco_with_ltv.csv', index=False)


                    



