import gurobipy as gb

model = gb.Model()

# Define decision variables
x = {}
for j in range(7):
    for i in range(28):
        x[i, j] = model.addVar(vtype=gb.GRB.BINARY)

# Define objective function
model.setObjective(gb.quicksum(x[i, j] for j in range(7) for i in range(28)), gb.GRB.MINIMIZE)

# Define constraints
for i in range(28):
    model.addConstr(gb.quicksum(x[i, j] for j in range(7)) == 1)

for j in range(7):
    available = gb.LinExpr([10, 8, 12, 14, 9, 11, 7][j])
    for i in range(4):
        model.addConstr(gb.quicksum(x[j+i+k*7, j] for k in range(5)) >= available)

    model.addConstr(gb.quicksum(x[j+i, j] for i in range(28)) <= 2)
    nb_travail_jours = j * 4
    nb_conge_jours = 2
    model.addConstr(gb.quicksum(x[j+i, e] for i in range(nb_travail_jours, nb_travail_jours+nb_conge_jours) for e in range(7)) == 0)

# Solve the model
model.optimize()

# Print the solution
for j in range(7):
    print(f"Day {j+1}:")
    for i in range(28):
        if x[i, j].x > 0.5:
            print(f"\tEmployee {i+1}")
