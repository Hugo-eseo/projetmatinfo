from math import sqrt, isclose, atan2
import time
import tkinter as tk

def det(m, n, p):
    # m, n, p tuples of 2
    det = m[0] * n[1] + m[1] * p[0] + n[0] * p[1]
    det -= m[1] * n[0] + m[0] * p[1] + n[1] * p[0]
    return det

def barycentre(A1, A2, B1, B2):
    # A1, A2, B1, B2 tuples of 2
    part1 = (det(B1, B2, A2) * A1[0], det(B1, B2, A2) * A1[1])
    part2 = (det(B2, B1, A1) * A2[0], det(B2, B1, A1) * A2[1])
    numerateur = (part1[0] + part2[0], part1[1] + part2[1])
    denominateur = det(B1, B2, A2) + det(B2, B1, A1)
    if denominateur == 0: return None
    I = (numerateur[0] / denominateur, numerateur[1] / denominateur)
    return I

def angle_two_points(point, center):
    # a, b tuples of 2 
    angle = atan2(point[1] - center[1], point[0] - center[0])
    return angle

def find_direction(a, b):
    # a, b tuples of 2
    if a[0] > b[0]:
        if a[1] > b[1]:
            return "NO"
        elif a[1] < b[1]:
            return "SO"
        else:
            return "O"
    elif a[0] < b[0]:
        if a[1] > b[1]:
            return "NE"
        elif a[1] < b[1]:
            return "SE"
        else:
            return "E"
    else:
        if a[1] > b[1]:
            return "N"
        elif a[1] < b[1]:
            return "S"
        else:
            return None

def point_in_segment(a, b, c):
    # les points doivent etre alignés 
    AB = distance_two_points(a, b)
    AC = distance_two_points(a, c)
    BC = distance_two_points(b, c)
    return isclose(AC + BC, AB, rel_tol=0.01)

def distance_two_points(a, b):
    # a, b tuples of 2
    part1 = b[0] - a[0]
    part2 = b[1] - a[1]
    dist = sqrt(part1**2 + part2**2)
    return dist

def middle(a, b):
    # a, b tuples of 2 
    middle = (((a[0] + b[0]) / 2), ((a[1] + b[1]) / 2))
    return middle

def droite(event):
    global points, droite_list
    points.append((event.x, event.y))
    if len(points) == 2:
        cnv.create_line(points, tag="droite")
        droite_list.append(points.copy())
        points.clear()

def intersection(segment1, segment2, cnv):
    I = barycentre(segment1[0], segment1[1], segment2[0], segment2[1])
    if point_in_segment(segment1[0], segment1[1], I) and point_in_segment(segment2[0], segment2[1], I):
        cnv.create_oval(I[0]-5, I[1]-5, I[0]+5, I[1]+5, fill='blue', tag='point')

if __name__ == '__main__':
    points = []
    droite_list = []
    wnd = tk.Tk()
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    boutton = tk.Button(wnd, text="intersect", command= lambda droite_list=droite_list, cnv=cnv : intersection(droite_list[0], droite_list[1], cnv)).pack(side=tk.BOTTOM)
    cnv.bind('<1>', droite)
    wnd.mainloop()