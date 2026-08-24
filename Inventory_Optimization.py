"""
inventory_optimization.py
-------------------------
Calculates Safety Stock, ROP, EOQ and simulates inventory policy performance.
"""

import pandas as pd
import numpy as np
from scipy import stats

# Assumptions
LEAD_TIME_DAYS = 7
SERVICE_LEVEL = 0.95
Z_SCORE = stats.norm.ppf(SERVICE_LEVEL)
DAILY_HOLDING_COST = 0.05
STOCKOUT_COST = 15.0
ORDERING_COST = 50000

def calculate_policy(forecast_mean, forecast_std):
    lead_time_mean = forecast_mean * LEAD_TIME_DAYS
    lead_time_std = forecast_std * np.sqrt(LEAD_TIME_DAYS)
    safety_stock = Z_SCORE * lead_time_std
    reorder_point = lead_time_mean + safety_stock
    annual_demand = forecast_mean * 365
    eoq = np.sqrt((2 * annual_demand * ORDERING_COST) / (DAILY_HOLDING_COST * 365))

    print("=== INVENTORY POLICY ===")
    print(f"Safety Stock: {safety_stock:,.0f} L")
    print(f"Reorder Point: {reorder_point:,.0f} L")
    print(f"EOQ: {eoq:,.0f} L")
    print(f"Max Inventory: {reorder_point + eoq:,.0f} L")
    return safety_stock, reorder_point, eoq

def simulate_policy(sim_demands, initial_inv, rop, eoq, lt, n_sims=1000):
    stockouts = np.zeros(n_sims)
    stockout_qty = np.zeros(n_sims)
    for sim in range(n_sims):
        inv = initial_inv
        transit = []
        for day in range(sim_demands.shape[1]):
            arriving = [q for d,q in transit if d==day]
            for q in arriving: inv += q
            transit = [(d,q) for d,q in transit if d>day]
            demand = sim_demands[sim, day]
            if inv >= demand:
                inv -= demand
            else:
                stockouts[sim] += 1
                stockout_qty[sim] += (demand - inv)
                inv = 0
            has_pending = any(d>day and d<=day+lt for d,q in transit)
            if inv <= rop and not has_pending:
                transit.append((day+lt, eoq))
    return stockouts, stockout_qty

if __name__ == "__main__":
    # Load forecast
    fc = pd.read_csv("forecast_60_days.csv")
    forecast_mean = fc['yhat'].mean()
    forecast_std = 2608  # from model residual analysis

    ss, rop, eoq = calculate_policy(forecast_mean, forecast_std)

    # Monte Carlo simulation
    np.random.seed(42)
    stress_std = forecast_std * 1.5
    sim_demands = []
    for _ in range(1000):
        noise = np.random.normal(0, stress_std, 60)
        sim_demands.append(np.maximum(fc['yhat'].values + noise, forecast_mean * 0.6))
    sim_demands = np.array(sim_demands)

    s_no, q_no = simulate_policy(sim_demands, rop - ss, rop - ss, eoq, LEAD_TIME_DAYS)
    s_yes, q_yes = simulate_policy(sim_demands, rop, rop, eoq, LEAD_TIME_DAYS)

    print("\n=== SIMULATION RESULTS ===")
    print(f"No SS  — Stockouts: {s_no.mean():.2f} days, Avg qty: {q_no.mean():,.0f} L")
    print(f"With SS — Stockouts: {s_yes.mean():.2f} days, Avg qty: {q_yes.mean():,.0f} L")
    print(f"Savings: KES {(q_no.mean() - q_yes.mean()) * STOCKOUT_COST:,.0f}")
