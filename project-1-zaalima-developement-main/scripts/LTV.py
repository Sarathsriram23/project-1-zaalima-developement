# train and evaluate LTV regression models
import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from custom_transformers import FeatureEngineer

def train_ltv():
    # 1. Load data
    data_path = "data/cleaned_telco.csv"
    if not os.path.exists(data_path):
        print(f"Cleaned dataset not found at: {data_path}")
        return
        
    print(f"Loading cleaned dataset: {data_path}")
    df = pd.read_csv(data_path)
    
    # 2. Compute target variable EstimatedLTV (MonthlyCharges * tenure)
    print("Computing target variable EstimatedLTV...")
    df["EstimatedLTV"] = df["MonthlyCharges"] * df["tenure"]
    
    # 3. Separate features and target
    X = df.drop(["EstimatedLTV"], axis=1)
    y = df["EstimatedLTV"]
    
    # 4. Identify categorical and numeric columns
    categorical_cols = X.select_dtypes(include="object").columns.tolist()
    # Add engineered column to numeric_cols so the ColumnTransformer scales it
    numeric_cols = X.select_dtypes(exclude="object").columns.tolist() + ["AvgChargePerMonth"]
    
    print(f"Categorical features ({len(categorical_cols)}): {categorical_cols}")
    print(f"Numeric features ({len(numeric_cols)}): {numeric_cols}")
    
    # 5. Define ColumnTransformer for preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )
    
    # 6. Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # 7. Initialize regressor models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    # 8. Train and evaluate each regressor pipeline
    results = {}
    best_r2 = -1
    best_model_name = ""
    best_pipeline = None
    
    os.makedirs("models", exist_ok=True)
    
    for name, model in models.items():
        print(f"\n================ Training {name} ================")
        pipeline = Pipeline(steps=[
            ("feature_engineering", FeatureEngineer()),
            ("preprocessor", preprocessor),
            ("regressor", model)
        ])
        
        # Fit pipeline
        pipeline.fit(X_train, y_train)
        
        # Predict
        y_pred = pipeline.predict(X_test)
        
        # Metrics
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        results[name] = {
            "R2 Score": r2,
            "MAE": mae,
            "RMSE": rmse
        }
        
        print(f"R² Score:  {r2:.4f}")
        print(f"MAE:       ${mae:.2f}")
        print(f"RMSE:      ${rmse:.2f}")
        
        # Save model pipeline
        model_filename = f"models/{name.lower().replace(' ', '_')}.pkl"
        joblib.dump(pipeline, model_filename)
        print(f"Saved {name} model pipeline to {model_filename}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline
            
    # 9. Print comparison summary
    print("\n================ Regressor Comparison Summary ================")
    summary_df = pd.DataFrame(results).T
    print(summary_df)
    
    print(f"\nBest LTV Model: {best_model_name} with R²: {best_r2:.4f}")
    
    # Save best model to standard location
    joblib.dump(best_pipeline, "models/ltv_model.pkl")
    print("Saved best LTV model pipeline to models/ltv_model.pkl")
    
if __name__ == "__main__":
    train_ltv()