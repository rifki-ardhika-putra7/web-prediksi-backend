import pandas as pd
from app.models.predictor import predict_from_csv

# Contoh data dummy
data = {
    "nama": ["Tes User"],
    "nilai_akhir": [85],
    "absensi": [90],
    "sikap": ["baik"]
}
df = pd.DataFrame(data)

hasil = predict_from_csv(df)
print(hasil)
