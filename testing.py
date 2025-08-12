import joblib
import os
import pandas as pd


model_trend = "linear_trend_model.pkl"
model_residual = "xgb_residual_model.pkl"
model_features = "feature_names.pkl"

model_trend_loaded = joblib.load(model_trend)
model_residual_loaded = joblib.load(model_residual)
model_features_loaded = joblib.load(model_features)


