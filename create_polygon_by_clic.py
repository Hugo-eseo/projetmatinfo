import tkinter as tk

def polygon_by_clic(event, cnv):
    global coords_list
    x, y = event.x, event.y
    coords_list.append((x, y))
    cnv.create_oval(x-5, y-5, x+5, y+5, fill='blue', tag='point')

def draw(cnv):
    global coords_list
    cnv.create_polygon(coords_list, fill='grey', outline='black')
    coords_list.clear()
    cnv.delete('point')

if __name__ == '__main__':
    # few variables
    coords_list = []

    wnd = tk.Tk()
    wnd.title("Detection")
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    draw_button = tk.Button(wnd, command=lambda: draw(cnv), text='Draw polygon !')
    draw_button.pack(side=tk.BOTTOM)
    clear_button = tk.Button(wnd, command=lambda: cnv.delete('all'), text='Delete all')
    clear_button.pack(side=tk.BOTTOM)
    cnv.bind('<Button-1>', lambda event, cnv=cnv: polygon_by_clic(event, cnv))
    wnd.mainloop()

     


