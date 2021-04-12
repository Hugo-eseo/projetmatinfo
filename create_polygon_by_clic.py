import tkinter as tk
from maths import barycentre, det, distance_two_points, point_in_segment
from math import isclose

def point_in_polygon(point, segments_list):
    # side est un point sur le bord du canvas au meme x (ou y) que le gardien
    side_x = (0, point[1])
    side_y = (point[0], 0)
    cpt_x, cpt_y = 0, 0
    intersections_x_list = []
    intersections_y_list = []
    for segment in segments_list:
        intersection_x = barycentre(side_x, point, segment[0], segment[1])
        intersection_y = barycentre(side_y, point, segment[0], segment[1])
        if intersection_x is not None:
            # verification que les segments se coupent
            if point_in_segment(segment[0], segment[1], intersection_x):
                intersections_x_list.append(intersection_x)
        if intersection_y is not None:
            if point_in_segment(segment[0], segment[1], intersection_y):
                intersections_y_list.append(intersection_y)
    if len(intersections_x_list):
        # tri par les x croissants de tous les points d'intersection sur la droite horizontale
        intersections_x_list.sort(key=lambda tupple: tupple[0])
        for intersection in intersections_x_list:
            if point[0] > intersection[0]:
                # comptage du nombre d'intersections avant d'arriver au point
                cpt_x += 1 
    if len(intersections_y_list):
        # tri par les y croissants de tous les points d'intersection sur la droite verticale 
        intersections_y_list.sort(key=lambda tupple: tupple[1])
        for intersection in intersections_y_list:
            # comptage du nombre d'intersections avant d'arriver au point
            if point[1] > intersection[1]:
                cpt_y += 1
    if cpt_x % 2 != 0:
        # si le nombre d'intersections est impair alors on est dans le polygone 
        return True
    else: 
        # sinon on est en dehors
        return False

def polygon_by_clic(event, cnv):
    global coords_list
    x, y = event.x, event.y
    coords_list.append((x, y))
    cnv.create_oval(x-5, y-5, x+5, y+5, fill='blue', tag='point')

def polygon_by_txt(cnv):
    global segments_list, corner_list
    segments_list.clear()
    corner_list.clear()
    cnv.delete('point')
    # mettre dans un ficher txt par la suite, ici on evite les problemes de chemin qui ne seront pas les memes entre nos differents ordinateurs 
    point_list = [(243, 308), (243, 286), (242, 244), (206, 242), (171, 242), (145, 241), (125, 241), (99, 242), (76, 242), (42, 240), (42, 221), (41, 199), (40, 165), (39, 148), (39, 120), (38, 96), (36, 67), (36, 37), (62, 37), (81, 36), (103, 35), (105, 60), (104, 87), (82, 84), (65, 84), (65, 101), (65, 129), (65, 155), (65, 185), (65, 199), (86, 196), (113, 195), (136, 195), (166, 195), (198, 195), (196, 169), (196, 149), (152, 148), (110, 147), (106, 114), (131, 113), (131, 83), (131, 52), (154, 49), (174, 47), (175, 71), (175, 104), (196, 105), (215, 105), (220, 80), (220, 62), (226, 32), (249, 16), (276, 16), (310, 16), (342, 16), (345, 36), (323, 38), (288, 38), (267, 44), (267, 66), (264, 101), (287, 101), (320, 101), (358, 101), (376, 95), (375, 78), (375, 56), (375, 26), (407, 21), (427, 21), (438, 21), (437, 58), (437, 94), (436, 116), (434, 139), (432, 161), (434, 195), (434, 230), (434, 278), (433, 329), (383, 336), (319, 338), (246, 340)]
    cnv.create_polygon(point_list, fill='grey', outline='black')
    corner_list = point_list.copy()
    for i in range(len(point_list)-1):
        # creation de la liste des segments
        segments_list.append((point_list[i], point_list[i+1]))
    segments_list.append((point_list[-1], point_list[0]))

def draw(cnv):
    global coords_list, segments_list, corner_list
    if len(coords_list) >= 3:
        # 3 points minimum pour un polygone
        cnv.create_polygon(coords_list, fill='grey', outline='black')
        print(coords_list)
        segments_list.clear()
        corner_list.clear()
        for i in range(len(coords_list)-1):
            # creation de la liste des segments
            segments_list.append((coords_list[i], coords_list[i+1]))
        segments_list.append((coords_list[-1], coords_list[0]))
        # liste des sommets du polygone
        corner_list = coords_list.copy()
        coords_list.clear()
        cnv.delete('all')

