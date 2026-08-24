# Week 8: Supply Chain Optimization — Kenyan Fuel Demand

### 1. Environment Setup
```bash
pip install pandas numpy matplotlib scikit-learn scipy pulp
# Forecasting
python forecasting_model.py

# Inventory optimization
python inventory_optimization.py

# Distribution LP
python distribution_lp.py
| Metric                | Value          |
| --------------------- | -------------- |
| Forecast MAPE         | 1.80%          |
| Forecast RMSE         | 2,709 liters   |
| Safety Stock          | 11,351 liters  |
| Reorder Point         | 869,718 liters |
| EOQ                   | 495,225 liters |
| LP Optimal Daily Cost | ~KES 2.1M      |
Assumptions
Lead Time: 7 days (Mombasa to inland depots)
Service Level: 95% (Z = 1.645)
Holding Cost: KES 0.05/liter/day
Stockout Cost: KES 15.00/liter
Ordering Cost: KES 50,000/order
