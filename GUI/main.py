# coding: utf-8

import os
import sys
from functools import partial
from tkinter import Toplevel, Label, NW, Tk, Canvas, Menu, filedialog, Image, ttk, StringVar
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from allFilter import *

import matplotlib.pyplot as plt
from matplotlib.image import imread

import numpy as np

import subprocess

#sys.path.append(os.path.abspath("."))

class ImageAvecZoom:
    def __init__(self, chemin_image, img = False):
        self.root = gui
        if(img):
            self.image_originale = img
        else:
            self.chemin_image = chemin_image
            self.image_originale = Image.open(self.chemin_image)

        self.largeur, self.hauteur = self.image_originale.size

        self.facteur_zoom = 1.0

        self.child_window = Toplevel(gui)
        self.child_window.title("Image Viewer")
        self.child_window.geometry("800x800")

        self.canvas = Canvas(self.child_window, width=self.largeur, height=self.hauteur)
        self.canvas.pack()

        self.photo = ImageTk.PhotoImage(self.image_originale)
        self.image_affichee = self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

        self.canvas.bind("<MouseWheel>", self.zoomer)
        self.canvas.bind("<Button-1>", self.deplacer_image)

    def afficher_image(self):
        self.image_redimensionnee = self.image_originale.resize((int(self.largeur * self.facteur_zoom),
                                                                 int(self.hauteur * self.facteur_zoom)))
        self.photo = ImageTk.PhotoImage(self.image_redimensionnee)
        self.canvas.itemconfig(self.image_affichee, image=self.photo)

    def zoomer(self, event):
        if event.delta > 0:
            self.facteur_zoom *= 1.1  # Zoom in
        else:
            self.facteur_zoom /= 1.1  # Zoom out

        self.afficher_image()

    def deplacer_image(self, event):
        self.canvas.scan_mark(event.x, event.y)
        self.canvas.bind("<B1-Motion>", lambda e: self.deplacement_image(e))

    def deplacement_image(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


def open_help():
   top= Toplevel(gui)
   top.geometry("750x250")
   top.title("Child Window")
   msg = (
       "Vous vous trouvez actuellement dans une application permettant de retirer le bruit d'une image (espérons-le en tout cas).\n"
       "Importez une image depuis le menu 'Fichier', puis exécutez 'Run > Denoise' pour débruiter l'image avec l'IA.\n"
       "Vous pouvez également sélectionner un filtre pour un débruitage manuel.\n"
       "Une fois terminé, enregistrez les images souhaitées depuis le menu 'Fichier'.")
   Label(top, text= msg).place(x=20,y=20)

def openViewer_g(event):
    if resultImg[0]:
        open_imageViewer("", resultImg[0])

def openViewer_p(event):
    if resultImg[1]:
        open_imageViewer("", resultImg[1])

def openViewer_f(event):
    if resultImg[2]:
        open_imageViewer("", resultImg[2])

def open_imageViewer(path, img = False):
    image_zoom = ImageAvecZoom(path, img)
    image_zoom.afficher_image()


def tensorToImageConversion(Tensor):
    Tensor = Tensor*255
    Tensor = np.array(Tensor, dtype=np.uint8)
    if np.ndim(Tensor)>3:
        assert Tensor.shape[0] == 1
        Tensor = Tensor[0]
    return Image.fromarray(Tensor)

def importMainImage(mainCanvas, imgList, imgPathList):
    imgPath = importImage(mainCanvas, imgList, imgPathList, 0)
    # denoise(imgPath)
    # imgPathList[2] = "outImg/out.png"
    # importImage(colorTransfertCanvas, previewImgList, imgPathList, 1)


# comme on est en python on ne peut passer par référence que certaines chose, et oui. C'est pour ça "l'index"
def importImage(canvas, imgList, imgPathList, img_index):

    filepath = askopenfilename(title="Ouvrir une image",filetypes=[('all files','.*')])
    imgPreview = Image.open(filepath)
    imgPathList[img_index] = filepath

    resized_image = imgPreview.resize((50,50))
    imgList[img_index] = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=NW, image=imgList[img_index])
    return filepath


