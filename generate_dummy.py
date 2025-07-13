import pandas as pd
import random

# Parameter
total_data = 300  # total jumlah data dummy
target_balance = 0.5  # proporsi lulus (50%)

# List nama depan & belakang
first_names = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eka', 'Fajar', 'Gita', 'Hadi', 'Indra', 'Joko', 'Kiki', 'Lina', 'Mira', 'Nina', 'Oki', 'Putri', 'Rizki', 'Sari', 'Tono', 'Wawan']
last_names = ['Pratama', 'Wijaya', 'Saputra', 'Hidayat', 'Purnama', 'Kusuma', 'Santoso', 'Utami', 'Setiawan', 'Rahmawati']

data = []

for i in range(total_data):
    # nama random
    nama = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # random sikap
    sikap = random.choices(['baik', 'cukup', 'kurang'], weights=[0.4, 0.4, 0.2])[0]
    
    # random nilai dan absensi sesuai sikap
    if sikap == 'baik':
        nilai_akhir = random.randint(75, 100)
        absensi = random.randint(75, 100)
    elif sikap == 'cukup':
        nilai_akhir = random.randint(65, 90)
        absensi = random.randint(60, 95)
    else:  # kurang
        nilai_akhir = random.randint(50, 85)
        absensi = random.randint(50, 90)
    
    # tentukan status
    if nilai_akhir > 75 and absensi > 75 and sikap != 'kurang':
        status = 1
    else:
        status = 0
    
    data.append([nama, nilai_akhir, absensi, sikap, status])

# Buat DataFrame
df = pd.DataFrame(data, columns=['nama', 'nilai_akhir', 'absensi', 'sikap', 'status'])

# Cek distribusi awal
print("Distribusi awal:\n", df['status'].value_counts())

# Tambahkan data dummy kalau perlu biar seimbang
count_1 = df['status'].sum()
count_0 = len(df) - count_1

while count_1 < target_balance * total_data:
    nama = f"{random.choice(first_names)} {random.choice(last_names)}"
    nilai_akhir = random.randint(80, 100)
    absensi = random.randint(80, 100)
    sikap = 'baik'
    status = 1
    df = pd.concat([df, pd.DataFrame([[nama, nilai_akhir, absensi, sikap, status]], 
                                     columns=['nama', 'nilai_akhir', 'absensi', 'sikap', 'status'])],
                   ignore_index=True)
    count_1 += 1

# Cek distribusi akhir
print("\nDistribusi setelah balancing:\n", df['status'].value_counts())

# Simpan ke CSV
df.to_csv("dummy_dataset_balanced2.csv", index=False)
print("✅ Dummy dataset balanced berhasil dibuat dan disimpan.")
