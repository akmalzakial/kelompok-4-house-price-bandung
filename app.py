# pyrefly: ignore [missing-import]
import streamlit as st
import os
import textwrap
# pyrefly: ignore [missing-import]
from utils.visualization import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="Prediksi Harga Rumah Bandung",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom modern CSS
inject_custom_css()

# Sidebar branding
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px 0;'>
    <h2>🏠 Bandung House Predictor</h2>
    <p style='color: #64748B; font-size: 14px;'>Random Forest Regressor App</p>
</div>
<hr style='margin-top: 0; margin-bottom: 20px;' />
""", unsafe_allow_html=True)

# Try to show logo in sidebar if available
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.info("Gunakan navigasi di atas untuk berpindah halaman.")

# Main page layout
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #2563EB; font-size: 2.5rem; margin-bottom: 5px;'>Sistem Prediksi Harga Rumah di Kota Bandung</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #64748B; font-weight: 500; margin-top: 0; margin-bottom: 20px;'>Menggunakan Random Forest Regressor</h3>", unsafe_allow_html=True)

st.markdown("""
Aplikasi ini dikembangkan untuk memprediksi harga properti/rumah di wilayah Bandung Raya (Kota Bandung, Kabupaten Bandung, dan Bandung Barat) secara akurat berdasarkan fitur-fitur fisik rumah. Sistem backend menggunakan algoritma **Random Forest Regressor** yang dilatih menggunakan puluhan ribu data riil transaksi rumah di Bandung.
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Grid layout for system highlights
col1, col2 = st.columns(2)

with col1:
    st.markdown(textwrap.dedent("""
    <div class='custom-card' style='height: 100%;'>
        <h3 style='color: #0F172A; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px; margin-bottom: 15px;'>🚀 Navigasi Halaman</h3>
        <ul style='padding-left: 20px; line-height: 1.8;'>
            <li><b>Dashboard:</b> Ringkasan data, dimensi dataset, statistik harga, dan peninjauan langsung baris data.</li>
            <li><b>Analisis Data:</b> Visualisasi interaktif seperti distribusi harga, korelasi fitur, analisis harga berdasarkan lokasi, dan luas bangunan/tanah.</li>
            <li><b>Evaluasi Model:</b> Detail training, nilai metrik evaluasi ($R^2$, MAE, RMSE), sebaran residual error, dan peringkat kepentingan fitur.</li>
            <li><b>Prediksi Harga Rumah:</b> Form input interaktif untuk menghitung taksiran nilai pasar rumah secara instan.</li>
        </ul>
    </div>
    """), unsafe_allow_html=True)

with col2:
    st.markdown(textwrap.dedent("""
    <div class='custom-card' style='height: 100%;'>
        <h3 style='color: #0F172A; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px; margin-bottom: 15px;'>⚙️ Pipeline Machine Learning</h3>
        <p>Proses pemodelan kami terintegrasi secara modular:</p>
        <ol style='padding-left: 20px; line-height: 1.7;'>
            <li><b>Cleaning:</b> Menghapus data duplikat dan membersihkan indeks kosong.</li>
            <li><b>Encoding:</b> Mengubah kolom teks seperti <i>Location</i> dan <i>City/Regency</i> dengan <code>LabelEncoder</code>.</li>
            <li><b>Pemodelan:</b> Regresi menggunakan <code>RandomForestRegressor</code> dengan 200 estimator dan kedalaman maksimal 15.</li>
            <li><b>Cashing & Evaluasi:</b> Mematangkan model dengan split 80:20 dan caching sumber daya untuk performa yang optimal.</li>
        </ol>
    </div>
    """), unsafe_allow_html=True)

st.markdown("""
<div class='custom-card' style='text-align: center; background-color: #EFF6FF !important; border-color: #BFDBFE !important;'>
    <h4 style='color: #1E40AF; margin-bottom: 10px;'>Mulai Eksplorasi Sekarang</h4>
    <p style='color: #1E3A8A; font-size: 14px;'>Silakan klik menu <b>Dashboard</b> di sidebar sebelah kiri untuk melihat ringkasan data awal.</p>
</div>
""", unsafe_allow_html=True)
