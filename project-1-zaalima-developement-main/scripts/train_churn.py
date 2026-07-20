# Train and Evaluate Churn Prediction Models
import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from evaluate_models import evaluate
from custom_transformers import FeatureEngineer

def train_models():
    # 1. Load data
    data_path = "data/cleaned_telco.csv"
    if not os.path.exists(data_path):
        print(f"Cleaned dataset not found at: {data_path}")
        return
        
    print(f"Loading cleaned dataset: {data_path}")
    df = pd.read_csv(data_path)
    
    # 2. Separate features and target (No manual feature engineering here!)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]
    
    # 3. Identify categorical and numeric columns
    categorical_cols = X.select_dtypes(include="object").columns.tolist()
    # Add engineered column to numeric_cols so the ColumnTransformer scales it
    numeric_cols = X.select_dtypes(exclude="object").columns.tolist() + ["AvgChargePerMonth"]
    
    print(f"Categorical features ({len(categorical_cols)}): {categorical_cols}")
    print(f"Numeric features ({len(numeric_cols)}): {numeric_cols}")
    
    # 4. Define ColumnTransformer for preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )
    
    # 5. Train-test split (80/20, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # Calculate scale_pos_weight for XGBoost to handle class imbalance (negative class / positive class)
    num_neg = sum(y_train == 0)
    num_pos = sum(y_train == 1)
    scale_pos_weight = num_neg / num_pos
    print(f"XGBoost scale_pos_weight: {scale_pos_weight:.4f}")
    
    # 6. Initialize models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced"),
        "XGBoost": XGBClassifier(eval_metric="logloss", random_state=42, scale_pos_weight=scale_pos_weight, use_label_encoder=False)
    }
    
    # 7. Train, tune, and evaluate
    results = {}
    best_f1 = 0
    best_model_name = ""
    best_pipeline = None
    
    # Define hyperparameter grid for tuning
    param_grids = {
        "Logistic Regression": {
            "classifier__C": [0.01, 0.1, 1.0, 10.0]
        },
        "Random Forest": {
            "classifier__n_estimators": [50, 100],
            "classifier__max_depth": [5, 10, None]
        },
        "XGBoost": {
            "classifier__max_depth": [3, 5, 7],
            "classifier__learning_rate": [0.01, 0.1]
        }
    }
    
    os.makedirs("models", exist_ok=True)
    
    for name, model in models.items():
        print(f"\n================ Training and Tuning {name} ================")
        # Pipeline contains FeatureEngineer() as step 1
        pipeline = Pipeline(steps=[
            ("feature_engineering", FeatureEngineer()),
            ("preprocessor", preprocessor),
            ("classifier", model)
        ])
        
        # Setup Grid Search
        grid_search = GridSearchCV(
            pipeline,
            param_grid=param_grids[name],
            cv=5,
            scoring="f1",
            n_jobs=-1
        )
        
        print(f"Running Grid Search for {name} using 5-fold cross-validation...")
        grid_search.fit(X_train, y_train)
        
        # Get the best estimator
        best_est = grid_search.best_estimator_
        print(f"Best parameters for {name}: {grid_search.best_params_}")
        
        # Predict on test set using the best estimator
        y_pred = best_est.predict(X_test)
        y_prob = best_est.predict_proba(X_test)[:, 1]
        
        # Score
        metrics = evaluate(y_test, y_pred, y_prob)
        results[name] = metrics
        
        # Save each model's best pipeline
        model_filename = f"models/{name.lower().replace(' ', '_')}.pkl"
        joblib.dump(best_est, model_filename)
        print(f"Saved optimized {name} model pipeline to {model_filename}")
        
        # Track the overall best model based on test F1 Score
        if metrics["F1 Score"] > best_f1:
            best_f1 = metrics["F1 Score"]
            best_model_name = name
            best_pipeline = best_est
            
    # 8. Print comparison summary
    print("\n================ Model Comparison Summary ================")
    summary_df = pd.DataFrame(results).T
    print(summary_df)
    
    print(f"\nBest Model: {best_model_name} with F1-Score: {best_f1:.4f}")
    
    # Save best model to standard location
    joblib.dump(best_pipeline, "models/churn_model.pkl")
    print("Saved best model pipeline to models/churn_model.pkl")
    
    # 9. Generate dashboard predictions file using best model (Member 5 Deliverable)
    print("\nGenerating churn predictions for dashboard dataset...")
    best_pred = best_pipeline.predict(X_test)
    best_prob = best_pipeline.predict_proba(X_test)[:, 1]
    
    # Combine original test features with actual, predicted, and probability columns
    predictions_df = X_test.copy()
    predictions_df["ActualChurn"] = y_test
    predictions_df["PredictedChurn"] = best_pred
    predictions_df["ChurnProbability"] = best_prob
    
    predictions_path = "data/churn_predictions.csv"
    predictions_df.to_csv(predictions_path, index=False)
    print(f"Predictions saved to {predictions_path}. Shape: {predictions_df.shape}")
    
if __name__ == "__main__":
    train_models() train_models()
    
