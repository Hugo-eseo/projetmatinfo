# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 10:34:01 2021

@author: hugob
"""

import tkinter
import tkinter.filedialog

LST_Types = [ ( "Fichier texte" , ".txt" ) , ( "Autres types" , ".*" ) ]

def FNC_Selection ( ) :
    kfichier = tkinter.filedialog.asksaveasfilename ( title = "Enregistrer sous ..." , filetypes = LST_Types , defaultextension = ".txt" )
    print(kfichier)
    with open(kfichier,'w') as f:
        f.write("Hello world")
    print ( f"Vous avez créé :\n{ kfichier }" )

TKI_Principal = tkinter.Tk ( )
BUT_Quitter = tkinter.Button ( TKI_Principal , text = "Quitter" , command = TKI_Principal.destroy )
BUT_Enregistrer = tkinter.Button ( TKI_Principal , text = "Enregistrer sous ... " , command = FNC_Selection )

BUT_Enregistrer.pack ( )
BUT_Quitter.pack ( )

TKI_Principal.mainloop ( )