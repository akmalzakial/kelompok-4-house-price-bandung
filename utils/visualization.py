import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def inject_custom_css():
    """
    Injects custom CSS to style the Streamlit application to resemble a premium SaaS dashboard.
    """
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Font and overall app background styling */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #F8FAFC !important;
            font-family: 'Inter', sans-serif !important;
            color: #0F172A !important;
        }
        
        /* Custom styling for sidebar navigation and profile */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        
        [data-testid="stSidebarNav"] {
            padding-top: 1.5rem !important;
        }
        
        /* Title and headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }
        
        /* Custom layout structures */
        .custom-card {
            background-color: #FFFFFF !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
            border: 1px solid #E2E8F0 !important;
            margin-bottom: 24px !important;
        }
        
        /* Custom premium metric cards */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .metric-card {
            background: #FFFFFF !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid #E2E8F0 !important;
            text-align: left !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .metric-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05) !important;
            border-color: #60A5FA !important;
        }
        
        .metric-title {
            color: #64748B !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 8px !important;
        }
        
        .metric-value {
            color: #2563EB !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }
        
        /* Custom buttons styling */
        .stButton>button {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: 1px solid #2563EB !important;
            padding: 12px 28px !important;
            font-size: 16px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.15), 0 2px 4px -2px rgba(37, 99, 235, 0.15) !important;
            width: 100% !important;
        }
        
        .stButton>button:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.25) !important;
        }
        
        .stButton>button:active {
            transform: translateY(1px) !important;
        }
        
        /* Input and selections */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            font-size: 15px !important;
            padding: 4px 12px !important;
        }
        
        /* Interactive styling for graphs container */
        .graph-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 24px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_metric_cards(metrics_list):
    """
    Renders custom HTML metric cards in a grid layout.
    metrics_list should be a list of dicts: [{'title': 'Label', 'value': 'Value'}]
    """
    cols_html = ""
    for metric in metrics_list:
        cols_html += (
            f'<div class="metric-card">'
            f'<div class="metric-title">{metric["title"]}</div>'
            f'<div class="metric-value">{metric["value"]}</div>'
            f'</div>'
        )
    
    grid_html = f'<div class="metric-grid">{cols_html}</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

def format_price_idr(price):
    """
    Formats price in IDR representation.
    Example: 1,500,000,000 -> Rp 1.50 Miliar or Rp 1.500.000.000
    """
    if price >= 1_000_000_000:
        return f"Rp {price / 1_000_000_000:.2f} Miliar"
    elif price >= 1_000_000:
        return f"Rp {price / 1_000_000:.2f} Juta"
    else:
        return f"Rp {price:,.0f}".replace(",", ".")

# Plotly graphs custom theme helper
def _get_plotly_layout_params(title):
    return {
        'title': {
            'text': title,
            'font': {'family': 'Inter, sans-serif', 'size': 18, 'color': '#0F172A', 'weight': 'bold'},
            'x': 0.05
        },
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'xaxis': {
            'gridcolor': '#F1F5F9',
            'linecolor': '#E2E8F0',
            'tickfont': {'family': 'Inter, sans-serif', 'color': '#64748B'},
            'title': {'font': {'family': 'Inter, sans-serif', 'color': '#0F172A', 'size': 14}}
        },
        'yaxis': {
            'gridcolor': '#F1F5F9',
            'linecolor': '#E2E8F0',
            'tickfont': {'family': 'Inter, sans-serif', 'color': '#64748B'},
            'title': {'font': {'family': 'Inter, sans-serif', 'color': '#0F172A', 'size': 14}}
        },
        'margin': {'t': 60, 'b': 40, 'l': 50, 'r': 30},
        'hovermode': 'closest'
    }

