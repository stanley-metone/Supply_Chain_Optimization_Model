# Week 8: Fuel Supply Chain Optimization Report

## What This Project Is About

This project helps us plan how much fuel to buy, when to buy it, and how to move it across Kenya—so we never run out at the pump, but we also don't waste money storing fuel we don't need.

We used two and a half years of daily national fuel demand data (January 2024 to June 2026) to build a smart forecast, set safe inventory levels, and find the cheapest way to ship fuel from our refineries to regional depots.

---

## Why This Matters

Running out of fuel is expensive. When a depot goes dry, we must buy emergency fuel on the spot market at a huge markup. On the other hand, keeping too much fuel in storage costs money every day (tank rental, insurance, and tied-up cash).

This project finds the **sweet spot**: enough fuel on hand to cover surprises, but not so much that we bleed cash holding it.

---

## What We Did

### 1. Demand Forecasting
We built a model that predicts how much fuel Kenya will need each day for the next 60 days.

**What we learned:**
- Demand is growing steadily—about 17% higher in 2026 than in 2024.
- Weekdays are busier than weekends (trucks and buses move more during the work week).
- Demand jumps at the end of each month when salaries are paid.
- Public holidays create short, predictable dips.

**How accurate is it?**
When we tested the model against real June 2026 data, it was off by less than 2% on average. That is accurate enough to plan orders confidently.

---

### 2. Inventory Policy
We calculated three key numbers to manage stock at each depot:

| Policy Element | What It Means | Our Number |
|---|---|---|
| **Reorder Point** | "When fuel drops to this level, place a new order." | 869,718 liters |
| **Safety Stock** | "Extra fuel kept just in case demand spikes while we wait for delivery." | 11,351 liters |
| **Order Size (EOQ)** | "How much to order each time." | 495,225 liters |

**Why 11,351 liters of safety stock?**
It takes 7 days for a new fuel delivery to arrive. During those 7 days, demand can jump unexpectedly. The safety stock is a small buffer—about 9% of one day's usage—that protects us 95% of the time. We ran 1,000 simulated scenarios, and this buffer consistently reduced shortages and emergency costs.

**The bottom line:** Spending a little to hold this buffer saves us roughly KES 162,000 every 60 days in avoided emergency purchases.

---

### 3. Distribution Optimization
We have two refineries (Mombasa and Nairobi) and three main depots (Nakuru, Kisumu, and Eldoret). Shipping fuel costs different amounts depending on the route.

We used a mathematical optimizer to find the cheapest way to meet every depot's daily demand without exceeding what each refinery can produce.

**The result:** The optimal plan saves about **KES 180,000 per day** compared to our old "gut feel" routing.

**Best route insight:** Nairobi should supply Nakuru (short, cheap haul), while Mombasa covers Kisumu and Eldoret. This seems obvious, but the optimizer proved exactly how many liters to send on each route to minimize total cost.

---

## Key Results at a Glance

| Result | Value |
|---|---|
| Forecast error | Less than 2% (very accurate) |
| Safety stock | 11,351 liters |
| Reorder trigger | 869,718 liters |
| Typical order size | 495,225 liters |
| Daily distribution savings | ~KES 180,000 |
| Stockout protection | 95% confidence |

---

## Files in This Folder

- **week8_supply_chain_optimization.ipynb** — The main technical notebook (for analysts and engineers).
- **forecasting_model.py** — The forecasting engine (can be run automatically each morning to update predictions).
- **inventory_optimization.py** — The inventory calculator and simulator (shows how often we would run out with and without safety stock).
- **distribution_lp.py** — The shipping route optimizer (tells us the cheapest way to move fuel today).
- **synthetic_kenyan_fuel_demand.csv** — The historical data we started with.
- **forecast_60_days.csv** — The 60-day demand prediction (updated daily).
- **hackathon2_reflection.md** — Notes from our team on how we worked together during the hackathon.
- **Week8_Ops_Review_VideoScript.md** — The script used for the 15-minute management presentation.
- **Week8_Ops_Review_[YourName].mp4** — The recorded video presentation for senior leadership.
- **Week8_Ops_Slides.pdf** — The slide deck used in the video.

---

## How to Use This Work

1. **Each morning:** Run `forecasting_model.py` to get today's updated 60-day demand outlook.
2. **Each afternoon:** Check current depot tank levels. If any depot is at or below 869,718 liters, trigger an order for 495,225 liters.
3. **Each evening:** Run `distribution_lp.py` to confirm tomorrow's cheapest shipping plan from refineries to depots.

---

## Assumptions We Made

To keep the math realistic, we had to make some educated guesses. If these change, the numbers should be updated:

- **Delivery time:** 7 days from order to arrival at depot.
- **Target reliability:** We want to avoid stockouts 95% of the time (industry standard for critical fuel supply).
- **Holding cost:** KES 0.05 per liter per day to keep fuel in storage.
- **Emergency cost:** KES 15 per liter if we have to buy on the spot market during a shortage.
- **Order cost:** KES 50,000 in admin and logistics fees every time we place a replenishment order.

---

## What Happens Next

Three strategic actions are recommended:

1. **Install smart tank sensors** so we know exact fuel levels in real time and can trigger reorders automatically. Estimated payback: 5 months.
2. **Expand the Nairobi–Nakuru short-haul route** so we can move more cheap fuel on our cheapest lane.
3. **Renegotiate the Mombasa minimum supply contract** from 40% down to 30%, freeing volume to use the cheaper Nairobi refinery where possible.

Combined, these actions are projected to save **KES 5.4 million in Q3 alone**.

---

## Questions?

Contact: [Your Name] — [your.email@company.co.ke]
Date: August 2026



