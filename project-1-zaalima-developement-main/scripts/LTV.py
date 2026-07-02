df["ExpectedRevenue"] = (
    df["MonthlyCharges"] *
    (df["tenure"] + (1 - df["Churn"]) * 12)
)

active_df = df[df["Churn"] == 0].copy()

active_df

active_df["ExpectedRevenue"] = (
    active_df["MonthlyCharges"] *
    (active_df["tenure"] + 12)
)

X = active_df.drop(
    ["ExpectedRevenue", "Churn"],
    axis=1
)

y = active_df["ExpectedRevenue"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "XGBoost": XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        random_state=42
    )
}

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", model)
])

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test,
        predictions,
        squared=False
    )
    r2 = r2_score(y_test, predictions)

    print(name)
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R²  :", r2)

    best_rmse = float("inf")

    explainer = shap.LinearExplainer(
    model,
    X_test_transformed
)

active_df["Predicted_LTV"] = best_pipeline.predict(
    X
)

active_df["LTV_Segment"] = pd.qcut(
    active_df["Predicted_LTV"],
    q=3,
    labels=["Low", "Medium", "High"]
)