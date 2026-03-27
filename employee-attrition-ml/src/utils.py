def risk_level(score):
    if score >= 60:
        return "High"
    elif score >= 35:
        return "Medium"
    return "Low"