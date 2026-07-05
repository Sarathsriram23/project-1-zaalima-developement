from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load trained pipeline
model = joblib.load("models/churn_model.pkl")


# Define full input schema
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}


@app.post("/predict")
def predict(data: CustomerData):
    try:
        df = pd.DataFrame([data.dict()])

        # ✅ Create missing feature
        df["AvgChargePerMonth"] = df["TotalCharges"] / df["tenure"]

        # Optional safety (avoid division by zero)
        df["AvgChargePerMonth"] = df["AvgChargePerMonth"].fillna(0)

        prediction = model.predict(df)[0]

        return {
    "prediction": int(prediction),
    "result": "Churn" if prediction == 1 else "No Churn"
}
    except Exception as e:
        return {"error": str(e)}