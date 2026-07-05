from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="Churn Prediction API")

# Load trained model
model = joblib.load("model.pkl")


#  Input schema (VALIDATION + STRUCTURE)
class Customer(BaseModel):
    gender: str = Field(..., example="Male")
    tenure: int = Field(..., ge=0, example=12)
    MonthlyCharges: float = Field(..., ge=0, example=50.0)


# Root endpoint
@app.get("/")
def home():
    return {"message": "API is running successfully"}


# Prediction endpoint
@app.post("/predict")
def predict(data: Customer):
    try:
        # Convert gender to numeric (example encoding)
        gender_map = {"Male": 1, "Female": 0}

        if data.gender not in gender_map:
            raise HTTPException(status_code=400, detail="Invalid gender value")

        gender = gender_map[data.gender]
        tenure = data.tenure
        monthly_charges = data.MonthlyCharges

        # Prepare input for model
        input_data = np.array([[gender, tenure, monthly_charges]])

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Optional probability (if model supports it)
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(input_data)[0][1]
        else:
            prob = None

        # Convert to readable label
        label = "Churn" if prediction == 1 else "No Churn"

        return {
            "prediction": int(prediction),
            "label": label,
            "probability": prob
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))