# Pydantic Schemas for Request/Response Validation
from pydantic import BaseModel, Field

class CustomerInput(BaseModel):
    """
    Validates the input JSON containing all 19 customer features.
    Matches the schema expected by the ColumnTransformer and pipeline.
    """
    gender: str = Field(description="Gender of the customer (Male/Female)")
    SeniorCitizen: int = Field(description="Is the customer a senior citizen? (1/0)", ge=0, le=1)
    Partner: str = Field(description="Does the customer have a partner? (Yes/No)")
    Dependents: str = Field(description="Does the customer have dependents? (Yes/No)")
    tenure: int = Field(description="Number of months the customer has stayed", ge=0)
    PhoneService: str = Field(description="Does the customer have a phone service? (Yes/No)")
    MultipleLines: str = Field(description="Does the customer have multiple lines? (Yes/No/No phone service)")
    InternetService: str = Field(description="Customer's internet service provider (DSL/Fiber optic/No)")
    OnlineSecurity: str = Field(description="Does the customer have online security? (Yes/No/No internet service)")
    OnlineBackup: str = Field(description="Does the customer have online backup? (Yes/No/No internet service)")
    DeviceProtection: str = Field(description="Does the customer have device protection? (Yes/No/No internet service)")
    TechSupport: str = Field(description="Does the customer have tech support? (Yes/No/No internet service)")
    StreamingTV: str = Field(description="Does the customer have streaming TV? (Yes/No/No internet service)")
    StreamingMovies: str = Field(description="Does the customer have streaming movies? (Yes/No/No internet service)")
    Contract: str = Field(description="The contract term of the customer (Month-to-month/One year/Two year)")
    PaperlessBilling: str = Field(description="Does the customer have paperless billing? (Yes/No)")
    PaymentMethod: str = Field(description="The payment method (Electronic check/Mailed check/Bank transfer (automatic)/Credit card (automatic))")
    MonthlyCharges: float = Field(description="The amount charged to the customer monthly", ge=0.0)
    TotalCharges: float = Field(description="The total amount charged to the customer", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 1,
                "PhoneService": "No",
                "MultipleLines": "No phone service",
                "InternetService": "DSL",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "No",
                "StreamingMovies": "No",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 29.85,
                "TotalCharges": 29.85
            }
        }

class ChurnResponse(BaseModel):
    churn_probability: float = Field(description="Probability of customer churning (0.0 to 1.0)")
    predicted_churn: int = Field(description="Binary classification prediction: 1 = Churn, 0 = Retained")

class LTVResponse(BaseModel):
    estimated_ltv: float = Field(description="Estimated Customer Lifetime Value in USD")

class CustomerPredictionResponse(BaseModel):
    predicted_churn: int
    churn_probability: float
    estimated_ltv: float
