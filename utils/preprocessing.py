import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

def load_data(file_path="data/clean_df.csv"):
    """
    Loads dataset from CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    return pd.read_csv(file_path)

def clean_data(df):
    """
    Cleans dataset by dropping duplicate rows and unnecessary index columns.
    """
    df_cleaned = df.copy()
    
    # Drop first column if it's unnamed or empty (usually represents index)
    unnamed_cols = [col for col in df_cleaned.columns if col == '' or col.startswith('Unnamed')]
    if unnamed_cols:
        df_cleaned = df_cleaned.drop(columns=unnamed_cols)
        
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates().reset_index(drop=True)
    return df_cleaned