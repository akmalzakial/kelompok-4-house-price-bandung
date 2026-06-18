import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from utils.preprocessing import clean_data, preprocess_data

def train_model(df, model_path="models/random_forest_model.pkl"):
    """
    Trains a Random Forest Regressor model on the provided DataFrame,
    evaluates it, and saves the model bundle.
    """
    # 1. Clean the dataset
    df_clean = clean_data(df)
    
    # 2. Encode categorical columns
    feature_cols = [
        'Location', 'Bedroom', 'Bathroom', 'Carport', 
        'Land', 'Building', 'Month', 'City/Regency', 
        'Latitude', 'Longitude'
    ]
    target_col = 'Price'
    
    # Preprocess features and fit encoders
    df_encoded, encoders = preprocess_data(df_clean, categorical_cols=['Location', 'City/Regency'])
    
    X = df_encoded[feature_cols]
    y = df_encoded[target_col]
    
    # 3. Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train model
    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1 # speed up training
    )
    rf.fit(X_train, y_train)
    
    # 5. Evaluate model
    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Feature importances
    importances = rf.feature_importances_
    feat_importances = dict(zip(feature_cols, importances))
    
    # 6. Save bundle
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    model_bundle = {
        'model': rf,
        'encoders': encoders,
        'features': feature_cols,
        'metrics': {
            'r2': float(r2),
            'mae': float(mae),
            'rmse': float(rmse)
        },
        'feature_importances': feat_importances,
        # Save a sample of test data (e.g. 500 records) to keep file size reasonable
        # and prevent slow plotting in streamlit, while maintaining accuracy for visualizations
        'test_sample': {
            'y_test': y_test.values,
            'y_pred': y_pred
        }
    }
    
    joblib.dump(model_bundle, model_path)
    return model_bundle

def train_model_comparison(df, comparison_path="models/model_comparison.pkl"):
    """
    Trains five models (Linear Regression, Ridge Regression, Decision Tree,
    Random Forest, and Gradient Boosting Regressor) on the provided DataFrame,
    evaluates them, and saves a comparison bundle.
    """
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    
    # 1. Clean the dataset
    df_clean = clean_data(df)
    
    # 2. Encode categorical columns
    feature_cols = [
        'Location', 'Bedroom', 'Bathroom', 'Carport', 
        'Land', 'Building', 'Month', 'City/Regency', 
        'Latitude', 'Longitude'
    ]
    target_col = 'Price'
    
    df_encoded, encoders = preprocess_data(df_clean, categorical_cols=['Location', 'City/Regency'])
    
    X = df_encoded[feature_cols]
    y = df_encoded[target_col]
    
    # 3. Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize models
    models_dict = {
        'linear_regression': ('Linear Regression', LinearRegression()),
        'ridge_regression': ('Ridge Regression', Ridge(alpha=1.0)),
        'decision_tree': ('Decision Tree Regressor', DecisionTreeRegressor(max_depth=15, random_state=42)),
        'random_forest': ('Random Forest Regressor', RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)),
        'gradient_boosting': ('Gradient Boosting Regressor', GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42))
    }
    
    comparison_bundle = {}
    
    # 5. Train and evaluate each model
    for key, (name, model) in models_dict.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Extract feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
        else:
            importances = np.zeros(len(feature_cols))
            
        feat_importances = dict(zip(feature_cols, importances))
        
        comparison_bundle[key] = {
            'model_name': name,
            'metrics': {
                'r2': float(r2),
                'mae': float(mae),
                'rmse': float(rmse)
            },
            'feature_importances': feat_importances,
            'test_sample': {
                'y_test': y_test.iloc[:1000].values,
                'y_pred': y_pred[:1000]
            }
        }
        
    # 6. Save comparison bundle
    os.makedirs(os.path.dirname(comparison_path), exist_ok=True)
    joblib.dump(comparison_bundle, comparison_path)
    return comparison_bundle

