"""
forecasting_model.py
--------------------
Standalone Prophet-style forecasting script for Kenyan fuel demand.
Can be run from CLI: python forecasting_model.py
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def load_and_engineer(path: str):
    df = pd.read_csv(path)
    df['ds'] = pd.to_datetime(df['ds'])
    df.columns = ['ds', 'y']
    df['t'] = (df['ds'] - df['ds'].min()).dt.days
    df['trend'] = df['t']
    df['trend_sq'] = df['t'] ** 2

    # Fourier yearly (10 harmonics)
    for i in range(1, 11):
        df[f'yearly_sin_{i}'] = np.sin(2 * np.pi * i * df['t'] / 365.25)
        df[f'yearly_cos_{i}'] = np.cos(2 * np.pi * i * df['t'] / 365.25)

    # Fourier weekly (3 harmonics)
    for i in range(1, 4):
        df[f'weekly_sin_{i}'] = np.sin(2 * np.pi * i * df['t'] / 7)
        df[f'weekly_cos_{i}'] = np.cos(2 * np.pi * i * df['t'] / 7)

    # External regressors
    holidays = pd.to_datetime([
        '2024-01-01','2024-04-01','2024-05-01','2024-06-01','2024-10-10','2024-10-20','2024-12-12','2024-12-25','2024-12-26',
        '2025-01-01','2025-04-18','2025-04-21','2025-05-01','2025-06-01','2025-10-10','2025-10-20','2025-12-12','2025-12-25','2025-12-26',
        '2026-01-01','2026-04-03','2026-04-06','2026-05-01','2026-06-01','2026-10-10','2026-10-20','2026-12-12','2026-12-25','2026-12-26',
        '2027-01-01','2027-03-26','2027-03-29','2027-05-01','2027-06-01','2027-10-10','2027-10-20','2027-12-12','2027-12-25','2027-12-26'
    ])
    df['is_holiday'] = df['ds'].isin(holidays).astype(int)
    df['holiday_window'] = 0
    for hd in holidays:
        mask = (df['ds'] >= hd - timedelta(days=1)) & (df['ds'] <= hd + timedelta(days=1))
        df.loc[mask, 'holiday_window'] = 1

    df['weekend'] = df['ds'].dt.dayofweek.isin([5, 6]).astype(int)
    df['days_to_month_end'] = (df['ds'] + pd.offsets.MonthEnd(0) - df['ds']).dt.days
    df['month_end_surge'] = (df['days_to_month_end'] <= 3).astype(int)
    df['quarter_start'] = ((df['ds'].dt.month.isin([1,4,7,10])) & (df['ds'].dt.day <= 7)).astype(int)

    return df

def train_model(df):
    feature_cols = [c for c in df.columns if c not in ['ds', 'y', 'days_to_month_end', 'day_of_quarter']]
    train_df = df[df['ds'] <= '2026-05-31'].copy()
    test_df = df[df['ds'] > '2026-05-31'].copy()

    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_df[feature_cols].values)
    y_train = train_df['y'].values
    X_test = scaler.transform(test_df[feature_cols].values)
    y_test = test_df['y'].values

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"MAPE: {mape:.2f}% | RMSE: {rmse:,.0f}L")
    return model, scaler, feature_cols, rmse

def forecast_next_60(model, scaler, feature_cols, df):
    last_date = df['ds'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=60, freq='D')
    future = pd.DataFrame({'ds': future_dates})
    future['t'] = (future['ds'] - df['ds'].min()).dt.days
    future['trend'] = future['t']
    future['trend_sq'] = future['t'] ** 2

    for i in range(1, 11):
        future[f'yearly_sin_{i}'] = np.sin(2 * np.pi * i * future['t'] / 365.25)
        future[f'yearly_cos_{i}'] = np.cos(2 * np.pi * i * future['t'] / 365.25)
    for i in range(1, 4):
        future[f'weekly_sin_{i}'] = np.sin(2 * np.pi * i * future['t'] / 7)
        future[f'weekly_cos_{i}'] = np.cos(2 * np.pi * i * future['t'] / 7)

    holidays = pd.to_datetime([
        '2024-01-01','2024-04-01','2024-05-01','2024-06-01','2024-10-10','2024-10-20','2024-12-12','2024-12-25','2024-12-26',
        '2025-01-01','2025-04-18','2025-04-21','2025-05-01','2025-06-01','2025-10-10','2025-10-20','2025-12-12','2025-12-25','2025-12-26',
        '2026-01-01','2026-04-03','2026-04-06','2026-05-01','2026-06-01','2026-10-10','2026-10-20','2026-12-12','2026-12-25','2026-12-26',
        '2027-01-01','2027-03-26','2027-03-29','2027-05-01','2027-06-01','2027-10-10','2027-10-20','2027-12-12','2027-12-25','2027-12-26'
    ])
    future['is_holiday'] = future['ds'].isin(holidays).astype(int)
    future['holiday_window'] = 0
    for hd in holidays:
        mask = (future['ds'] >= hd - timedelta(days=1)) & (future['ds'] <= hd + timedelta(days=1))
        future.loc[mask, 'holiday_window'] = 1
    future['weekend'] = future['ds'].dt.dayofweek.isin([5, 6]).astype(int)
    future['days_to_month_end'] = (future['ds'] + pd.offsets.MonthEnd(0) - future['ds']).dt.days
    future['month_end_surge'] = (future['days_to_month_end'] <= 3).astype(int)
    future['quarter_start'] = ((future['ds'].dt.month.isin([1,4,7,10])) & (future['ds'].dt.day <= 7)).astype(int)

    X_f = scaler.transform(future[feature_cols].values)
    future['yhat'] = model.predict(X_f)
    return future

if __name__ == "__main__":
    df = load_and_engineer("synthetic_kenyan_fuel_demand.csv")
    model, scaler, feature_cols, rmse = train_model(df)
    forecast = forecast_next_60(model, scaler, feature_cols, df)
    forecast[['ds','yhat']].to_csv("forecast_60_days.csv", index=False)
    print("Saved forecast_60_days.csv")
