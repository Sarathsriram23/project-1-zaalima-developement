import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

df = pd.read_csv(
    r"D:\zaalima\Customer_Churn_LTV_Project\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

df["AvgChargePerMonth"] = df["TotalCharges"] / (df["tenure"] + 1)

df.drop("customerID", axis=1, inplace=True)

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
}).astype(int)

X = df.drop("Churn", axis=1)
y = df["Churn"]

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        eval_metric="logloss",
        random_state=42
    )
}

best_f1 = 0
best_pipeline = None

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    print(f"\n{name}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC AUC   : {roc_auc:.4f}")

    if f1 > best_f1:
        best_f1 = f1
        best_pipeline = pipeline
        best_name = name

        from sklearn.metrics import classification_report, confusion_matrix

y_pred = best_pipeline.predict(X_test)
y_proba = best_pipeline.predict_proba(X_test)[:, 1]

print("Best Model:", best_name)

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))

print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("ROC AUC  :", roc_auc_score(y_test, y_proba))

import shap

# transform test data
X_test_transformed = best_pipeline.named_steps["preprocessor"].transform(X_test)

# get model
model = best_pipeline.named_steps["classifier"]

feature_names = best_pipeline.named_steps["preprocessor"].get_feature_names_out()

explainer = shap.LinearExplainer(model, X_test_transformed)
shap_values = explainer.shap_values(X_test_transformed)

shap.summary_plot(
    shap_values,
    X_test_transformed,
    feature_names=feature_names
)

shap.summary_plot(
    shap_values,
    X_test_transformed,
    feature_names=feature_names,
    plot_type="bar"
)

shap.force_plot(
    explainer.expected_value,
    shap_values[i],
    X_test_transformed[i],
    feature_names=feature_names,
    matplotlib=True
)

import joblib

joblib.dump(best_pipeline, "churn_model_pipeline.pkl")