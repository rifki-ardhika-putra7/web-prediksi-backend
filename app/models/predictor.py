import pandas as pd
from app.models.loader import load_model

model = load_model()

def predict_from_csv(df: pd.DataFrame):
    required_cols = ['nama', 'nilai_akhir', 'absensi', 'sikap']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df = df.copy()
    sikap_mapping = {'kurang': 0, 'cukup': 1, 'baik': 2}
    df['sikap_encoded'] = df['sikap'].map(sikap_mapping)

    df['nilai_akhir'] = pd.to_numeric(df['nilai_akhir'], errors='coerce')
    df['absensi'] = pd.to_numeric(df['absensi'], errors='coerce')
    df['sikap_encoded'] = pd.to_numeric(df['sikap_encoded'], errors='coerce')

    needed = ['nilai_akhir', 'absensi', 'sikap_encoded']
    if df[needed].isnull().any().any():
        raise ValueError("Invalid data: ada NaN / non-numeric")

    preds = model.predict(df[needed])
    probs = model.predict_proba(df[needed])

    results = []
    for i in range(len(df)):
        results.append({
            "nama": df.iloc[i]['nama'],
            "nilai_akhir": float(df.iloc[i]['nilai_akhir']),
            "absensi": float(df.iloc[i]['absensi']),
            "sikap": df.iloc[i]['sikap'],
            "predicted_status": "lulus" if int(preds[i]) == 1 else "tidak lulus",
            "probability": round(float(probs[i][1]), 4)
        })
    return results
