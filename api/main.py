# FastAPI Application Server for Churn & LTV Engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
import numpy as np
import joblib
import os
import sys
from contextlib import asynccontextmanager

# Add scripts directory to path for unpickling Custom Transformers
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.abspath(os.path.join(current_dir, "..", "scripts"))
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

from custom_transformers import FeatureEngineer
from database import get_db
from schemas import CustomerInput, ChurnResponse, LTVResponse, CustomerPredictionResponse

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Resolve absolute paths
    churn_model_path = os.path.abspath(os.path.join(current_dir, "..", "models", "churn_model.pkl"))
    ltv_model_path = os.path.abspath(os.path.join(current_dir, "..", "models", "ltv_model.pkl"))
    
    # Load model pipelines
    print(f"Loading churn model pipeline from {churn_model_path}...")
    if not os.path.exists(churn_model_path):
        raise FileNotFoundError(f"Model file not found at: {churn_model_path}")
    models["churn"] = joblib.load(churn_model_path)
    
    print(f"Loading LTV model pipeline from {ltv_model_path}...")
    if not os.path.exists(ltv_model_path):
        raise FileNotFoundError(f"Model file not found at: {ltv_model_path}")
    models["ltv"] = joblib.load(ltv_model_path)
    
    yield
    models.clear()

app = FastAPI(
    title="Telco Customer Churn & LTV Prediction API",
    description="REST API for predicting churn risk and Customer Lifetime Value (LTV).",
    version="1.0.0",
    lifespan=lifespan
)

def preprocess_and_predict(df_input: pd.DataFrame):
    # Ensure TotalCharges is numeric and handle missing values
    df_input["TotalCharges"] = pd.to_numeric(df_input["TotalCharges"], errors="coerce")
    # Median fallback for TotalCharges if NaN
    df_input["TotalCharges"] = df_input["TotalCharges"].fillna(700.5)
    
    # Columns expected by Churn model pipeline (exactly 19 features)
    expected_cols = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
        "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ]
    
    df_churn_input = df_input[expected_cols].copy()
    
    # 1. Predict Churn first
    churn_prob = float(models["churn"].predict_proba(df_churn_input)[:, 1][0])
    churn_pred = int(models["churn"].predict(df_churn_input)[0])
    
    # 2. Inject predicted churn as a feature for the LTV model (matches LTV model's training columns)
    df_ltv_input = df_churn_input.copy()
    df_ltv_input["Churn"] = churn_pred
    
    # 3. Predict LTV
    ltv_pred = float(models["ltv"].predict(df_ltv_input)[0])
    
    return churn_pred, churn_prob, ltv_pred

@app.post("/predict_churn", response_model=ChurnResponse, tags=["Predictions"])
def predict_churn(customer: CustomerInput):
    """
    Predicts the churn probability and classification (1 = Churn, 0 = Retained) for a customer.
    """
    try:
        df_input = pd.DataFrame([customer.dict()])
        churn_pred, churn_prob, _ = preprocess_and_predict(df_input)
        return ChurnResponse(churn_probability=churn_prob, predicted_churn=churn_pred)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict_ltv", response_model=LTVResponse, tags=["Predictions"])
def predict_ltv(customer: CustomerInput):
    """
    Predicts the Customer Lifetime Value (LTV) in USD for a customer.
    """
    try:
        df_input = pd.DataFrame([customer.dict()])
        _, _, ltv_pred = preprocess_and_predict(df_input)
        return LTVResponse(estimated_ltv=ltv_pred)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict_all", response_model=CustomerPredictionResponse, tags=["Predictions"])
def predict_all(customer: CustomerInput):
    """
    Predicts both Churn risk and Lifetime Value (LTV) for a customer.
    """
    try:
        df_input = pd.DataFrame([customer.dict()])
        churn_pred, churn_prob, ltv_pred = preprocess_and_predict(df_input)
        return CustomerPredictionResponse(
            predicted_churn=churn_pred,
            churn_probability=churn_prob,
            estimated_ltv=ltv_pred
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/predict_customer/{customer_id}", response_model=CustomerPredictionResponse, tags=["Database Integration"])
def predict_customer(customer_id: str, db: Session = Depends(get_db)):
    """
    Queries a customer record by ID from the database, feeds their features into the ML models,
    and returns both Churn and LTV predictions.
    """
    query = text("SELECT * FROM telco_customers WHERE customerID = :cid")
    try:
        result = db.execute(query, {"cid": customer_id}).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
        
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer ID '{customer_id}' not found in database.")
        
    # Convert Row object to dictionary
    try:
        row_dict = dict(result._mapping)
    except AttributeError:
        # Fallback for older SQLAlchemy versions
        row_dict = dict(zip(result.keys(), result))
        
    df_input = pd.DataFrame([row_dict])
    
    try:
        churn_pred, churn_prob, ltv_pred = preprocess_and_predict(df_input)
        return CustomerPredictionResponse(
            predicted_churn=churn_pred,
            churn_probability=churn_prob,
            estimated_ltv=ltv_pred
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction execution error: {str(e)}")

@app.get("/", tags=["General"])
def index():
    return {
        "status": "online",
        "message": "Welcome to the Telco Customer Churn & LTV API. Visit /docs for Swagger UI documentation."
    }
