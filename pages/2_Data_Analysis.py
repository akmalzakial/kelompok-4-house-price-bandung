import streamlit as st
import pandas as pd
from utils.preprocessing import load_data, clean_data
from utils.visualization import (
    inject_custom_css,
    plot_price_distribution,
    plot_price_by_location,
    plot_scatter_building_vs_price,
    plot_scatter_land_vs_price,
    plot_feature_correlation,
    plot_top_locations
)

# Set page config
st.set_page_config(
    page_title="Analisis Data - Prediksi Harga Rumah Bandung",
    page_icon="📈",
    layout="wide"
)

# Inject custom modern CSS
inject_custom_css()

st.title("📈 Analisis Data Eksploratif (EDA)")
st.markdown("Visualisasi interaktif mengenai faktor-faktor yang memengaruhi harga properti di Kota Bandung.")

try:
    # Load dataset with cache
    @st.cache_data
    def get_analysis_data():
        df_raw = load_data("data/clean_df.csv")
        return clean_data(df_raw)
        
    df = get_analysis_data()
    
    # 1. Distribusi Harga Rumah
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_dist = plot_price_distribution(df)
    st.plotly_chart(fig_dist, use_container_width=True)
    st.markdown("""
    **Insight:** 
    Distribusi harga rumah di Bandung miring ke kanan (*positive skew*). Mayoritas harga rumah berada di kisaran di bawah 
    **Rp 3.0 Miliar**. Namun, terdapat ekor panjang (*long tail*) yang mencapai **Rp 9.7 Miliar**, merepresentasikan perumahan 
    mewah/premium di lokasi-lokasi elite.
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. Top Lokasi Dengan Harga Tertinggi (Horizontal) & Lokasi Bar Chart (Vertical)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
        fig_top = plot_top_locations(df)
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown("""
        **Insight:** 
        Grafik menampilkan 10 wilayah (kecamatan) dengan rata-rata harga tertinggi. Kawasan Bandung Utara dan pusat kota 
        seperti Cidadap, Dago, Coblong, dan Bandung Wetan mendominasi puncak klasemen properti premium.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
        fig_loc = plot_price_by_location(df)
        st.plotly_chart(fig_loc, use_container_width=True)
        st.markdown("""
        **Insight:** 
        Distribusi harga rata-rata berdasarkan wilayah menunjukkan kesenjangan harga yang signifikan. Lokasi strategis 
        memiliki nilai premium per meter persegi yang berkali-kali lipat dibanding daerah pinggiran/suburban.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 3. Luas Bangunan vs Harga & Luas Tanah vs Harga
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
        fig_build = plot_scatter_building_vs_price(df)
        st.plotly_chart(fig_build, use_container_width=True)
        st.markdown("""
        **Insight:** 
        Hubungan antara Luas Bangunan dan Harga cenderung linear positif. Semakin besar luas bangunan, semakin tinggi harga rumah. 
        Variansi sebaran melebar pada rumah ukuran besar, mengindikasikan faktor lain (seperti kualitas material & prestise daerah) 
        mulai mendominasi harga pada properti besar.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col4:
        st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
        fig_land = plot_scatter_land_vs_price(df)
        st.plotly_chart(fig_land, use_container_width=True)
        st.markdown("""
        **Insight:** 
        Luas Tanah berkorelasi positif dengan harga. Properti dengan luas tanah besar memiliki harga dasar tinggi. 
        Beberapa *outliers* menunjukkan tanah sangat luas dengan bangunan minimalis, yang biasanya merepresentasikan 
        investasi spekulasi lahan strategis.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 4. Korelasi Antar Fitur
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_corr = plot_feature_correlation(df)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("""
    **Insight:** 
    Berdasarkan koefisien korelasi, **Luas Bangunan** (korelasi tertinggi) dan **Luas Tanah** adalah dua prediktor terkuat 
    dari harga rumah. Menariknya, jumlah **Kamar Mandi** memiliki korelasi terhadap harga yang sedikit lebih tinggi dibanding 
    jumlah **Kamar Tidur**, menunjukkan bahwa preferensi modern lebih menghargai kenyamanan sanitasi per kamar.
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Dataset tidak ditemukan! Pastikan file CSV berada di `data/clean_df.csv`.")
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat memuat grafik: {str(e)}")