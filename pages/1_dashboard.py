import streamlit as st
import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
from utils.preprocessing import load_data, clean_data
# pyrefly: ignore [missing-import]
from utils.visualization import inject_custom_css, render_metric_cards, format_price_idr

# Set page configs
st.set_page_config(
    page_title="Dashboard - Prediksi Harga Rumah Bandung",
    page_icon="📊",
    layout="wide"
)

# Inject modern CSS styles
inject_custom_css()

st.title("Dashboard Properti Bandung")
st.markdown("Ringkasan data, informasi metadata, dan pratinjau dataset properti di wilayah Bandung.")

try:
    # Load dataset with cache
    @st.cache_data
    def get_dashboard_data():
        df_raw = load_data("data/clean_df.csv")
        return clean_data(df_raw)
        
    df = get_dashboard_data()
    
    # 1. Ringkasan Dataset (Metric Cards)
    st.subheader("Ringkasan Properti")
    
    total_data = len(df)
    avg_price = df['Price'].mean()
    max_price = df['Price'].max()
    min_price = df['Price'].min()
    
    metrics = [
        {"title": "Total Data Rumah", "value": f"{total_data:,}"},
        {"title": "Rata-rata Harga", "value": format_price_idr(avg_price)},
        {"title": "Harga Tertinggi", "value": format_price_idr(max_price)},
        {"title": "Harga Terendah", "value": format_price_idr(min_price)}
    ]
    render_metric_cards(metrics)
    
    # Space spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Informasi Dataset & Metadata
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Informasi Dataset")
        
        # Calculate summary table
        missing_count = df.isnull().sum().sum()
        
        metadata_df = pd.DataFrame({
            "Metadata": ["Jumlah Baris", "Jumlah Kolom", "Total Missing Value", "Jumlah Duplikat (Dibersihkan)"],
            "Nilai": [f"{df.shape[0]:,}", f"{df.shape[1]}", f"{missing_count}", "0 (Telah Dihapus)"]
        })
        
        st.dataframe(metadata_df, hide_index=True, use_container_width=True)
        
    with col2:
        st.subheader("Fitur & Tipe Data")
        
        # Build features information table
        features_info = []
        for col in df.columns:
            features_info.append({
                "Nama Fitur": col,
                "Tipe Data": str(df[col].dtype),
                "Missing Value": df[col].isnull().sum(),
                "Peran": "Target" if col == 'Price' else "Fitur (Prediktor)"
            })
            
        st.dataframe(pd.DataFrame(features_info), hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Preview Dataset
    st.subheader("🔍 Preview Data (100 Baris Pertama)")
    st.dataframe(df.head(100), use_container_width=True)

except FileNotFoundError as e:
    st.error("❌ Dataset tidak ditemukan!")
    st.warning("Pastikan file dataset berada di `data/clean_df.csv` sesuai struktur proyek.")
    st.info("Silakan unggah atau tempatkan data/clean_df.csv di folder kerja.")
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat membaca dataset: {str(e)}")