def plot_price_distribution(df):
    """
    Plots the price distribution histogram.
    """
    # Use Billions of IDR for easier reading on the axis
    df_plot = df.copy()
    df_plot['Price_Billion'] = df_plot['Price'] / 1_000_000_000
    
    fig = px.histogram(
        df_plot,
        x="Price_Billion",
        nbins=60,
        color_discrete_sequence=['#2563EB'],
        labels={'Price_Billion': 'Harga (Miliar Rp)', 'count': 'Frekuensi'}
    )
    
    fig.update_layout(**_get_plotly_layout_params("Distribusi Harga Rumah di Bandung"))
    fig.update_traces(
        hovertemplate="Harga: Rp %{x:.2f} Miliar<br>Jumlah Rumah: %{y}"
    )
    return fig

def plot_price_by_location(df):
    """
    Plots average price by location (district) using a bar chart.
    """
    df_loc = df.groupby('Location')['Price'].agg(['mean', 'count']).reset_index()
    df_loc = df_loc.sort_values(by='mean', ascending=False)
    
    # Take top 25 for better visualization readability
    df_loc = df_loc.head(25)
    df_loc['Price_Billion'] = df_loc['mean'] / 1_000_000_000
    
    fig = px.bar(
        df_loc,
        x='Location',
        y='Price_Billion',
        color='Price_Billion',
        color_continuous_scale='Blues',
        labels={'Location': 'Kecamatan / Lokasi', 'Price_Billion': 'Rata-rata Harga (Miliar Rp)'}
    )
    
    layout_params = _get_plotly_layout_params("Rata-rata Harga Rumah Berdasarkan Lokasi (Top 25)")
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_traces(
        hovertemplate="Lokasi: %{x}<br>Rerata Harga: Rp %{y:.2f} Miliar"
    )
    return fig

def plot_scatter_building_vs_price(df):
    """
    Scatter plot comparing Building Area vs House Price.
    """
    df_plot = df.copy()
    df_plot['Price_Billion'] = df_plot['Price'] / 1_000_000_000
    
    fig = px.scatter(
        df_plot,
        x="Building",
        y="Price_Billion",
        color="Price_Billion",
        color_continuous_scale='Blues',
        hover_data={"Location": True, "Bedroom": True, "Bathroom": True, "Building": True, "Price_Billion": False},
        labels={'Building': 'Luas Bangunan (m²)', 'Price_Billion': 'Harga (Miliar Rp)'}
    )
    
    layout_params = _get_plotly_layout_params("Luas Bangunan vs Harga Rumah")
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    fig.update_traces(
        marker=dict(size=6, opacity=0.7),
        hovertemplate="Luas Bangunan: %{x} m²<br>Harga: Rp %{y:.2f} Miliar<br>Lokasi: %{customdata[0]}<br>Kamar: %{customdata[1]} KT / %{customdata[2]} KM"
    )
    return fig

def plot_scatter_land_vs_price(df):
    """
    Scatter plot comparing Land Area vs House Price.
    """
    df_plot = df.copy()
    df_plot['Price_Billion'] = df_plot['Price'] / 1_000_000_000
    
    fig = px.scatter(
        df_plot,
        x="Land",
        y="Price_Billion",
        color="Price_Billion",
        color_continuous_scale='Blues',
        hover_data={"Location": True, "Bedroom": True, "Bathroom": True, "Land": True, "Price_Billion": False},
        labels={'Land': 'Luas Tanah (m²)', 'Price_Billion': 'Harga (Miliar Rp)'}
    )
    
    layout_params = _get_plotly_layout_params("Luas Tanah vs Harga Rumah")
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    fig.update_traces(
        marker=dict(size=6, opacity=0.7),
        hovertemplate="Luas Tanah: %{x} m²<br>Harga: Rp %{y:.2f} Miliar<br>Lokasi: %{customdata[0]}<br>Kamar: %{customdata[1]} KT / %{customdata[2]} KM"
    )
    return fig

