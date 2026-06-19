# 🏠 Sistem Prediksi Harga Rumah Kota Bandung

> **Tugas UAS Mata Kuliah Machine Learning — Digitech University**  
> Aplikasi web interaktif berbasis Streamlit untuk memprediksi harga properti rumah di wilayah Bandung Raya menggunakan algoritma regresi Machine Learning.

---

## 👥 Kelompok 4

| No  | Nama                   | NIM      | Role　　　　　　　　　　　　　　　　|
| :---:| :-----------------------| :--------:| :------------------------------------|
| 1   | **Akmal Zaki Alfadly** | 20124078 | 🏗️ Project Lead & App Architecture　|
| 2   | **Azil Rasya Jabari**  | 20124083 | 🔧 Data Engineer & Preprocessing　　|
| 3   | **Kaila Naya**         | 20124095 | 📊 Data Analyst & EDA Visualization |
| 4   | **Ari Aripin**         | 20124108 | 🤖 ML Engineer & Model Training　　 |
| 5   | **Ninda Syaima Zain**  | 20124076 | 📈 Model Evaluator & Comparison　　 |
| 6   | **Edi Suryadi**        | 20125068 | 🔮 Prediction UI & Documentation　　|

---

## 📋 Deskripsi Proyek

Proyek ini adalah sebuah aplikasi web **Machine Learning** interaktif untuk memprediksi harga properti/rumah di wilayah **Bandung Raya** (Kota Bandung, Kabupaten Bandung, dan Kabupaten Bandung Barat) berdasarkan fitur-fitur fisik rumah seperti luas bangunan, luas tanah, lokasi (kecamatan), serta koordinat geografis.

Aplikasi ini menggunakan **5 algoritma regresi** yang dibandingkan performanya:
- **Linear Regression** — Baseline model regresi linier
- **Ridge Regression** — Regularisasi L2 untuk mengurangi overfitting
- **Decision Tree Regressor** — Pohon keputusan tunggal
- **Random Forest Regressor** — Ensemble bagging (Model Utama)
- **Gradient Boosting Regressor** — Ensemble boosting

## 🎯 Tujuan

1. Membantu calon pembeli rumah memperkirakan harga wajar rumah idaman di Bandung Raya.
2. Membantu pemilik properti menentukan harga jual rumah berdasarkan fitur bangunan yang ditawarkan.
3. Memberikan analisis data eksploratif (EDA) yang interaktif mengenai dinamika pasar properti di Kota Bandung.
4. Membandingkan performa beberapa algoritma regresi ML dalam konteks prediksi harga properti.

---

## 📊 Dataset

Dataset yang digunakan berada pada berkas `data/clean_df.csv` yang berisi **32.536 baris** data bersih tanpa *missing value*.

| Fitur | Tipe | Keterangan |
|:---|:---|:---|
| `Price` | Float | **Target** — Harga rumah (IDR) |
| `Location` | String | Nama kecamatan |
| `City/Regency` | String | Kota/Kabupaten |
| `Bedroom` | Integer | Jumlah kamar tidur (1–8) |
| `Bathroom` | Integer | Jumlah kamar mandi (1–7) |
| `Carport` | Integer | Kapasitas parkir (0–3) |
| `Land` | Float | Luas tanah (m²) |
| `Building` | Float | Luas bangunan (m²) |
| `Month` | Integer | Bulan pengambilan data (8, 9, 10) |
| `Latitude` | Float | Koordinat lintang |
| `Longitude` | Float | Koordinat bujur |

---

## 🤖 Performa Model Utama (Random Forest)

| Metrik | Nilai |
|:---|:---|
| **R² Score** | `0.8626` (86.26%) |
| **MAE** | Rp 410.940.076 (~411 Juta) |
| **RMSE** | Rp 692.664.969 (~693 Juta) |

---

## 🗂️ Struktur Folder

```text
house-price-bandung/
│
├── app.py                        # 🏠 Landing Page Utama (Akmal)
│
├── data/
│   └── clean_df.csv              # 📂 Dataset CSV Bersih (Azil)
│
├── models/
│   ├── random_forest_model.pkl   # 🤖 Model Utama RF (Ari)
│   ├── model_comparison.pkl      # 📊 Bundle Perbandingan 5 Model (Ari & Ninda)
│   ├── linear_regression_model.pkl
│   ├── ridge_regression_model.pkl
│   ├── decision_tree_model.pkl
│   └── gradient_boosting_model.pkl
│
├── pages/
│   ├── 1_Dashboard.py            # 📊 Ringkasan & Preview Data (Akmal)
│   ├── 2_Data_Analysis.py        # 📈 Visualisasi EDA Interaktif (Kaila)
│   ├── 3_Model_Evaluation.py     # 🤖 Evaluasi & Perbandingan Model (Ninda)
│   └── 4_House_Prediction.py     # 🔮 Form Prediksi Harga (Edi)
│
├── utils/
│   ├── preprocessing.py          # 🔧 Loading & Encoding Data (Azil)
│   ├── training.py               # ⚙️ Training Pipeline Model (Ari)
│   ├── prediction.py             # 🎯 Load Model & Inference (Edi)
│   └── visualization.py          # 🎨 Visualisasi Plotly & CSS (Kaila & Ninda)
│
├── notebooks/                    # 📓 Jupyter Notebook Eksplorasi
│
├── assets/
│   └── logo.png                  # 🖼️ Logo Aplikasi
│
├── laporan_model.md              # 📝 Laporan Teknis Model (Edi)
├── tugas_role.md                 # 📋 Pembagian Tugas & Saran Commit
├── requirements.txt              # 📦 Dependensi Python
├── .gitignore                    # 🚫 File yang Diabaikan Git
└── README.md                     # 📖 Dokumentasi Utama (Akmal)
```

---

## ⚙️ Tech Stack

| Komponen | Teknologi |
|:---|:---|
| Bahasa | Python 3.10+ |
| Framework Web | Streamlit |
| Visualisasi | Plotly Express, Plotly Graph Objects |
| Machine Learning | scikit-learn (RandomForest, Ridge, GBR, dll) |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |

---

## 🚀 Cara Instalasi & Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/Akmalz26/kelompok-4-machine-learning.git
cd kelompok-4-machine-learning
```

### 2. Buat Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

Buka browser dan akses `http://localhost:8501`.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis Tugas UAS Mata Kuliah **Machine Learning** di **Digitech University**.

---

<div align="center">
  <b>Kelompok 4 — Machine Learning — Digitech University © 2026</b>
</div>