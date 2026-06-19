import streamlit as st
import numpy as np
# Mengimpor fungsi grafik yang sudah kita buat di folder utils
from utils.visualization import plot_predicted_vs_actual, plot_residuals

st.title("📊 Evaluasi Performa Model")
st.markdown("Analisis hasil pelatihan model regresi beserta perbandingan performa antar algoritma.")

# Membuat Menu Tab Utama
tab1, tab2 = st.tabs(["🎯 Model Utama (Random Forest)", "📈 Perbandingan Semua Model"])

# Membuat data bohongan (dummy) hanya untuk mengetes apakah grafiknya muncul
np.random.seed(42)
y_actual = np.random.randint(100, 500, size=100)
y_pred = y_actual + np.random.normal(0, 30, size=100)

with tab1:
    st.header("Evaluasi Model Utama")
    st.subheader("1. Scatter Plot Prediksi vs Aktual")
    
    # Memanggil fungsi Commit 1
    fig1 = plot_predicted_vs_actual(y_actual, y_pred)
    st.pyplot(fig1)
    
    st.subheader("2. Distribusi Residual")
    # Memanggil fungsi Commit 2
    fig2 = plot_residuals(y_actual, y_pred)
    st.pyplot(fig2)

with tab2:
    st.header("Perbandingan Semua Model")
    st.write("Tempat tabel metrik perbandingan model akan diletakkan di sini.")