# Custom Scikit-Learn Transformers for Model Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom transformer to perform feature engineering inside the Scikit-Learn Pipeline.
    Calculates Average Charge per Month to prevent data leakage and simplify deployment.
    """
    def __init__(self):
        super().__init__()
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Create a copy to prevent modifying the original dataframe
        X_copy = X.copy()
        
        # Calculate Average Charge per Month
        # Adding 1 to tenure prevents division by zero for new customers
        X_copy["AvgChargePerMonth"] = X_copy["TotalCharges"] / (X_copy["tenure"] + 1)
        
        return X_copy
