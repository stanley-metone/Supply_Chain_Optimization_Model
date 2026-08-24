"""
distribution_lp.py
------------------
Solves the fuel distribution LP using PuLP.
"""

import pulp

def solve_distribution():
    refineries = ['Mombasa_Refinery', 'Nairobi_Refinery']
    supply = {'Mombasa_Refinery': 800000, 'Nairobi_Refinery': 500000}
    depots = ['Nakuru_Depot', 'Kisumu_Depot', 'Eldoret_Depot']
    demand = {'Nakuru_Depot': 350000, 'Kisumu_Depot': 280000, 'Eldoret_Depot': 220000}

    costs = {
        ('Mombasa_Refinery', 'Nakuru_Depot'): 2.50,
        ('Mombasa_Refinery', 'Kisumu_Depot'): 4.20,
        ('Mombasa_Refinery', 'Eldoret_Depot'): 5.00,
        ('Nairobi_Refinery', 'Nakuru_Depot'): 1.80,
        ('Nairobi_Refinery', 'Kisumu_Depot'): 3.50,
        ('Nairobi_Refinery', 'Eldoret_Depot'): 4.10,
    }

    prob = pulp.LpProblem("Fuel_Distribution", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("ship", (refineries, depots), lowBound=0, cat='Continuous')

    prob += pulp.lpSum([costs[(i,j)] * x[i][j] for i in refineries for j in depots])

    for i in refineries:
        prob += pulp.lpSum([x[i][j] for j in depots]) <= supply[i]
    for j in depots:
        prob += pulp.lpSum([x[i][j] for i in refineries]) >= demand[j]
    prob += pulp.lpSum([x['Mombasa_Refinery'][j] for j in depots]) >= 0.4 * supply['Mombasa_Refinery']

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    print(f"Status: {pulp.LpStatus[prob.status]}")
    print(f"Optimal Cost: KES {pulp.value(prob.objective):,.2f}")

    for i in refineries:
        for j in depots:
            v = pulp.value(x[i][j])
            if v and v > 0:
                print(f"  {i} -> {j}: {v:,.0f} L")

if __name__ == "__main__":
    solve_distribution()
