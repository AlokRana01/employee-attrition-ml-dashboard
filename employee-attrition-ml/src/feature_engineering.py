import pandas as pd

def engineer_features(df):
    df = df.copy()

    df['SatisfactionScore'] = (
        df['JobSatisfaction'] +
        df['EnvironmentSatisfaction'] +
        df['RelationshipSatisfaction'] +
        df['WorkLifeBalance']
    ) / 4

    df['IncomePerYear'] = df['MonthlyIncome'] / (df['TotalWorkingYears'] + 1)
    df['PromotionGap'] = df['YearsSinceLastPromotion'] / (df['YearsAtCompany'] + 1)

    df['IsOvertime'] = df['OverTime'].isin(['Yes']).astype(int)
    df['LowSatOvertime'] = ((df['JobSatisfaction'] <= 2) & (df['OverTime'] == 'Yes')).astype(int)
    df['StuckInRole'] = ((df['YearsSinceLastPromotion'] >= 4) & (df['JobLevel'] <= 2)).astype(int)

    return df