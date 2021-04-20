import tkinter as tk
from maths import barycentre, det, distance_two_points, point_in_segment, middle, find_direction, angle_two_points
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
    if cpt_x % 2 != 0 and cpt_y % 2 != 0:
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
    cnv.delete('all')
    # mettre dans un ficher txt par la suite, ici on evite les problemes de chemin qui ne seront pas les memes entre nos differents ordinateurs 
    point_list = [(243, 308), (244, 286), (242, 244), (206, 242), (171, 243), (145, 241), (125, 242), (99, 241), (76, 242), (43, 240), (42, 221), (41, 199), (40, 165), (39, 148), (38, 120), (37, 96), (36, 67), (35, 37), (62, 38), (81, 36), (103, 35), (105, 60), (104, 87), (82, 84), (62, 83), (63, 101), (64, 129), (65, 155), (66, 185), (67, 199), (86, 196), (113, 195), (136, 194), (166, 193), (198, 195), (196, 169), (195, 149), (152, 148), (110, 147), (106, 114), (131, 113), (132, 83), (131, 52), (154, 49), (174, 47), (175, 71), (174, 104), (196, 105), (215, 105), (220, 80), (221, 62), (226, 32), (249, 16), (276, 17), (310, 16), (342, 17), (345, 36), (323, 38), (288, 37), (267, 44), (267, 66), (264, 101), (287, 100), (320, 101), (358, 100), (376, 95), (375, 78), (373, 56), (375, 26), (407, 21), (427, 22), (438, 21), (437, 58), (438, 94), (436, 116), (434, 139), (432, 161), (434, 195), (432, 230), (434, 278), (433, 329), (383, 336), (319, 338), (246, 340)]
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
        cnv.delete('all')
        cnv.create_polygon(coords_list, fill='grey', outline='black')
        segments_list.clear()
        corner_list.clear()
        for i in range(len(coords_list)-1):
            # creation de la liste des segments
            segments_list.append((coords_list[i], coords_list[i+1]))
        segments_list.append((coords_list[-1], coords_list[0]))
        # liste des sommets du polygone
        corner_list = coords_list.copy()
        coords_list.clear()

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
    global polygon_list
    """ WIP, le bug indiqué dans la notice du projet est encore present """
    def light(x0, y0, corner, segments_list, corner_list):
        global polygon_list
        # initialisation
        light_list = []
        distance_list = []
        A1 = (x0, y0) 
        NO, NE, SO, SE = (0, 0), (600, 0), (0, 400), (600, 400)
        ########################
        # modification de corner en side
        ## reecrire plus proprement 
        direction = find_direction(A1, corner)
        if direction == 'NO':
            top = barycentre(A1, corner, NE, NO)
            left = barycentre(A1, corner, NO, SO)
            if top is not None and point_in_segment(NO, NE, top):
                A2 = top
            else:
                A2 = left
        elif direction == 'N':
            top = barycentre(A1, corner, NE, NO)
            if top is not None and point_in_segment(NO, NE, top):
                A2 = top
        elif direction == 'NE':
            top = barycentre(A1, corner, NE, NO)
            right = barycentre(A1, corner, SE, NE)
            if top is not None and point_in_segment(NO, NE, top):
                A2 = top
            else:
                A2 = right
        elif direction == 'E':
            right = barycentre(A1, corner, SE, NE)
            if right is not None and point_in_segment(NE, SE, right):
                A2 = right
        elif direction == 'SE':
            bottom = barycentre(A1, corner, SO, SE)
            right = barycentre(A1, corner, SE, NE)
            if bottom is not None and point_in_segment(SE, SO, bottom):
                A2 = bottom
            else:
                A2 = right
        elif direction == 'S':
            bottom = barycentre(A1, corner, SO, SE)
            if bottom is not None and point_in_segment(SE, SO, bottom):
                A2 = bottom
        elif direction == 'SO':
            bottom = barycentre(A1, corner, SO, SE)
            left = barycentre(A1, corner, NO, SO)
            if bottom is not None and point_in_segment(SE, SO, bottom):
                A2 = bottom
            else:
                A2 = left
        elif direction == 'O':
            left = barycentre(A1, corner, NO, SO)
            if left is not None and point_in_segment(SO, NO, left):
                A2 = left
        #########################
        for segment in segments_list:
            B1 = segment[0]
            B2 = segment[1]
            intersection = barycentre(A1, A2, B1, B2)
            if intersection is not None:
                # verification de si les segments se coupent, et non les droites
                if point_in_segment(B1, B2, intersection) and point_in_segment(A1, A2, intersection):
                    light_list.append(intersection)
        for inter in light_list:
            # calcul des distances pour toutes les intersections
            distance_list.append((distance_two_points(A1, inter), inter))
        # tri par rapport à la distance 
        distance_list.sort()
        if len(distance_list) >= 2 and isclose(distance_list[0][0], distance_list[1][0], rel_tol=0.01):
            distance_list.pop(0)
        cnv.create_line(A1[0], A1[1], distance_list[0][1][0], distance_list[0][1][1], tag='light', fill="yellow")
        for corner in corner_list:
            if isclose(distance_list[0][1][0], corner[0], rel_tol=0.01) and isclose(distance_list[0][1][1], corner[1], rel_tol=0.01):
                polygon_list.append(((distance_list[0][1][0], distance_list[0][1][1]), "angle"))
        else: 
            polygon_list.append(((distance_list[0][1][0], distance_list[0][1][1]), "mur simple"))
        if len(distance_list) >= 2:
            for corner in corner_list:
                if isclose(distance_list[0][1][0], corner[0], rel_tol=0.01) and isclose(distance_list[0][1][1], corner[1], rel_tol=0.01):
                    # milieu des deux intersections
                    middle_point = middle(distance_list[0][1], distance_list[1][1])
                    if point_in_polygon(middle_point, segments_list):
                        # si le milieu est dans le polygone, alors on dessine la lumiere jusqu'a la 2eme intersection 
                        cnv.create_line(distance_list[0][1][0], distance_list[0][1][1], distance_list[1][1][0], distance_list[1][1][1], tag='light', fill="blue")   
                        polygon_list.append(((distance_list[1][1][0], distance_list[1][1][1]), "projeté d'un angle"))
    x0, y0 = event.x, event.y
    polygon_list_corner = []
    final_polygon = []
    light_poly_coords = []
    # verification de si le gardien est dans la polygone
    if point_in_polygon((x0, y0), segments_list):
        cnv.delete('guardian')
        cnv.delete('light')
        cnv.delete('polyLight')
        polygon_list.clear()
        # boucle qui prend tous les points du bord du canvas pour avoir toutes les directions possibles
        for corner in corner_list:
            light(x0, y0, corner, segments_list, corner_list)
        # creation du polygone de lumiere
        for elem in polygon_list:
            if elem[1] != 'mur simple':
                polygon_list_corner.append(elem)
        ############
        # besoin de trier, peut etre avec atan2 pour avoir les points dans le sens des aiguilles d'une montre
        for elem in polygon_list_corner:
            final_polygon.append((angle_two_points(elem[0], (x0, y0)), elem[1], elem[0]))
        final_polygon.sort()
        for i in range(len(final_polygon)-1):
            if isclose(final_polygon[i][0], final_polygon[i+1][0], rel_tol=0.01):
                if find_direction((x0, y0), final_polygon[i][2]) == "NE" or find_direction((x0, y0), final_polygon[i][2]) == "E" or find_direction((x0, y0), final_polygon[i][2]) == "SE" or find_direction((x0, y0), final_polygon[i][2]) == "N":
                    if final_polygon[i][1] == "angle":
                        final_polygon[i], final_polygon[i+1] = final_polygon[i+1], final_polygon[i]
                elif find_direction((x0, y0), final_polygon[i][2]) == "NO" or find_direction((x0, y0), final_polygon[i][2]) == "O" or find_direction((x0, y0), final_polygon[i][2]) == "SO" or find_direction((x0, y0), final_polygon[i][2]) == "S":
                    if final_polygon[i][1] == "projeté d'un angle":
                        final_polygon[i], final_polygon[i+1] = final_polygon[i+1], final_polygon[i]
        for elem in final_polygon:
            light_poly_coords.append(elem[2])
        cnv.create_polygon(light_poly_coords, fill="yellow", tag="light")
        ############
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
    polygon_list = []

    wnd = tk.Tk()
    wnd.title("Detection")
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    # boutton pour creer un polygone une fois les points placés
    draw_button = tk.Button(wnd, command=lambda: draw(cnv), text='Draw polygon !').pack(side=tk.BOTTOM)
    # boutton creeant automatiquement une figure de type musée d'art
    draw_museum_button = tk.Button(wnd, command=lambda : polygon_by_txt(cnv), text='Museum').pack(side=tk.RIGHT)
    # boutton supprimant les points
    delete_point_button = tk.Button(wnd, command=lambda: delete_points(cnv), text='Delete all points').pack(side=tk.BOTTOM)
    # boutton supprimant tous els elemets du canvas
    delete_all_button = tk.Button(wnd, command=lambda: delete_all(cnv), text='Delete all').pack(side=tk.BOTTOM)
    # reglages des clics de la souris, <2> correspond au clic mollette pour windows, si le clic droit est souhaité il faut changer par <3> 
    cnv.bind('<1>', lambda event, cnv=cnv: polygon_by_clic(event, cnv))
    cnv.bind('<Button-2>', lambda event, cnv=cnv: guardian_by_clic(event, cnv, segments_list))
    cnv.bind('<Double-Button-2>', lambda event, cnv=cnv: guardian_by_clic_on_corner(event, cnv, segments_list, corner_list))

    wnd.mainloop()