def plot_feature_correlation(df):
    """
    Plots heatmap showing correlation between numeric variables.
    """
    # Select only numeric features (excl. coordinates and ID column if exists)
    numeric_cols = ['Price', 'Bedroom', 'Bathroom', 'Carport', 'Land', 'Building', 'Month']
    cols_to_use = [col for col in numeric_cols if col in df.columns]
    
    corr = df[cols_to_use].corr()
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale='Blues',
        labels=dict(x="Fitur", y="Fitur", color="Korelasi"),
        x=cols_to_use,
        y=cols_to_use
    )
    
    fig.update_layout(**_get_plotly_layout_params("Matriks Korelasi Antar Fitur"))
    return fig

def plot_top_locations(df):
    """
    Plots the top 10 locations with highest average price using horizontal bar chart.
    """
    df_top = df.groupby('Location')['Price'].mean().sort_values(ascending=False).head(10).reset_index()
    df_top['Price_Billion'] = df_top['Price'] / 1_000_000_000
    df_top = df_top.sort_values(by='Price_Billion', ascending=True) # Ascending for horizontal bar ordering
    
    fig = px.bar(
        df_top,
        x='Price_Billion',
        y='Location',
        orientation='h',
        color='Price_Billion',
        color_continuous_scale='Blues',
        labels={'Price_Billion': 'Rata-rata Harga (Miliar Rp)', 'Location': 'Lokasi'}
    )
    
    layout_params = _get_plotly_layout_params("Top 10 Lokasi Dengan Rata-rata Harga Tertinggi")
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    fig.update_traces(
        hovertemplate="Lokasi: %{y}<br>Rerata Harga: Rp %{x:.2f} Miliar"
    )
    return fig

# Model Evaluation Visualizations

def plot_predicted_vs_actual(y_test, y_pred):
    """
    Scatter plot comparing Actual Prices vs Predicted Prices.
    """
    y_test_b = np.array(y_test) / 1_000_000_000
    y_pred_b = np.array(y_pred) / 1_000_000_000
    
    # Calculate boundaries
    max_val = max(max(y_test_b), max(y_pred_b))
    
    fig = go.Figure()
    
    # Scatter points
    fig.add_trace(go.Scatter(
        x=y_test_b,
        y=y_pred_b,
        mode='markers',
        marker=dict(color='#2563EB', opacity=0.5, size=6),
        name='Prediksi',
        hovertemplate="Aktual: Rp %{x:.2f} Miliar<br>Prediksi: Rp %{y:.2f} Miliar"
    ))
    
    # Reference Identity line (y=x)
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='#EF4444', dash='dash', width=2),
        name='Garis Sempurna'
    ))
    
    fig.update_layout(
        **_get_plotly_layout_params("Prediksi vs Aktual"),
        xaxis_title="Harga Aktual (Miliar Rp)",
        yaxis_title="Harga Prediksi (Miliar Rp)"
    )
    fig.update_layout(showlegend=False)
    return fig

def plot_residuals(y_test, y_pred):
    """
    Histogram of residual errors.
    """
    residuals_billion = (np.array(y_test) - np.array(y_pred)) / 1_000_000_000
    
    fig = px.histogram(
        x=residuals_billion,
        nbins=50,
        color_discrete_sequence=['#60A5FA'],
        labels={'x': 'Selisih / Residual (Miliar Rp)', 'y': 'Frekuensi'}
    )
    
    fig.update_layout(
        **_get_plotly_layout_params("Distribusi Residual (Error)"),
        xaxis_title="Residual Error (Miliar Rp)",
        yaxis_title="Frekuensi"
    )
    fig.update_traces(
        hovertemplate="Error: Rp %{x:.3f} Miliar<br>Frekuensi: %{y}"
    )
    return fig

