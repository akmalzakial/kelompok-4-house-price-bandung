import streamlit as st

# Mengatur judul halaman utama web
st.title("📊 Evaluasi Performa Model")
st.markdown("Analisis hasil pelatihan model regresi beserta perbandingan performa antar algoritma.")

# Membuat Menu Tab Utama (Commit 2)
tab1, tab2 = st.tabs(["🎯 Model Utama (Random Forest)", "📈 Perbandingan Semua Model"])

with tab1:
    st.header("Evaluasi Model Utama")
    st.write("Tempat grafik scatter plot dan histogram akan muncul.")

with tab2:
    st.header("Perbandingan Semua Model")
    st.write("Tempat tabel metrik dan perbandingan semua model.")