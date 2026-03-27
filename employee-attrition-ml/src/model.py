from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
from config import CAT_COLS, ALL_FEATURES

def train_model(df):
    df_enc = df.copy()
    encoders = {}

    for col in CAT_COLS:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df_enc[col])
        encoders[col] = le

    X = df_enc[ALL_FEATURES]
    y = df_enc['Left']

    if len(y.unique()) < 2:
        raise ValueError("❌ Dataset must have both classes (Yes/No)")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)

    auc = roc_auc_score(y_test, y_prob[:,1]) if y_prob.shape[1] > 1 else 0.5

    return model, encoders, auc