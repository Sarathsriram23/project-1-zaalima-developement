import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Title
# -----------------------------
st.title("Customer Churn Prediction Dashboard")

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/logistic_regression.pkl")

model = load_model()

# -----------------------------
# Data Source Selection
# -----------------------------
st.sidebar.header("Data Source")

option = st.sidebar.radio(
    "Choose data source:",
    ("Use default dataset", "Upload your own CSV")
)

# -----------------------------
# Load Data
# -----------------------------
data = None

if option == "Use default dataset":
    try:
        data = pd.read_csv("data/churn_predictions.csv")
        st.success("Loaded default dataset successfully ")
    except Exception as e:
        st.error(f"Error loading default dataset: {e}")

else:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully ")

# -----------------------------
# Process Data
# -----------------------------
if data is not None:

    st.subheader(" Data Preview")
    st.dataframe(data.head())

    try:
        # -----------------------------
        # Prediction
        # -----------------------------
        predictions = model.predict(data)

        data["Churn Prediction"] = predictions

        st.subheader("Predictions")
        st.dataframe(data)

        # -----------------------------
        # Download Results
        # -----------------------------
        csv = data.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Predictions",
            data=csv,
            file_name="churn_predictions_output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.warning("Make sure your dataset has the SAME structure as training data.")