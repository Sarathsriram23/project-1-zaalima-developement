import warnings

warnings.filterwarnings("ignore")



import numpy as np

import pandas as pd



from sklearn.model_selection import train_test_split, RandomizedSearchCV

from sklearn.preprocessing import OneHotEncoder, RobustScaler

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.ensemble import (

    RandomForestRegressor,

    ExtraTreesRegressor,

    GradientBoostingRegressor,

    HistGradientBoostingRegressor

)

from sklearn.linear_model import Ridge, ElasticNet

from sklearn.inspection import permutation_importance

import joblib