import random
import math

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisin(solution):
    """Crée une nouvelle solution en échangeant deux villes au hasard"""
    voisin = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule(matrice_distances, temperature_initiale, temperature_min, alpha, nombre_iterations):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    temperature = temperature_initiale

    for _ in range(nombre_iterations):
        voisin = generer_voisin(solution_actuelle)
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        distance_voisin = calculer_distance_totale(voisin, matrice_distances)
        delta = distance_voisin - distance_actuelle

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            solution_actuelle = voisin
            if distance_voisin < meilleure_distance:
                meilleure_solution = voisin[:]
                meilleure_distance = distance_voisin

        temperature = max(temperature * alpha, temperature_min)
        if temperature <= temperature_min:
            break

    return meilleure_solution, meilleure_distance

matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

temperature_initiale = 100
temperature_min = 0.01
alpha = 0.995
nombre_iterations = 10000

meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances,
    temperature_initiale,
    temperature_min,
    alpha,
    nombre_iterations
)

print("Meilleure solution trouvée (Recuit simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
