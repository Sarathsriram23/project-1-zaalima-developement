from fastapi import FastAPI, Depends
import joblib
import pandas as pd
from api.database import get_db

app = FastAPI()

model = joblib.load("models/logistic_regression.pkl")

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data]) # FIX: wrap in list

        prediction = model.predict(df)

        return {"prediction": int(prediction[0])}

    except Exception as e:
        return {"error": str(e)}