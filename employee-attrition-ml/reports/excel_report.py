import pandas as pd
from io import BytesIO

def generate_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attrition Report')

    output.seek(0)
    return output