def saveImage(index):
    ftype = [('PNG', '*.png'), ('JPEG', '*.jpg'), ('PPM', '*.ppm')]

    filename = filedialog.asksaveasfilename(filetypes=ftype, defaultextension=".png")

    if filename and resultImg[index]:
        # Récupérer l'extension choisie à partir du nom de fichier
        file_extension = filename.split(".")[-1].lower()

        # Sauvegarder l'image avec l'extension correcte
        resultImg[index].save(filename)

def saveC():
    saveImage(0)

def saveS():
    saveImage(1)

def saveF():
    saveImage(2)

def waitText(canva):
    canva.create_text(256, 256, text="Calul en cours ...", font=("Arial", 20), tag="text",  fill="red")
    canva.pack()
    x_ = canva.winfo_x()
    y_ = canva.winfo_y()
    canva.place(x = x_, y = y_)

def denoise(canva, previewImgList, result, imgPathList):

    if not imgPathList[0]:
        print("ya pas d'image gros")
        return

    waitText(canva)
    waitText(IA_P_Canva)
    gui.update()

    command_g = [
    "python",                # Commande Python
    "config.py",             # Nom du script à exécuter
    "infer-image",           # Argument --image
    "--image",               # Option --image
    imgPathList[0],  # Valeur pour --image
    "--out",                 # Option --out
    "outImg/outg.png",        # Valeur pour --out
    "--network-snapshot",    # Option --network-snapshot
    "models/gaussian_ia.pickle"  # Valeur pour --network-snapshot
    ]

    command_p = [
        "python",  # Commande Python
        "config.py",  # Nom du script à exécuter
        "infer-image",  # Argument --image
        "--image",  # Option --image
        imgPathList[0],  # Valeur pour --image
        "--out",  # Option --out
        "outImg/outp.png",  # Valeur pour --out
        "--network-snapshot",  # Option --network-snapshot
        "models/poisson_ia.pickle"  # Valeur pour --network-snapshot
    ]

    subprocess.run(command_g)
    subprocess.run(command_p)

    imgPathList[1] = "outImg/outg.png"
    imgPathList[2] = "outImg/outp.png"

    denoisedImg_g = Image.open(imgPathList[1])
    denoisedImg_p = Image.open(imgPathList[2])

    resultImg[0] = denoisedImg_g
    resultImg[1] = denoisedImg_p

    resized_imageg = denoisedImg_g.resize((512,512))
    resized_imagep = denoisedImg_p.resize((512, 512))

    previewImgList[1] =  ImageTk.PhotoImage(image=resized_imageg, master = gui)
    previewImgList[2] = ImageTk.PhotoImage(image=resized_imagep, master=gui)

    canva.create_image(0,0, anchor=NW, image = previewImgList[1])
    IA_P_Canva.create_image(0, 0, anchor=NW, image=previewImgList[2])


def option_selected_filter(event):
    selected_option = dropdown.get()  # Récupère l'option sélectionnée

    img = Image.open(imgPathList[0])

    if(selected_option == "Gaussian"):
        waitText(Filtre_Canva)
        gui.update()
        res = gaussian_filter(img, 5, 1.5)
        resultImg[2] = res
        resized_image = res.resize((512, 512))
        previewImgList[3] = ImageTk.PhotoImage(image=resized_image, master=gui)
        Filtre_Canva.create_image(0,0, anchor=NW, image = previewImgList[3])

    elif (selected_option == "Median"):
        waitText(Filtre_Canva)
        gui.update()
        res = median_filter_color(img, 3)
        resultImg[2] = res
        resized_image = res.resize((512, 512))
        previewImgList[3] = ImageTk.PhotoImage(image=resized_image, master=gui)
        Filtre_Canva.create_image(0, 0, anchor=NW, image=previewImgList[3])
    elif (selected_option == "Hole_Filling"):
        waitText(Filtre_Canva)
        gui.update()
        res = hole_filling_color(img, 3)
        resultImg[2] = res
        resized_image = res.resize((512, 512))
        previewImgList[3] = ImageTk.PhotoImage(image=resized_image, master=gui)
        Filtre_Canva.create_image(0, 0, anchor=NW, image=previewImgList[3])


