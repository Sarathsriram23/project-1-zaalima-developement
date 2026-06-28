import pandas as pd
import joblib
import shap

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import precision_score, recall_score, f1_score

#Feature Engineering
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df = df.dropna()

df["AvgChargePerMonth"] = (
    df["TotalCharges"] / (df["tenure"] + 1)
)

# Remove customer ID
df = df.drop("customerID", axis=1)

# Target Encoding
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# splitting target and features
X = df.drop("Churn", axis=1)
y = df["Churn"]

#Encoding and Scaling
categorical_cols = X.select_dtypes(include="object").columns
numeric_cols = X.select_dtypes(exclude="object").columns

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_cols
        ),
        (
            "num",
            StandardScaler(),
            numeric_cols
        )
    ]
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#Model Training
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        eval_metric="logloss",
        random_state=42
    )
}

#Training and Evaluation
results = []

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    results.append([
        name,
        precision,
        recall,
        f1
    ])

    print(f"\n{name}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    joblib.dump(
        pipeline,
        f"../models/{name.replace(' ','_').lower()}.pkl"
    )

    #Results DataFrame
    results_df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "Precision",
        "Recall",
        "F1 Score"
    ]
)

print("\nModel Comparison")
print(results_df)

xgb_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", XGBClassifier(
        eval_metric="logloss",
        random_state=42
    ))
])

#SHAP for XGBoost

xgb_pipeline.fit(X_train, y_train)

X_processed = xgb_pipeline.named_steps[
    "preprocessor"
].transform(X_test)

explainer = shap.TreeExplainer(
    xgb_pipeline.named_steps["classifier"]
)

shap_values = explainer.shap_values(
    X_processed
)

shap.summary_plot(
    shap_values,
    X_processed
)