def plot_feature_importance(feat_importance_dict):
    """
    Bar chart showing importance score for each feature.
    """
    df_feat = pd.DataFrame([
        {'Fitur': k, 'Pentingnya': v} for k, v in feat_importance_dict.items()
    ])
    # Sort
    df_feat = df_feat.sort_values(by='Pentingnya', ascending=True)
    
    # Translate features name to local Indonesian context if preferred, or keep as is.
    feature_translation = {
        'Location': 'Lokasi',
        'Bedroom': 'Kamar Tidur',
        'Bathroom': 'Kamar Mandi',
        'Carport': 'Carport',
        'Land': 'Luas Tanah',
        'Building': 'Luas Bangunan',
        'Month': 'Bulan Data',
        'City/Regency': 'Kota/Kabupaten',
        'Latitude': 'Latitude',
        'Longitude': 'Longitude'
    }
    df_feat['Fitur_ID'] = df_feat['Fitur'].map(lambda x: feature_translation.get(x, x))
    
    fig = px.bar(
        df_feat,
        x='Pentingnya',
        y='Fitur_ID',
        orientation='h',
        color='Pentingnya',
        color_continuous_scale='Blues',
        labels={'Pentingnya': 'Tingkat Kepentingan', 'Fitur_ID': 'Fitur'}
    )
    
    layout_params = _get_plotly_layout_params("Ranking Fitur Paling Berpengaruh (Feature Importance)")
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    fig.update_traces(
        hovertemplate="Fitur: %{y}<br>Nilai Kepentingan: %{x:.4f}"
    )
    return fig

