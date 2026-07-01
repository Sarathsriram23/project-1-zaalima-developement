# Model Explainability using SHAP
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import shap
from sklearn.pipeline import Pipeline
# Make sure to import FeatureEngineer so it can be unpickled properly
from custom_transformers import FeatureEngineer

def explain_model():
    model_path = "models/churn_model.pkl"
    data_path = "data/cleaned_telco.csv"
    
    if not os.path.exists(model_path) or not os.path.exists(data_path):
        print("Model or dataset not found. Please run preprocess.py and train_churn.py first.")
        return
        
    print(f"Loading best model pipeline: {model_path}")
    pipeline = joblib.load(model_path)
    
    print(f"Loading cleaned dataset: {data_path}")
    df = pd.read_csv(data_path)
    
    # Separate features (no manual feature engineering needed!)
    X = df.drop("Churn", axis=1)
    
    # Identify initial categorical columns
    categorical_cols = X.select_dtypes(include="object").columns.tolist()
    
    # Reconstruct the preprocessing pipeline (all steps except the classifier)
    # This runs FeatureEngineer followed by the preprocessor ColumnTransformer
    preprocessor_pipeline = Pipeline(pipeline.steps[:-1])
    X_processed = preprocessor_pipeline.transform(X)
    
    # Extract feature names after encoding from the ColumnTransformer step
    preprocessor = pipeline.named_steps["preprocessor"]
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_features = cat_encoder.get_feature_names_out(categorical_cols).tolist()
    # Programmatically retrieve the scaled numerical columns
    numeric_features = preprocessor.transformers[1][2]
    all_feature_names = cat_features + numeric_features
    
    # Create DataFrame of processed features for SHAP explainer
    X_processed_df = pd.DataFrame(X_processed, columns=all_feature_names)
    
    # Get classifier
    classifier = pipeline.named_steps["classifier"]
    
    print("Calculating SHAP values...")
    # Initialize explainer appropriate for the model
    # For Logistic Regression, we use LinearExplainer
    explainer = shap.Explainer(classifier, X_processed)
    shap_values = explainer(X_processed)
        
    print(f"SHAP values computed. Shape: {shap_values.shape}")
    
    # Generate summary plot
    os.makedirs("reports", exist_ok=True)
    plt.figure(figsize=(10, 6))
    
    # Create a SHAP summary plot and save it
    shap.summary_plot(shap_values, X_processed_df, show=False)
    
    plt.title("SHAP Feature Importance (Customer Churn Model)", fontsize=14, pad=15)
    plt.tight_layout()
    plot_path = "reports/shap_summary_plot.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    print(f"SHAP summary plot saved to {plot_path} successfully!")

if __name__ == "__main__":
    explain_model()
