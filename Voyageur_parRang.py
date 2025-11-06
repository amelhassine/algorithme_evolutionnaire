import random

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

# Croisement simple point
def crossover_simple(parent1, parent2):
    taille = len(parent1)
    point = random.randint(1, taille - 2)
    enfant = [None] * taille
    enfant[:point] = parent1[:point]
    ptr = point
    for gene in parent2:
        if gene not in enfant:
            enfant[ptr] = gene
            ptr += 1
    return enfant

# Croisement double point
def crossover_double(parent1, parent2):
    taille = len(parent1)
    p1, p2 = sorted(random.sample(range(taille), 2))
    enfant = [None] * taille
    enfant[p1:p2] = parent1[p1:p2]
    ptr = 0
    for gene in parent2:
        if gene not in enfant:
            while enfant[ptr] is not None:
                ptr += 1
            enfant[ptr] = gene
    return enfant

# Croisement uniforme
def crossover_uniforme(parent1, parent2):
    taille = len(parent1)
    enfant = [None] * taille
    mask = [random.choice([True, False]) for _ in range(taille)]
    for i in range(taille):
        if mask[i]:
            enfant[i] = parent1[i]
    ptr = 0
    for gene in parent2:
        if gene not in enfant:
            while enfant[ptr] is not None:
                ptr += 1
            enfant[ptr] = gene
    return enfant

# Mutation version 1 : échange de deux villes
def mutation(solution, taux=0.05):
    sol = solution[:]
    if random.random() < taux:
        i, j = random.sample(range(len(sol)), 2)
        sol[i], sol[j] = sol[j], sol[i]
    return sol

# Sélection par roulette
def selection_roulette(population, fitnesses, n):
    selection = []
    total = sum(fitnesses)
    for _ in range(n):
        pick = random.uniform(0, total)
        courant = 0
        for ind, fit in zip(population, fitnesses):
            courant += fit
            if courant >= pick:
                selection.append(ind[:])
                break
    return selection

def algorithme_genetique_roulette(
        matrice_distances,
        taille_population=100,
        nb_generations=500,
        taux_crossover=0.8,
        taux_mutation=0.05,
        type_crossover='simple'  # 'simple', 'double' ou 'uniforme'
    ):
    nb_villes = len(matrice_distances)
    population = [random.sample(range(nb_villes), nb_villes) for _ in range(taille_population)]

    meilleure_solution = None
    meilleure_distance = float('inf')

    for _ in range(nb_generations):
        distances = [calculer_distance_totale(ind, matrice_distances) for ind in population]
        fitnesses = [1 / (d + 1e-10) for d in distances]

        for ind, dist in zip(population, distances):
            if dist < meilleure_distance:
                meilleure_solution = ind[:]
                meilleure_distance = dist

        parents = selection_roulette(population, fitnesses, taille_population)

        nouvelle_population = []
        for i in range(0, taille_population, 2):
            p1 = parents[i]
            p2 = parents[(i + 1) % taille_population]

            if random.random() < taux_crossover:
                if type_crossover == 'simple':
                    enfant1 = crossover_simple(p1, p2)
                    enfant2 = crossover_simple(p2, p1)
                elif type_crossover == 'double':
                    enfant1 = crossover_double(p1, p2)
                    enfant2 = crossover_double(p2, p1)
                elif type_crossover == 'uniforme':
                    enfant1 = crossover_uniforme(p1, p2)
                    enfant2 = crossover_uniforme(p2, p1)
                else:
                    raise ValueError("type_crossover doit être 'simple', 'double' ou 'uniforme'")
            else:
                enfant1, enfant2 = p1[:], p2[:]

            enfant1 = mutation(enfant1, taux_mutation)
            enfant2 = mutation(enfant2, taux_mutation)

            nouvelle_population.extend([enfant1, enfant2])

        population = nouvelle_population[:taille_population]

    return meilleure_solution, meilleure_distance

# Exemple de matrice de distances
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

if __name__ == "__main__":
    meilleure_solution, meilleure_distance = algorithme_genetique_roulette(
        matrice_distances,
        taille_population=100,
        nb_generations=500,
        taux_crossover=0.8,
        taux_mutation=0.05,
        type_crossover='simple'  # 'double' ou 'uniforme' aussi possible
    )
    print("Meilleure solution (roulette):", meilleure_solution)
    print("Distance minimale:", meilleure_distance)
