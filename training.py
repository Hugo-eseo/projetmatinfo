import numpy as np
from polygon_eclairage import polygon_eclairage

# fonction de calcul de l'aire
def aire_polygon(points_coords):
    sommeX_Y1 = 0
    sommeY_X1 = 0
    for i in range(len(points_coords)):
        if i+1 == len(points_coords):
            sommeX_Y1 += points_coords[i][0] * points_coords[0][1]
            sommeY_X1 += points_coords[i][1] * points_coords[0][0]
        else:
            sommeX_Y1 += points_coords[i][0] * points_coords[i+1][1]
            sommeY_X1 += points_coords[i][1] * points_coords[i+1][0]
    return int(abs(0.5*(sommeX_Y1-sommeY_X1)))


# recuperation de la carte
carte = np.loadtxt('P2/projetmatinfo/fichier.txt', dtype=np.uint8)

# recuperation des sommets du polygone
f = open("P2/projetmatinfo/fichier2.txt", 'r')
liste_sommets = eval(f.read())
f.close()

# calcul de l'aire du polygone
aire_totale = aire_polygon(liste_sommets)

############################
# Parametres
generation = 1
seuil = 0.8
generation_clef = [200, 300, 400, 500, 600, 700, 800]
mutation_proba = 0.05
pop_taille = 10
############################

canvas = 0

# creation d'une population de 10 individus ayant pour genome (x, y)
pop = [] 
for i in range(pop_taille):
    # choix d'une cellule au hasard incluse dans la polygone
    cell = None
    while cell != 0:
        x = np.random.randint(0, 600)
        y = np.random.randint(0, 400)
        cell = carte[y][x] 
    pop.append((x, y))

pop_sorted = []
for indiv in pop:
    pop_sorted.append(aire_polygon(polygon_eclairage(gen1, liste_sommets), indiv))  # polygon_eclairage en cours de reecriture
    pop_sorted.sort(reverse=True)

while pop_sorted[0][0]/aire_totale < seuil:
    
    # classer la population (fonction d'evaluation)
    pop_sorted = []
    for indiv in pop:
        pop_sorted.append(aire_polygon(polygon_eclairage(gen1, liste_sommets, canvas), indiv))  # polygon_eclairage en cours de reecriture
    pop_sorted.sort(reverse=True)
        
    # crossover (methode de la moyenne utilisée)
    pop = []
    # clonage du meilleur individu
    pop.append(pop_sorted[0][1])
    # crossover des meilleurs individus entre eux
    for i in range(pop_taille//2 - 1):
        new_individu = ((pop_sorted[i][1][0] + pop_sorted[i+1][1][0]) // 2, (pop_sorted[i][1][1] + pop_sorted[i+1][1][1]) // 2)
        pop.append(new_individu)

    # mutation
    for indiv in pop:
        if np.random.uniform(0, 1) < mutation_proba:
            dirX = np.random.randint(0, 1)
            dirY = np.random.randint(0, 1)
            if dirX == 1 and dirY == 1:
                indiv[0] += 5
                indiv[1] += 5
            elif dirX == 1 and dirY == 0:
                indiv[0] += 5
                indiv[1] -= 5
            elif dirX == 0 and dirY == 1:
                indiv[0] -= 5
                indiv[1] += 5
            else:
                indiv[0] -= 5
                indiv[1] -= 5

    # finir la nouvelle population
    for i in range(pop_taille//2):
        # choix d'une cellule au hasard incluse dans la polygone
        cell = None
        while cell != 0:
            x = np.random.randint(0, 600)
            y = np.random.randint(0, 400)
            cell = carte[y][x] 
        pop.append((x, y))
    
    generation += 1
    if generation == 100:
        mutation_proba = 0.03
    if generation == 500:
        mutation_proba = 0
    if generation in generation_clef:
        seuil -= 5

print(f"Une solution satisfaisante à {pop_sorted[0][0]} ({seuil}%) a été obtenue à la {generation}ème generation: {pop_sorted[0][1]}")
