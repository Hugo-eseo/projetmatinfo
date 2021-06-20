import tkinter as tk

class gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse):
        self.position = Point   # position en pixels
        self.direction = direction # en degrés
        self.angle = angle  # en degrés
        self.puissance = puissance    # puissance de la torche en pixels
        self.vitesse = vitesse  # vitesse de deplacement

    def move(self):
        pass

    def turn(self):
        pass

    def eclaire(self):
        pass

class voleur:
    def __init__(self, Point, direction, angle, vitesse):
        self.position = Point   # position en pixels
        self.direction = direction # en degrés
        self.angle = angle  # en degrés
        self.puissance = puissance    # puissance de la torche en pixels
        self.vitesse = vitesse  # vitesse de deplacement
        self.score = 0

    def move(self):
        pass

    def active(self):
        pass

def creer_niveau(cnv, niveau):
    """
    
    """
    cnv.delete('all')
    cnv.create_polygone(niveau, fill='grey', outline='black')
    liste_segments = 


    
# parametres du jeu
width_canvas, height_canvas = 600, 400
width_frame, height_frame = 100, 400


# création de l'interface graphique
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=width_canvas, height=height_canvas)
cnv.pack(side=tk.LEFT)
frm = tk.Frame(wnd, width=width_frame, height=height_frame)
frm.pack(side=tk.RIGHT)


wnd.mainloop()
