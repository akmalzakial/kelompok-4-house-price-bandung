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

def preprocess_data(df, categorical_cols=None, encoders=None):
    """
    Preprocesses dataset. If encoders are provided, uses them to transform features.
    If not, fits new LabelEncoder instances.
    
    Returns:
        df_encoded (pd.DataFrame): Dataframe with encoded categorical columns.
        encoders (dict): Dict of fitted LabelEncoder instances.
    """
    if categorical_cols is None:
        categorical_cols = ['Location', 'City/Regency']
        
    df_encoded = df.copy()
    fitted_encoders = {}
    
    for col in categorical_cols:
        if col not in df_encoded.columns:
            continue
            
        if encoders and col in encoders:
            # Predict mode: Use existing encoder
            le = encoders[col]
            # Convert to string to avoid comparison errors with numbers/nulls
            val_series = df_encoded[col].astype(str)
            
            # Fast mapping check to handle unseen categories safely just in case
            classes = set(le.classes_)
            val_series_safe = val_series.apply(lambda x: x if x in classes else le.classes_[0])
            df_encoded[col] = le.transform(val_series_safe)
            fitted_encoders[col] = le
        else:
            # Train mode: Fit new encoder
            le = LabelEncoder()
            # Convert to string to avoid comparison errors
            df_encoded[col] = df_encoded[col].astype(str)
            df_encoded[col] = le.fit_transform(df_encoded[col])
            fitted_encoders[col] = le
            
    return df_encoded, fitted_encoders
