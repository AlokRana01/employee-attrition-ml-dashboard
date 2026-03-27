import pandas as pd
from config import CAT_COLS, ALL_FEATURES
from src.feature_engineering import engineer_features

def score_dataframe(df, model, encoders):
    df_original = df.copy()   # ✅ keep original for UI

    df_model = df.copy()      # ✅ separate copy for ML

    df_model = engineer_features(df_model)

    # Encode ONLY in model dataframe
    for col in CAT_COLS:
        le = encoders[col]
        df_model[col] = df_model[col].apply(
            lambda x: x if x in le.classes_ else le.classes_[0]
        )
        df_model[col] = le.transform(df_model[col])

    X = df_model[ALL_FEATURES]

    df_original['RiskScore'] = model.predict_proba(X)[:,1] * 100

    return df_original