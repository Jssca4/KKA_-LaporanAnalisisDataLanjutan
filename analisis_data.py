import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- MEMBACA FILE TXT ---
file_name = "DataPenjualan.txt"

try:
    # File TXT berformat CSV → gunakan read_csv
    df = pd.read_csv(file_name)
    df = df.dropna()

    # Jika kolom Pendapatan tidak ada → hitung otomatis
    if "Pendapatan" not in df.columns:
        if "Jumlah" in df.columns and "Harga Satuan" in df.columns:
            df["Pendapatan"] = df["Jumlah"] * df["Harga Satuan"]
        else:
            print("ERROR: Tidak ada kolom Pendapatan maupun kolom Jumlah/Harga Satuan.")
            exit()

    df["Pendapatan"] = pd.to_numeric(df["Pendapatan"], errors="coerce")
    df = df.dropna(subset=["Pendapatan"])

    print(f"Data berhasil dimuat. Total baris: {len(df)}")

except Exception as e:
    print("Terjadi error saat membaca file:", e)
    exit()

# --- TAMBAH KOLOM DISKON ---
DISKON_RATE = 0.10
df["Diskon"] = df["Pendapatan"] * DISKON_RATE
df["Pendapatan Bersih"] = df["Pendapatan"] - df["Diskon"]

print("\n--- Contoh Data Akhir ---")
print(df[["Produk", "Pendapatan", "Diskon", "Pendapatan Bersih"]].head())

# --- VISUALISASI ---
df_bersih_per_produk = df.groupby("Produk")["Pendapatan Bersih"].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=df_bersih_per_produk, x="Produk", y="Pendapatan Bersih")
plt.title("Total Pendapatan Bersih per Produk (Diskon 10%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- SIMPAN ---
df.to_csv("analisis_diskon.csv", index=False)
print("\nHasil disimpan sebagai analisis_diskon.csv")

