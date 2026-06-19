import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fungsi Scatter Plot Prediksi vs Aktual (Commit 1)
def plot_predicted_vs_actual(y_actual, y_pred):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(y_actual, y_pred, alpha=0.5, color='blue')
    
    max_val = max(max(y_actual), max(y_pred))
    min_val = min(min(y_actual), min(y_pred))
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
    
    ax.set_xlabel("Aktual")
    ax.set_ylabel("Prediksi")
    ax.set_title("Scatter Plot: Prediksi vs Aktual")
    plt.tight_layout()
    return fig