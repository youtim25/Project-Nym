import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os

# --- Paramètre initial ---
r = int(input('Nombre de bâtonnets ? '))

# --- Données globales ---
choix = [[1, 2, 3] for _ in range(r)]
L = ['nem'] * r
Jnb = Inb = 0
t = 'j'
win = None

# --- Lancement de la fenêtre principale ---
root = tk.Tk()
root.title("Jeu des Nems")
root.withdraw()  # on la cache pendant l'apprentissage

# --- Apprentissage IA avec barre de progression ---
def apprentissage_ia():
    global choix
    top = tk.Toplevel()
    top.title("Apprentissage de l'IA")
    tk.Label(top, text="Apprentissage en cours...").pack(pady=10)
    pb = ttk.Progressbar(top, orient='horizontal', length=300, mode='determinate')
    pb.pack(pady=20)

    nb_iterations = 1000
    choix = [[1, 2, 3] for _ in range(r)]

    def simulate():
        nonlocal nb_iterations
        for i in range(nb_iterations):
            L = ['nem'] * r
            t = 'j'
            Jnb = Inb = 0
            while L:
                if t == 'j':
                    Jnb = random.choice([1, 2, 3][:len(L)])
                    for _ in range(Jnb): L.pop()
                    t = 'ia'
                else:
                    index = max(0, min(Jnb + Inb - 1, r - 1))
                    nb = random.choice(choix[index]) if choix[index] else random.choice([1, 2, 3])
                    if len(L) >= nb:
                        for _ in range(nb): L.pop()
                        Inb = nb
                    else:
                        if nb in choix[index]: choix[index].remove(nb)
                    t = 'j'
            if t == 'j':
                index = max(0, min(Jnb + Inb - 1, r - 1))
                if Inb in choix[index]:
                    choix[index].remove(Inb)
            pb["value"] = int((i + 1) / nb_iterations * 100)
            top.update()
        top.destroy()
        root.deiconify()

    root.after(100, simulate)

apprentissage_ia()

# --- Chargement de l'image ---
BASE_DIR = os.path.dirname(__file__)
image_path = os.path.join(BASE_DIR, "Images", "nem.png")
img_nem_pil = Image.open(image_path).resize((60, 60))
img_nem = ImageTk.PhotoImage(img_nem_pil)

# --- Fonctions de jeu ---
def update_affichage():
    for widget in frame_nems.winfo_children():
        widget.destroy()
    for _ in L:
        tk.Label(frame_nems, image=img_nem).pack(side=tk.LEFT, padx=2)
    root.update()

def enleve_baton(nb):
    global L
    for _ in range(nb):
        if L:
            L.pop()
    update_affichage()

def verif_win(tour):
    if not L and tour == 'ia':
        return 'J'
    elif not L and tour == 'j':
        return 'IA'
    return False

def att(Jnb, Inb):
    index = max(0, min(Jnb - Inb - 1, r - 1))
    if choix[index]:
        return random.choice(choix[index])
    return random.choice([1, 2, 3])

def apprentissage(Jnb, Inb, gagnant):
    if gagnant == 'J':
        index = max(0, min(Jnb + Inb - 1, r - 1))
        if Inb in choix[index]:
            choix[index].remove(Inb)

def Ia_intelligente(Jnb, Inb):
    index = max(0, min(Jnb + Inb - 1, r - 1))
    nb = att(Jnb, Inb)
    while len(L) < nb:
        if nb in choix[index]: choix[index].remove(nb)
        if not choix[index]: return 1
        nb = att(Jnb, Inb)
    enleve_baton(nb)
    return nb

def tour_ia():
    global Inb, t, win
    Inb = Ia_intelligente(Jnb, Inb)
    t = 'j'
    win = verif_win(t)
    if win:
        apprentissage(Jnb, Inb, win)
        messagebox.showinfo("Fin de partie", f"{win} a gagné !")
        disable_buttons()
    else:
        enable_buttons()

def joueur_joue(nb):
    global Jnb, t, win
    disable_buttons()
    if len(L) < nb:
        messagebox.showwarning("Erreur", "Pas assez de nems à retirer.")
        enable_buttons()
        return
    Jnb = nb
    enleve_baton(nb)
    t = 'ia'
    win = verif_win(t)
    if win:
        messagebox.showinfo("Fin de partie", f"{win} a gagné !")
        disable_buttons()
    else:
        root.after(1000, tour_ia)

def disable_buttons():
    btn1.config(state=tk.DISABLED)
    btn2.config(state=tk.DISABLED)
    btn3.config(state=tk.DISABLED)

def enable_buttons():
    btn1.config(state=tk.NORMAL)
    btn2.config(state=tk.NORMAL)
    btn3.config(state=tk.NORMAL)

def reset_game():
    global L, Jnb, Inb, t, win
    L = ['nem'] * r
    Jnb = Inb = 0
    t = 'j'
    win = None
    update_affichage()
    enable_buttons()

# --- Interface ---
frame_nems = tk.Frame(root)
frame_nems.pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn1 = tk.Button(frame_buttons, text="Retirer 1 nem", font=("Arial", 12), command=lambda: joueur_joue(1))
btn2 = tk.Button(frame_buttons, text="Retirer 2 nems", font=("Arial", 12), command=lambda: joueur_joue(2))
btn3 = tk.Button(frame_buttons, text="Retirer 3 nems", font=("Arial", 12), command=lambda: joueur_joue(3))
btn1.grid(row=0, column=0, padx=5)
btn2.grid(row=0, column=1, padx=5)
btn3.grid(row=0, column=2, padx=5)

btn_reset = tk.Button(root, text="Rejouer", font=("Arial", 12), command=reset_game)
btn_reset.pack(pady=5)

update_affichage()
root.mainloop()
