import numpy as np
from polygon_eclairage import polygon_eclairage
from aire_multi_polygones import aire_multi_polygones
import tkinter as tk

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


def preparation():
    # recuperation de la carte
    carte = np.loadtxt('P2/projetmatinfo/fichier.txt', dtype=np.uint8)

    # recuperation des sommets du polygone
    f = open("P2/projetmatinfo/fichier2.txt", 'r')
    liste_sommets = eval(f.read())
    f.close()

    # calcul de l'aire du polygone
    aire_totale = aire_polygon(liste_sommets)

    # creation de la fenetre
    wnd = tk.Tk()
    canvas = tk.Canvas(master=wnd, width=600, height=400)
    canvas.pack()
    # creation de la map
    canvas.create_polygon(liste_sommets, fill='grey')

    return carte, liste_sommets, aire_totale, canvas


def creer_pop(nombre_gardiens, pop_taille, carte):
    pop = []
    for i in range(pop_taille):
        individu = []
        for j in range(nombre_gardiens):
            cell = None
            while cell != 0:
                x = np.random.randint(0, 600)
                y = np.random.randint(0, 400)
                cell = carte[y][x]
            individu.append([x, y])
        pop.append(individu)
    return pop

def classer_pop(pop, nombre_gardiens, liste_sommets, canvas, generation):
    print(pop)
    if nombre_gardiens == 1:
        pop_sorted = []
        for indiv in pop:
            polygone_lumiere = polygon_eclairage(indiv[0], liste_sommets, canvas)
            aire = aire_polygon(polygone_lumiere)
            pop_sorted.append((aire, indiv[0]))
        pop_sorted.sort(reverse=True)
    else:
        if generation == 1:
            pop_sorted = []
            for indiv in pop:
                polygone_lumiere = list()
                for gardien in indiv:
                    polygone_lumiere.append(polygon_eclairage(gardien, liste_sommets, canvas))
                aire = aire_multi_polygones(polygone_lumiere)
                pop_sorted.append((aire, indiv))
            pop_sorted.sort(reverse=True)
        else:
            pop_sorted = []
            for indiv in pop[0]:
                polygone_lumiere = list()
                for gardien in indiv:
                    polygone_lumiere.append(polygon_eclairage(gardien, liste_sommets, canvas))
                aire = aire_multi_polygones(polygone_lumiere)
                pop_sorted.append((aire, indiv))
            pop_sorted.sort(reverse=True)
    print(pop_sorted)
    return pop_sorted

