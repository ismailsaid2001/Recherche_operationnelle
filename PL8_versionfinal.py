#PL  8 : shortest Path
import networkx as nx
import json
from networkx.readwrite import json_graph


def read_graph_from_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return json_graph.adjacency_graph(data)


# Read 'my_network.json' from file
filename = 'my_network.json'
D = read_graph_from_json(filename)
print(D.nodes, D.edges)
# Print the in-neighbors and out-neighbors of each node
for i in D.nodes:
    print("Node", i, "has in-neighbors", list(D.predecessors(i)), "and out-neighbors", list(D.successors(i)))
# Let's find a shortest path from 1 to 8 using a MIP
# First, import gurobi
import gurobipy as gp
from gurobipy import GRB

# Gu, Rothberg, Bixby -> Gurobi -> GRB
# Create model object
m = gp.Model()

# Variable x[i,j] equals 1 if edge (i,j) is part of the path
x = m.addVars(D.edges, vtype=GRB.BINARY)

# Specify the origin s and destination t
s = 1
t = 8

# Objective: minimize path length
m.setObjective(gp.quicksum(D.edges[e]['weight'] * x[e] for e in D.edges), GRB.MINIMIZE)
# m.setObjective( gp.quicksum( D.edges[i,j]['weight'] * x[i,j] for i,j in D.ed
# Constraint: leave s once.
# incoming edges - outgoing edges = -1
m.addConstr(gp.quicksum(x[j, s] for j in D.predecessors(s)) - gp.quicksum(x[s, j] for j in D.successors(s)) == -1)

# Constraints: flow balance at non-{s,t} nodes
# incoming edges - outgoing edges = 0
m.addConstrs(
    gp.quicksum(x[j, i] for j in D.predecessors(i)) - gp.quicksum(x[i, j] for j in D.successors(i)) == 0 for i in
    D.nodes if i not in {s, t})

m.update()
# Solve
m.optimize()
# print optimal solution
for e in D.edges:
    print("x[", e, "] =", x[e].x)

# which edges are part of the shortest path?
chosen_edges = [e for e in D.edges if x[e].x > 0.5]
print("The chosen edges (not necessarily in order) are", chosen_edges)

# solve the LP relaxation
r = m.relax()
r.optimize()
