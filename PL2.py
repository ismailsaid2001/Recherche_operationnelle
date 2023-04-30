import gurobipy as gp

# Création du modèle
model = gp.Model('Mixage optimal de pétrole')

# Données du problème
nb_barils_type1 = 5000
nb_barils_type2 = 10000
qualite_type1 = 10
qualite_type2 = 5
prix_gazoline = 25
prix_petrole_chauffage = 20
frais_marketing_gazoline = 0.2
frais_marketing_petrole_chauffage = 0.1

# Variables de décision
x1 = model.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, ub=nb_barils_type1, name='nb_barils_type1_mix')
x2 = model.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, ub=nb_barils_type2, name='nb_barils_type2_mix')

# Contraintes
model.addConstr(qualite_type1 * x1 + qualite_type2 * x2 >= 8 * (x1 + x2), name='qualite_min_gazoline')
model.addConstr(qualite_type1 * x1 + qualite_type2 * x2 >= 6 * (x1 + x2), name='qualite_min_petrole_chauffage')

# Fonction objectif
cout_total = prix_gazoline * x1 + prix_petrole_chauffage * x2 \
             - frais_marketing_gazoline * x1 - frais_marketing_petrole_chauffage * x2
model.setObjective(cout_total, sense=gp.GRB.MAXIMIZE)

# Résolution du modèle
model.optimize()

# Affichage des résultats
if model.status == gp.GRB.OPTIMAL:
    print('Mixage optimal: ')
    print('- Type 1: {} barils'.format(round(x1.x)))
    print('- Type 2: {} barils'.format(round(x2.x)))
    print('Profit total: {} D'.format(round(model.objVal)))
else:
    print('Le modèle n\'a pas trouvé de solution optimale')