def plot_model_comparison_time_series(df_test_1000):
    """
    Plots a line chart comparing the monthly average price of actual values
    against all trained models' predictions.
    """
    model_cols = ['linear_regression', 'ridge_regression', 'decision_tree', 'random_forest', 'gradient_boosting']
    all_cols = ['Actual'] + model_cols
    
    # Calculate monthly averages
    df_grouped = df_test_1000.groupby('Month')[all_cols].mean().reset_index()
    
    # Map month values to month names
    month_names = {8: 'Agustus', 9: 'September', 10: 'Oktober'}
    df_grouped['Nama_Bulan'] = df_grouped['Month'].map(month_names)
    
    # Sort chronologically by month value
    df_grouped = df_grouped.sort_values('Month')
    
    fig = go.Figure()
    
    # Define colors and styles for each line
    line_configs = {
        'Actual': dict(name='Harga Aktual', color='#EF4444', width=3, dash='solid'),
        'linear_regression': dict(name='Linear Regression', color='#94A3B8', width=1.5, dash='dash'),
        'ridge_regression': dict(name='Ridge Regression', color='#CBD5E1', width=1.5, dash='dot'),
        'decision_tree': dict(name='Decision Tree', color='#F59E0B', width=1.5, dash='dashdot'),
        'random_forest': dict(name='Random Forest', color='#2563EB', width=2.5, dash='solid'),
        'gradient_boosting': dict(name='Gradient Boosting', color='#10B981', width=2, dash='solid')
    }
    
    for col in all_cols:
        cfg = line_configs[col]
        # Convert to Billions of IDR
        y_values = df_grouped[col] / 1_000_000_000
        
        fig.add_trace(go.Scatter(
            x=df_grouped['Nama_Bulan'],
            y=y_values,
            mode='lines+markers',
            name=cfg['name'],
            line=dict(color=cfg['color'], width=cfg['width'], dash=cfg['dash']),
            marker=dict(size=8),
            hovertemplate=f"{cfg['name']}: Rp %{{y:.3f}} Miliar<br>Bulan: %{{x}}"
        ))
        
    layout_params = _get_plotly_layout_params("Tren Rata-rata Harga Bulanan (Forecast vs Actual)")
    fig.update_layout(
        **layout_params,
        xaxis_title="Bulan Penaksiran",
        yaxis_title="Rata-rata Harga (Miliar Rp)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def plot_model_comparison_sequence(df_test_1000, start_idx, end_idx):
    """
    Plots a line chart comparing the predicted price sequence vs actual price sequence
    for a slice of individual properties ordered chronologically.
    """
    model_cols = ['linear_regression', 'ridge_regression', 'decision_tree', 'random_forest', 'gradient_boosting']
    all_cols = ['Actual'] + model_cols
    
    # Sort chronologically by the original index
    df_sorted = df_test_1000.sort_index()
    
    # Extract the requested slice
    df_slice = df_sorted.iloc[start_idx:end_idx].reset_index()
    
    fig = go.Figure()
    
    # Define colors and styles for each line
    line_configs = {
        'Actual': dict(name='Harga Aktual', color='#EF4444', width=3, dash='solid'),
        'linear_regression': dict(name='Linear Regression', color='#94A3B8', width=1.5, dash='dash'),
        'ridge_regression': dict(name='Ridge Regression', color='#CBD5E1', width=1.5, dash='dot'),
        'decision_tree': dict(name='Decision Tree', color='#F59E0B', width=1.5, dash='dashdot'),
        'random_forest': dict(name='Random Forest', color='#2563EB', width=2.5, dash='solid'),
        'gradient_boosting': dict(name='Gradient Boosting', color='#10B981', width=2, dash='solid')
    }
    
    x_indices = [f"Sampel {i+1}" for i in range(start_idx, start_idx + len(df_slice))]
    
    for col in all_cols:
        cfg = line_configs[col]
        # Convert to Billions of IDR
        y_values = df_slice[col] / 1_000_000_000
        
        fig.add_trace(go.Scatter(
            x=x_indices,
            y=y_values,
            mode='lines',
            name=cfg['name'],
            line=dict(color=cfg['color'], width=cfg['width'], dash=cfg['dash']),
            hovertemplate=f"{cfg['name']}: Rp %{{y:.3f}} Miliar"
        ))
        
    layout_params = _get_plotly_layout_params(f"Perbandingan Sekuensial Kronologis (Sampel {start_idx+1} - {start_idx+len(df_slice)})")
    fig.update_layout(
        **layout_params,
        xaxis_title="Urutan Kronologis Properti",
        yaxis_title="Harga Rumah (Miliar Rp)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def plot_metrics_comparison_bar(metrics_df, metric_name):
    """
    Plots a bar chart comparing performance metrics across models.
    metrics_df should have columns: ['Model', 'R2 Score', 'MAE (Miliar Rp)', 'RMSE (Miliar Rp)']
    """
    # Map metric_name to the dataframe column
    metric_map = {
        'R2 Score': 'R2 Score',
        'MAE': 'MAE (Miliar Rp)',
        'RMSE': 'RMSE (Miliar Rp)'
    }
    col_to_plot = metric_map.get(metric_name, 'R2 Score')
    
    # Sort for visual hierarchy
    # R2: Higher is better, so ascending=True for plotly bar ordering
    # MAE/RMSE: Lower is better, so descending=True
    ascending_sort = (metric_name == 'R2 Score')
    df_sorted = metrics_df.sort_values(by=col_to_plot, ascending=ascending_sort)
    
    # Pick color scale based on metric
    color_scale = 'Blues' if metric_name == 'R2 Score' else 'Oranges'
    y_title = "Nilai R² Score" if metric_name == 'R2 Score' else f"Error ({metric_name} - Miliar Rp)"
    
    fig = px.bar(
        df_sorted,
        x='Model',
        y=col_to_plot,
        color=col_to_plot,
        color_continuous_scale=color_scale,
        labels={'Model': 'Model Algoritma', col_to_plot: y_title}
    )
    
    title_text = f"Perbandingan Performa Model berdasarkan {metric_name}"
    layout_params = _get_plotly_layout_params(title_text)
    layout_params['coloraxis_showscale'] = False
    fig.update_layout(**layout_params)
    
    if metric_name == 'R2 Score':
        fig.update_traces(hovertemplate="Model: %{x}<br>R² Score: %{y:.4f}")
    else:
        fig.update_traces(hovertemplate="Model: %{x}<br>Error: Rp %{y:.3f} Miliar")
        
    return fig

