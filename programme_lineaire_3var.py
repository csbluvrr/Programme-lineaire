import numpy as np
from scipy.optimize import linprog

print("=== Optimisation de la production de l'usine laitière ===\n")

# Saisie des marges unitaires
print("Entrez les marges unitaires :")
x1 = float(input("Marge par unite de lait (x₁) : "))
x2 = float(input("Marge par unite de fromage (x₂) : "))
x3 = float(input("Marge par unite de yaourt (x₃) : "))

objective = [-x1, -x2, -x3]  # On négative car linprog minimise

# ======================
# DÉFINIR LES CONTRAINTES
# ======================

# 1. Contrainte de pasteurisation
print("\nEntrez les temps de pasteurisation (en heures) :")
p1 = float(input("Temps pour un litre de lait : "))
p2 = float(input("Temps pour un kg de fromage : "))
p3 = float(input("Temps pour un kg de yaourt : "))

# 2. Contrainte de transformation
print("\nEntrez les temps de transformation (en heures) :")
t1 = float(input("Temps pour un litre de lait : "))
t2 = float(input("Temps pour un kg de fromage : "))
t3 = float(input("Temps pour un kg de yaourt : "))

# 3. Contrainte de stockage
print("\nEntrez les volumes de stockage (en m³) :")
s1 = float(input("Volume pour un litre de lait : "))
s2 = float(input("Volume pour un kg de fromage : "))
s3 = float(input("Volume pour un kg de yaourt : "))

# Matrice des contraintes
constraints_left = [
    [p1, p2, p3],        # Pasteurisation
    [t1, t2, t3],        # Transformation
    [s1, s2, s3]         # Stockage
]

# Limites maximales fixes
constraints_right = [4000, 3500, 100]

# Contraintes de positivité : x₁, x₂, x₃ ≥ 0
bounds = [(0, None), (0, None), (0, None)]

# ======================
# RÉSOUDRE LE PROBLÈME
# ======================

result = linprog(
    c=objective,
    A_ub=constraints_left,
    b_ub=constraints_right,
    bounds=bounds,
    method='highs'
)

# ======================
# AFFICHER LES RÉSULTATS
# ======================

if result.success:
    lait_optimal, fromage_optimal, yaourt_optimal = result.x
    
    # Arrondir les résultats aux nombres entiers (appartiennent à N)
    lait_optimal = round(lait_optimal)
    fromage_optimal = round(fromage_optimal)
    yaourt_optimal = round(yaourt_optimal)
    
    # Recalculer le profit avec les valeurs arrondies
    profit = x1*lait_optimal + x2*fromage_optimal + x3*yaourt_optimal
    
    print("\n✅ Solution Optimale Trouvée:")
    print(f"x₁ (Lait) : {lait_optimal} litres")
    print(f"x₂ (Fromage) : {fromage_optimal} kg")
    print(f"x₃ (Yaourt) : {yaourt_optimal} kg")
    print(f"Bénéfice Maximum: {profit:.2f} €")
    
    print("\nVérification des contraintes:")
    # Pasteurisation
    pasteur = p1*lait_optimal + p2*fromage_optimal + p3*yaourt_optimal
    reste_pasteur = 4000 - pasteur
    print(f"1. Pasteurisation: Reste {reste_pasteur:.2f} heures sur 4000")
    
    # Transformation
    transfo = t1*lait_optimal + t2*fromage_optimal + t3*yaourt_optimal
    reste_transfo = 3500 - transfo
    print(f"2. Transformation: Reste {reste_transfo:.2f} heures sur 3500")
    
    # Stockage
    stock = s1*lait_optimal + s2*fromage_optimal + s3*yaourt_optimal
    reste_stock = 100 - stock
    print(f"3. Stockage: Reste {reste_stock:.3f} m³ sur 100")
else:
    print("❌ Aucune solution réalisable trouvée.") 