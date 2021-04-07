import tkinter as tk
from maths import barycentre, det, distance_two_points, find_direction

def point_in_polygon(point, segments_list):
    side_x = (0, point[1])
    side_y = (point[0], 0)
    cpt_x, cpt_y = 0, 0
    intersections_x_list = []
    intersections_y_list = []
    for segment in segments_list:
        intersection_x = barycentre(side_x, point, segment[0], segment[1])
        intersection_y = barycentre(side_y, point, segment[0], segment[1])
        if intersection_x is not None:
            if (intersection_x[0] > segment[0][0] and intersection_x[0] < segment[1][0]) or (intersection_x[0] < segment[0][0] and intersection_x[0] > segment[1][0]):
                intersections_x_list.append(intersection_x)
        if intersection_y is not None:
            if (intersection_y[1] > segment[0][1] and intersection_y[1] < segment[1][1]) or (intersection_y[1] < segment[0][1] and intersection_y[1] > segment[1][1]):
                intersections_y_list.append(intersection_y)
    if len(intersections_x_list):
        intersections_x_list.sort(key=lambda tupple: tupple[0])
        for intersection in intersections_x_list:
            if point[0] > intersection[0]:
                cpt_x += 1 
    if len(intersections_y_list):
        intersections_y_list.sort(key=lambda tupple: tupple[1])
        for intersection in intersections_y_list:
            if point[1] > intersection[1]:
                cpt_y += 1
    if cpt_x % 2 != 0 and cpt_y % 2 != 0:
        return True
    else: 
        return False    

def polygon_by_clic(event, cnv):
    global coords_list
    x, y = event.x, event.y
    coords_list.append((x, y))
    cnv.create_oval(x-5, y-5, x+5, y+5, fill='blue', tag='point')

def draw(cnv):
    global coords_list, segments_list
    if len(coords_list):
        cnv.create_polygon(coords_list, fill='grey', outline='black')
        segments_list.clear()
        for i in range(len(coords_list)-1):
            segments_list.append((coords_list[i], coords_list[i+1]))
        segments_list.append((coords_list[-1], coords_list[0]))
        coords_list.clear()
        cnv.delete('point')

def guardian_by_clic(event, cnv, segments_list):
    cnv.delete('guardian')
    cnv.delete('light')
    x0, y0 = event.x, event.y
    is_in_polygon = point_in_polygon((x0, y0), segments_list)
    def light(x0, y0, side, segments_list):
        light_list = []
        # side is a point (tuple) of 2
        for segment in segments_list:
            A1 = (x0, y0)
            A2 = side
            B1 = segment[0]
            B2 = segment[1]
            intersection = barycentre(A1, A2, B1, B2)
            direction1 = []
            direction2 = []
            distances1 = []
            distances2 = []
            if intersection is not None:
                if (intersection[0] > B1[0] and intersection[0] < B2[0]) or (intersection[0] < B1[0] and intersection[0] > B2[0]):
                    light_list.append(intersection)
                elif (intersection[1] > B1[1] and intersection[1] < B2[1]) or (intersection[1] < B1[1] and intersection[1] > B2[1]):
                    light_list.append(intersection)
        if len(light_list):
            direction = find_direction(A1, light_list[0])
        for inter in light_list:
            if find_direction(A1, inter) == direction:
                direction1.append(inter)
            else:
                direction2.append(inter)
        for inter in direction1:
            distances1.append((distance_two_points(A1, inter), inter))
        for inter in direction2:
            distances2.append((distance_two_points(A1, inter), inter))
        distances1.sort(key=lambda tupple: tupple[0])
        distances2.sort(key=lambda tupple: tupple[1])
        if len(distances1):
            cnv.create_line(A1[0], A1[1], distances1[0][1][0], distances1[0][1][1], tags='light', fill="yellow", width=1)
        if len(distances2):
            cnv.create_line(A1[0], A1[1], distances2[0][1][0], distances2[0][1][1], tags='light', fill="yellow", width=1)
    if is_in_polygon:
        for width in range(0, 601, 100):
            for height in range(0, 401, 100):
                light(x0, y0, (width, height), segments_list)
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
    # few variables
    coords_list = []
    segments_list = []

    wnd = tk.Tk()
    wnd.title("Detection")
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    draw_button = tk.Button(wnd, command=lambda: draw(cnv), text='Draw polygon !')
    draw_button.pack(side=tk.BOTTOM)
    delete_point_button = tk.Button(wnd, command=lambda: delete_points(cnv), text='Delete all points')
    delete_point_button.pack(side=tk.BOTTOM)
    delete_all_button = tk.Button(wnd, command=lambda: delete_all(cnv), text='Delete all')
    delete_all_button.pack(side=tk.BOTTOM)
    cnv.bind('<1>', lambda event, cnv=cnv: polygon_by_clic(event, cnv))
    cnv.bind('<2>', lambda event, cnv=cnv: guardian_by_clic(event, cnv, segments_list))
    wnd.mainloop()