def moyenne_cross_over(pop_sorted, pop_taille, nombre_gardiens, carte):
    if nombre_gardiens == 1:
        pop = []
        # clonage du meilleur individu
        pop.append(pop_sorted[0][1])
        # crossover des meilleurs individus entre eux
        for i in range(pop_taille // 2 - 1):
            new_individu = [(pop_sorted[i][1][0] + pop_sorted[i+1][1][0]) // 2, (pop_sorted[i][1][1] + pop_sorted[i+1][1][1]) // 2]
            # verification que le nouvel individu est bien dans le polygone
            if carte[new_individu[0]][new_individu[1]] == 0: 
                pop.append(new_individu)
            else:
                pop.append(pop_sorted[i][1])
        return pop
    else:
        pop = []
        # clonage du meilleur individu
        pop.append(pop_sorted[0][1])
        # crossover des meilleurs individus entre eux
        for i in range(pop_taille // 2 - 1):
            new_individu = list()
            for j in range(nombre_gardiens):
                new_gardien = [(pop_sorted[i][1][j][0] + pop_sorted[i+1][1][j][0]) // 2, (pop_sorted[i][1][j][1] + pop_sorted[i+1][1][j][1]) // 2]
                
                # verification que le nouvel individu est bien dans le polygone
                if new_gardien[0] < 400 and new_gardien[1] < 600 and new_gardien[0] > 0 and new_gardien[1] > 0: 
                    if carte[new_gardien[0]][new_gardien[1]] == 0: 
                        new_individu.append(new_gardien)
                else:
                    new_individu.append(pop_sorted[i][1][j]) 
            pop.append(new_individu)
        return pop

def mutation(pop, mutation_proba, nombre_gardiens):
    if nombre_gardiens == 1:
        for indiv in pop:
            if np.random.uniform(0, 1) < mutation_proba:
                dirX = np.random.randint(0, 1)
                dirY = np.random.randint(0, 1)
                if dirX == 1 and dirY == 1:
                    indiv[0] += 1
                    indiv[1] += 1
                elif dirX == 1 and dirY == 0:
                    indiv[0] += 1
                    indiv[1] -= 1
                elif dirX == 0 and dirY == 1:
                    indiv[0] -= 1
                    indiv[1] += 1
                else:
                    indiv[0] -= 1
                    indiv[1] -= 1
        return pop
    else:
        for indiv in pop:
            for gardien in indiv:
                if np.random.uniform(0, 1) < mutation_proba:
                    dirX = np.random.randint(0, 1)
                    dirY = np.random.randint(0, 1)
                    if dirX == 1 and dirY == 1:
                        gardien[0] += 1
                        gardien[1] += 1
                    elif dirX == 1 and dirY == 0:
                        gardien[0] += 1
                        gardien[1] -= 1
                    elif dirX == 0 and dirY == 1:
                        gardien[0] -= 1
                        gardien[1] += 1
                    else:
                        gardien[0] -= 1
                        gardien[1] -= 1
        return pop

def completer_pop(pop, pop_taille, nombre_gardiens, carte):
    new_pop = []
    for indiv in pop:
        new_pop.append([indiv])
    nombre_manquant = pop_taille - len(pop)
    for i in range(nombre_manquant):
        individu = []
        for j in range(nombre_gardiens):
            cell = None
            while cell != 0:
                x = np.random.randint(0, 600)
                y = np.random.randint(0, 400)
                cell = carte[y][x]
            individu.append([x, y])
        new_pop.append(individu)
    return new_pop

def tester_pop(pop_sorted, seuil, nombre_gardiens, aire_totale):
    if nombre_gardiens == 1:
        aire_meilleur = pop_sorted[0][0]
        if aire_meilleur / aire_totale > seuil:
            return True
    else:
        pass

def entrainement(pop_taille, nombre_gardiens, mutation_proba, seuil, generation_max):
    carte, liste_sommets, aire_totale, canvas = preparation()
    pop = creer_pop(nombre_gardiens, pop_taille, carte)
    termine = False
    generation = 1
    for i in range(generation_max):
        print(f'generation n°{generation}')
        pop_sorted = classer_pop(pop, nombre_gardiens, liste_sommets, canvas, generation)
        termine = tester_pop(pop_sorted, seuil, nombre_gardiens, aire_totale)
        if termine is True:
            print(f"Une solution satisfaisante à {pop_sorted[0][0]}"
                  f"({seuil*100}%) a été obtenue à la {generation}ème "
                  f"generation: {pop_sorted[0][1]}")
            return pop_sorted[0][1]
        print(f'aire meilleur individu : {pop_sorted[0][0]} ({(pop_sorted[0][0]/aire_totale)*100}%)')
        pop_cross_over = moyenne_cross_over(pop_sorted, pop_taille, nombre_gardiens, carte)
        pop_mutation = mutation(pop_cross_over, mutation_proba, nombre_gardiens)
        pop = completer_pop(pop_mutation, pop_taille, nombre_gardiens, carte)
        generation += 1
    
    print(f"Une solution satisfaisante à {pop_sorted[0][0]}"
          f"({seuil*100}%) a été obtenue à la {generation}ème "
          f"generation: {pop_sorted[0][1]}")
    return pop_sorted[0][1]
        

if __name__ == '__main__':
    entrainement(10, 2, 0.1, 0.64, 40)


"""
############################
# Parametres
nombre_gardiens = 1
generation = 1
seuil = 0.5
generation_clef = [200, 300, 400, 500, 600, 700, 800]
mutation_proba = 0.1
pop_taille = 10
############################


wnd = tk.Tk()
canvas = tk.Canvas(master=wnd, width=600, height=400)
canvas.pack()

# creation de la map
canvas.create_polygon(liste_sommets, fill='grey')

liste_meilleurs = []

# creation d'une population de 10 individus ayant pour genome (x, y)
pop = [] 
for i in range(pop_taille):
    # choix d'une cellule au hasard incluse dans la polygone
    cell = None
    while cell != 0:
        x = np.random.randint(0, 600)
        y = np.random.randint(0, 400)
        cell = carte[y][x] 
    pop.append([x, y])

pop_sorted = []
for indiv in pop:
    polygone_lumiere = polygon_eclairage(indiv, liste_sommets, canvas, mode_demo=False)
    aire = aire_multi_polygones([polygone_lumiere])
    pop_sorted.append((aire, indiv))
pop_sorted.sort(reverse=True)

while pop_sorted[0][0]/aire_totale < seuil:
    print(f'generation n°{generation}')
    
    # classer la population (fonction d'evaluation)
    pop_sorted = []
    for indiv in pop:
        polygone_lumiere = polygon_eclairage(indiv, liste_sommets, canvas, mode_demo=False)
        aire = aire_multi_polygones([polygone_lumiere])
        pop_sorted.append((aire, indiv))
    pop_sorted.sort(reverse=True)

    print(f'aire meilleur individu : {pop_sorted[0][0]} ({(pop_sorted[0][0]/aire_totale)*100}%)')
    liste_meilleurs.append(pop_sorted[0][1])
    # crossover (methode de la moyenne utilisée)

    pop = []
    # clonage du meilleur individu
    pop.append(pop_sorted[0][1])
    # crossover des meilleurs individus entre eux
    for i in range(pop_taille//2 - 1):
        new_individu = [(pop_sorted[i][1][0] + pop_sorted[i+1][1][0]) // 2, (pop_sorted[i][1][1] + pop_sorted[i+1][1][1]) // 2]
        
        # verification que le nouvel individu est bien dans le polygone
        if new_individu[0] < 400 and new_individu[1] < 600 and new_individu[0] > 0 and new_individu[1] > 0: 
            if carte[new_individu[0]][new_individu[1]] == 0: 
                pop.append(new_individu)
        else:
            pop.append(pop_sorted[i][1]) 
    
    # mutation
    for indiv in pop:
        if np.random.uniform(0, 1) < mutation_proba:
            dirX = np.random.randint(0, 1)
            dirY = np.random.randint(0, 1)
            if dirX == 1 and dirY == 1:
                indiv[0] += 1
                indiv[1] += 1
            elif dirX == 1 and dirY == 0:
                indiv[0] += 1
                indiv[1] -= 1
            elif dirX == 0 and dirY == 1:
                indiv[0] -= 1
                indiv[1] += 1
            else:
                indiv[0] -= 1
                indiv[1] -= 1
            
    # finir la nouvelle population
    for i in range(pop_taille//2):
        # choix d'une cellule au hasard incluse dans la polygone
        cell = None
        while cell != 0:
            x = np.random.randint(0, 600)
            y = np.random.randint(0, 400)
            cell = carte[y][x] 
        pop.append([x, y])
    
    generation += 1
    # print(liste_meilleurs)
    if generation == 100:
        mutation_proba = 0.03
    if generation == 500:
        mutation_proba = 0
    if generation in generation_clef:
        seuil -= 5

print(f"Une solution satisfaisante à {pop_sorted[0][0]} ({seuil*100}%) a été obtenue à la {generation}ème generation: {pop_sorted[0][1]}")



for i in range(len(liste_meilleurs)):
    canvas.create_oval(liste_meilleurs[i][0]-4, liste_meilleurs[i][1]-4, liste_meilleurs[i][0]+4, liste_meilleurs[i][1]+4, fill='yellow')

# canvas.create_oval(liste_meilleurs[-1][0]-4, liste_meilleurs[-1][1]-4, liste_meilleurs[-1][0]+4, liste_meilleurs[-1][1]+4, fill='red')


canvas.create_oval(300-4, 232-4, 300+4, 232+4, fill='red')
canvas.create_oval(308-4, 237-4, 308+4, 237+4, fill='green')
canvas.create_oval(312-4, 234-4, 312+4, 234+4, fill='black')

polygone_lumiere = polygon_eclairage((312, 234), liste_sommets, canvas, mode_demo=False)
aire = aire_polygon(polygone_lumiere)
print(aire)

[296, 203]
"""