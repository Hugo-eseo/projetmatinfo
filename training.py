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
    carte = np.loadtxt('P2/projetmatinfo/carte.txt', dtype=np.uint8)

    # recuperation des sommets du polygone
    f = open("P2/projetmatinfo/sommets_polygone.txt", 'r')
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
    return carte, liste_sommets, aire_totale, canvas, wnd

def preparation_sans_wnd(wnd, cnv):
    # recuperation de la carte
    carte = np.loadtxt('P2/projetmatinfo/carte.txt', dtype=np.uint8)

    # recuperation des sommets du polygone
    f = open("P2/projetmatinfo/sommets_polygone.txt", 'r')
    liste_sommets = eval(f.read())
    f.close()

    # calcul de l'aire du polygone
    aire_totale = aire_polygon(liste_sommets)

    return carte, liste_sommets, aire_totale, wnd, cnv


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
    if nombre_gardiens == 1:
        pop_sorted = []
        for indiv in pop:
            polygone_lumiere = polygon_eclairage(indiv[0], liste_sommets, canvas)
            aire = aire_polygon(polygone_lumiere)
            pop_sorted.append((aire, indiv[0]))
        pop_sorted.sort(reverse=True)
    else:
        pop_sorted = []
        for indiv in pop:
            polygone_lumiere = list()
            for gardien in indiv:
                polygone_lumiere.append(polygon_eclairage(gardien, liste_sommets, canvas))
            aire = aire_multi_polygones(polygone_lumiere)
            pop_sorted.append((aire, indiv))
        pop_sorted.sort(reverse=True)
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
            if new_individu[0] < 600 and new_individu[1] < 400 and new_individu[0] > 0 and new_individu[1] > 0: 
                if carte[new_individu[1]][new_individu[0]] == 0: 
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
                if new_gardien[0] < 600 and new_gardien[1] < 400 and new_gardien[0] > 0 and new_gardien[1] > 0: 
                    if carte[new_gardien[1]][new_gardien[0]] == 0: 
                        new_individu.append(new_gardien)
                    else:
                        new_individu.append(pop_sorted[i][1][j])
                else:
                    new_individu.append(pop_sorted[i][1][j])
            pop.append(new_individu)
        return pop


def mutation(pop, mutation_proba, nombre_gardiens, carte):
    if nombre_gardiens == 1:
        for indiv in pop:
            if np.random.uniform(0, 1) < mutation_proba:
                dirX = np.random.randint(0, 1)
                dirY = np.random.randint(0, 1)
                if dirX == 1 and dirY == 1:
                    if carte[indiv[1]+1][indiv[0]+1] == 0:
                        indiv[0] += 1
                        indiv[1] += 1
                elif dirX == 1 and dirY == 0:
                    if carte[indiv[1]-1][indiv[0]+1] == 0:
                        indiv[0] += 1
                        indiv[1] -= 1
                elif dirX == 0 and dirY == 1:
                    if carte[indiv[1]+1][indiv[0]-1] == 0:
                        indiv[0] -= 1
                        indiv[1] += 1
                else:
                    if carte[indiv[1]-1][indiv[0]-1] == 0:
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
                        if carte[gardien[1]+1][gardien[0]+1] == 0:
                            gardien[0] += 1
                            gardien[1] += 1
                    elif dirX == 1 and dirY == 0:
                        if carte[gardien[1]-1][gardien[0]+1] == 0:
                            gardien[0] += 1
                            gardien[1] -= 1
                    elif dirX == 0 and dirY == 1:
                        if carte[gardien[1]+1][gardien[0]-1] == 0:
                            gardien[0] -= 1
                            gardien[1] += 1
                    else:
                        if carte[gardien[1]-1][gardien[0]-1] == 0:
                            gardien[0] -= 1
                            gardien[1] -= 1
        return pop


def completer_pop(pop, pop_taille, nombre_gardiens, carte):
    if nombre_gardiens == 1:
        new_pop = []
        for indiv in pop:
            new_pop.append([indiv])
        nombre_manquant = pop_taille - len(pop)
        for i in range(nombre_manquant):
            cell = None
            while cell != 0:
                x = np.random.randint(0, 600)
                y = np.random.randint(0, 400)
                cell = carte[y][x]
            new_pop.append([[x, y]])
        return new_pop
    else:
        new_pop = []
        for indiv in pop:
            new_pop.append(indiv)
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
    aire_meilleur = pop_sorted[0][0]
    if aire_meilleur / aire_totale > seuil:
        return True


def entrainement(pop_taille, nombre_gardiens, mutation_proba, seuil, generation_max, wnd, cnv):
    carte, liste_sommets, aire_totale, wnd, canvas  = preparation_sans_wnd(wnd, cnv)
    pop = creer_pop(nombre_gardiens, pop_taille, carte)
    termine = False
    generation = 1
    for i in range(generation_max):
        print(f'generation n°{generation}')
        pop_sorted = classer_pop(pop, nombre_gardiens, liste_sommets, canvas, generation)
        termine = tester_pop(pop_sorted, seuil, nombre_gardiens, aire_totale)
        if termine is True:
            print(f"Une solution satisfaisante à {pop_sorted[0][0]} "
                  f"({round((pop_sorted[0][0]/aire_totale)*100, 2)}%) a été obtenue à la {generation}ème "
                  f"generation: {pop_sorted[0][1]}")
            return pop_sorted[0][1], wnd, canvas, liste_sommets, pop_sorted[0][0]
        print(f'aire meilleur individu : {pop_sorted[0][0]} ({(pop_sorted[0][0]/aire_totale)*100}%)')
        pop_cross_over = moyenne_cross_over(pop_sorted, pop_taille, nombre_gardiens, carte)
        pop_mutation = mutation(pop_cross_over, mutation_proba, nombre_gardiens, carte)
        pop = completer_pop(pop_mutation, pop_taille, nombre_gardiens, carte)
        generation += 1
    
    print(f"Une solution satisfaisante à {pop_sorted[0][0]} "
          f"({round((pop_sorted[0][0]/aire_totale)*100, 2)}%) a été obtenue à la {generation}ème "
          f"generation: {pop_sorted[0][1]}")
    return pop_sorted[0][1], wnd, canvas, liste_sommets, pop_sorted[0][0]
        

if __name__ == '__main__':
    taille_point = 3
    indiv, wnd, canvas, liste_sommets, aire= entrainement(10, 1, 0.05, 0.8, 10)
    canvas.create_polygon(liste_sommets, fill='grey')
    if type(indiv[0]) is list:
        for gardien in indiv:
            canvas.create_polygon(polygon_eclairage(gardien, liste_sommets, canvas), fill='yellow')
        for gardien in indiv:
            canvas.create_oval(gardien[0]-taille_point, gardien[1]-taille_point, gardien[0]+taille_point, gardien[1]+taille_point, fill='red')
    else:
        canvas.create_polygon(polygon_eclairage(indiv, liste_sommets, canvas), fill='yellow')
        canvas.create_oval(indiv[0]-taille_point, indiv[1]-taille_point, indiv[0]+taille_point, indiv[1]+taille_point, fill='red')
    wnd.mainloop()