def guardian_by_clic(event, cnv, segments_list):
    def light(x0, y0, side, segments_list):
        # initialisation
        light_list = []
        distance_list = []
        A1 = (x0, y0)
        A2 = side   # side is a point (tuple) of 2
        for segment in segments_list:
            B1 = segment[0]
            B2 = segment[1]
            intersection = barycentre(A1, A2, B1, B2)
            if intersection is not None:
                # verification de si les segments se coupent, et non les droites
                if point_in_segment(B1, B2, intersection) and point_in_segment(A1, A2, intersection):
                    light_list.append(intersection)
        if len(light_list):
            for inter in light_list:
                # calcul des distances pour toutes les intersections
                distance_list.append((distance_two_points(A1, inter), inter))
            # tri par rapport à la distance 
            distance_list.sort()
            cnv.create_line(A1[0], A1[1], distance_list[0][1][0], distance_list[0][1][1], tags='light', fill="yellow")

    x0, y0 = event.x, event.y
    # verification de si le gardien est dans la polygone
    if point_in_polygon((x0, y0), segments_list):
        cnv.delete('guardian')
        cnv.delete('light')
        # boucle qui prend tous les points du bord du canvas pour avoir toutes les directions possibles
        for width in range(0, 601, 50):
            for height in range(0, 401, 50):
                light(x0, y0, (width, height), segments_list)
        # creation du gardien
        cnv.create_oval(x0-5, y0-5, x0+5, y0+5, fill='black', tag='guardian')

def guardian_by_clic_on_corner(event, cnv, segments_list, corner_list):
    """ WIP, le bug indiqué dans la notice du projet est encore present """
    def light(x0, y0, corner, segments_list, corner_list):
        # initialisation
        light_list = []
        distance_list = []
        A1 = (x0, y0)
        A2 = corner  # corner is a point (tuple) of 2
        NO, NE, SO, SE = (0, 0), (600, 0), (0, 400), (600, 400)
        # modification de corner en side
        #####################
        # cette portion devra etre réécrite plus proprement
        top = barycentre(A1, A2, NO, NE)
        bottom = barycentre(A1, A2, SO, SE)
        left = barycentre(A1, A2, NO, SO)
        right = barycentre(A1, A2, NE, SE)
        if top is not None and point_in_segment(NO, NE, top):
            A2 = top
        elif bottom is not None and point_in_segment(SO, SE, bottom):
            A2 = bottom
        elif left is not None and point_in_segment(NE, SE, left):
            A2 = left
        elif right is not None and point_in_segment(NE, SE, right):
            A2 = right
        #########################
        for segment in segments_list:
            B1 = segment[0]
            B2 = segment[1]
            intersection = barycentre(A1, A2, B1, B2)
            if intersection is not None:
                # verification de si les segments se coupent, et non les droites
                if point_in_segment(B1, B2, intersection) and point_in_segment(A1, corner, intersection):
                    light_list.append(intersection)
        if len(light_list):
            for inter in light_list:
                # calcul des distances pour toutes les intersections
                distance_list.append((distance_two_points(A1, inter), inter))
            # tri par rapport à la distance 
            distance_list.sort()
            cnv.create_line(A1[0], A1[1], distance_list[0][1][0], distance_list[0][1][1], tags='light', fill="yellow")

    x0, y0 = event.x, event.y
    # verification de si le gardien est dans la polygone
    if point_in_polygon((x0, y0), segments_list):
        cnv.delete('guardian')
        cnv.delete('light')
        # boucle qui prend tous les points du bord du canvas pour avoir toutes les directions possibles
        for corner in corner_list:
                light(x0, y0, corner, segments_list, corner_list)
        # creation du gardien
        cnv.create_oval(x0-5, y0-5, x0+5, y0+5, fill='black', tag='guardian')

def delete_points(cnv):
    global coords_list
    cnv.delete('point')
    coords_list.clear()

def delete_all(cnv):
    global coords_list
    cnv.delete('all')
    coords_list.clear()

if __name__ == '__main__':
    # initialisation
    coords_list = []
    segments_list = []
    corner_list = []

    wnd = tk.Tk()
    wnd.title("Detection")
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    # boutton pour creer un polygone une fois les points placés
    draw_button = tk.Button(wnd, command=lambda: draw(cnv), text='Draw polygon !')
    draw_button.pack(side=tk.BOTTOM)
    # boutton creeant automatiquement une figure de type musée d'art
    draw_museum_button = tk.Button(wnd, command=lambda : polygon_by_txt(cnv), text='Museum')
    draw_museum_button.pack(side=tk.RIGHT)
    # boutton supprimant les points
    delete_point_button = tk.Button(wnd, command=lambda: delete_points(cnv), text='Delete all points')
    delete_point_button.pack(side=tk.BOTTOM)
    # boutton supprimant tous els elemets du canvas
    delete_all_button = tk.Button(wnd, command=lambda: delete_all(cnv), text='Delete all')
    delete_all_button.pack(side=tk.BOTTOM)
    # reglages des clics de la souris, <2> correspond au clic mollette pour windows, si le clic droit est souhaité il faut changer par <3> 
    cnv.bind('<1>', lambda event, cnv=cnv: polygon_by_clic(event, cnv))
    cnv.bind('<2>', lambda event, cnv=cnv: guardian_by_clic(event, cnv, segments_list))
    cnv.bind('<Double-Button-2>', lambda event, cnv=cnv: guardian_by_clic_on_corner(event, cnv, segments_list, corner_list))
    wnd.mainloop()
