import pandas as pd
from config import NUM_COLS, CAT_COLS
from src.feature_engineering import engineer_features
from src.schema_mapper import map_columns

def load_and_clean(source):
    df = pd.read_csv(source)

    # ✅ Step 1: Auto map columns
    df = map_columns(df)

    # ✅ Step 2: Validate target
    if 'Attrition' not in df.columns:
        raise ValueError(
            "❌ Target column not found.\n"
            "Rename your column to 'Attrition' or similar (left/resigned)."
        )

    # ✅ Step 3: Normalize target
    df['Attrition'] = df['Attrition'].astype(str).str.lower()

    df['Left'] = df['Attrition'].apply(
        lambda x: 1 if any(k in x for k in ['yes','resign','left','exit']) else 0
    )

    # ✅ Step 4: Handle missing columns
    for col in NUM_COLS:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].median(), inplace=True)

    for col in CAT_COLS:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col].fillna(df[col].mode()[0], inplace=True)

    # ✅ Step 5: Feature engineering (safe)
    df = engineer_features(df)

    return df