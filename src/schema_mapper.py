import pandas as pd

# Possible column variations
COLUMN_MAP = {
    "Age": ["age"],
    "Department": ["department", "dept"],
    "JobRole": ["jobrole", "role", "position"],
    "OverTime": ["overtime", "ot"],
    "MonthlyIncome": ["monthlyincome", "salary", "income"],
    "Attrition": ["attrition", "left", "resigned", "exit"]
}

def map_columns(df):
    df = df.copy()
    new_columns = {}

    for standard, variations in COLUMN_MAP.items():
        for col in df.columns:
            if col.lower() in variations:
                new_columns[col] = standard

    df = df.rename(columns=new_columns)

    return df