# ------------------------------ Layout ------------------------------ #

# preview, style, palette, transferColor, TransferStyle // les images resize pour la preview dans le logiciel
previewImgList = [None, None, None, None, None]
imgPathList = [None, None, None, None, None]

# les images non resize, 0 = Gaussian_IA, 1 = Poisson_IA, 2 = Filtres
resultImg = [None, None, None]

gui = Tk()
gui.title("Denoisingz")

gui.geometry("1656x552")

# ------------------------ image preview / style ---------------------------- #

label_preview = Label(gui, text = "Preview :")
label_preview.pack()
label_preview.place(x = 20, y = 0)

previewCanvas = Canvas(gui, width=50, height=50, bg="white")
previewCanvas.pack()
previewCanvas.place(x = 20,y = 20)

label_style = Label(gui, text = "Image Débruitée Gauss :")
label_style.pack()
label_style.place(x = 80, y = 0)

IA_G_Canva = Canvas(gui, width=512, height=512, bg="white")
IA_G_Canva.pack()
IA_G_Canva.place(x = 80,y = 20)
IA_G_Canva.bind("<Button-1>", openViewer_g)

label_TColor_txt = Label(gui, text = "Image Débruitée Poisson :")
label_TColor_txt.pack()
label_TColor_txt.place(x = 602, y = 0)

IA_P_Canva = Canvas(gui, width=512, height=512, bg="white")
IA_P_Canva.pack()
IA_P_Canva.place(x = 602, y = 20)
IA_P_Canva.bind("<Button-1>", openViewer_p)

label_filtres = Label(gui, text = "Débruitage par filtre :")
label_filtres.pack()
label_filtres.place(x = 1124, y = 0)

Filtre_Canva = Canvas(gui, width=512, height=512, bg="white")
Filtre_Canva.pack()
Filtre_Canva.place(x = 1124, y = 20)
Filtre_Canva.bind("<Button-1>", openViewer_f)


# ----------------------------- Menu ----------------------------- #

menubar = Menu(gui)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Importer l'image à modifier", command = partial(importMainImage, previewCanvas, previewImgList, imgPathList))
menu1.add_separator()
menu1.add_command(label="Enregistrer l'image débruité IA_Gauss", command = saveC)
menu1.add_command(label="Enregistrer l'image débruité IA_Poisson", command = saveS)
menu1.add_command(label="Enregistrer l'image débruité Filtre", command = saveF)
menu1.add_separator()
menu1.add_command(label="Quitter", command=gui.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Denoise", command = partial(denoise, IA_G_Canva, previewImgList, resultImg, imgPathList))
menubar.add_cascade(label="Run", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=open_help)
menubar.add_cascade(label="Aide", menu=menu3)

gui.config(menu=menubar)


filter_list = ["Aucun", "Gaussian", "Median", "Hole_Filling"]
selected_filter = StringVar(gui)
selected_filter.set(filter_list[0])
dropdown = ttk.Combobox(gui, textvariable=selected_filter, values=filter_list, state="readonly")
dropdown.place(x = 1250, y = 0)
dropdown.bind("<<ComboboxSelected>>", option_selected_filter)

# -------------------------------------------------------------------- #


# filepath = "img/1.jpg"
# imgPreview = Image.open(filepath)
# imgPathList[0] = filepath
#
# resized_image = imgPreview.resize((50,50))
# previewImgList[0] = ImageTk.PhotoImage(resized_image)
# previewCanvas.create_image(0, 0, anchor=NW, image=previewImgList[0])


gui.mainloop()