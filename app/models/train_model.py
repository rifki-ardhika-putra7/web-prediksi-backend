# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from imblearn.over_sampling import SMOTE
import os

# Path dataset
csv_path = os.path.abspath("../dataset/dummy_dataset_balanced.csv")
df = pd.read_csv(csv_path)

# Konversi 'sikap' ke angka
sikap_mapping = {'kurang': 0, 'cukup': 1, 'baik': 2}
df['sikap_encoded'] = df['sikap'].map(sikap_mapping)

# Fitur & label
X = df[['nilai_akhir', 'absensi', 'sikap_encoded']]
y = df['status']

# Cek distribusi awal
print("Distribusi sebelum SMOTE:\n", y.value_counts())

# Balancing pakai SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)

# Cek distribusi sesudah SMOTE
print("Distribusi setelah SMOTE:\n", pd.Series(y_res).value_counts())

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Simpan model
joblib.dump(model, "model_kelulusan_balanced.pkl")
print("✅ Model berhasil dilatih & disimpan sebagai model_kelulusan_balanced.pkl")
