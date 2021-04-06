import tkinter as tk
from maths import barycentre, det

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
    cnv.create_oval(x0-5, y0-5, x0+5, y0+5, fill='black', tag='guardian')
    def light(x0, y0, segments_list):
        for i in range(0, 400, 100):
            for j in range(0, 600, 100):
                A1 = (x0, y0)
                A2 = (i, j)
                B1 = segments_list[0]
                B2 = segments_list[1]
                intersection = barycentre(A1, A2, B1, B2) 
                if intersection is not None:
                    if det(B1, B2, intersection) == 0:
                        if intersection[0] > B1[0] and intersection[0] < B2[0]:
                            cnv.create_line(A1[0], A1[1], intersection[0], intersection[1], tag='light')
                        elif intersection[1] > B1[1] and intersection[1] < B2[1]:
                            cnv.create_line(A1[0], A1[1], intersection[0], intersection[1], tag='light')
    for k in range(len(segments_list)):
        light(x0, y0, segments_list[k])

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

     
