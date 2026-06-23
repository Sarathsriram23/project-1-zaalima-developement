# Import Metrics
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
________________________________________
# Evaluation Function
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

          

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Load dataset
df = pd.read_csv("cleaned_telco.csv")


plt.figure(figsize=(6,4))
sns.countplot(x='Churn', data=df)
plt.title('Churn Distribution')
plt.show()

# Percentage
print(df['Churn'].value_counts(normalize=True) * 100)
