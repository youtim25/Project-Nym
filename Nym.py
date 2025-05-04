import random
import json
import os
from tqdm import tqdm

nb_baton = int(input('Combien voulez-vous de bâtonnets ? : '))
choix = [[1, 2, 3] for _ in range(nb_baton)]

# Sauvegarde initiale
with open("choix.json", "w") as f:
    json.dump(choix, f)

def enleve_baton(nb):
    for _ in range(nb):
        if L:
            L.pop()

def verif_win(t):
    if not L and t == 'ia':
        return 'J'
    if not L and t == 'j':
        return 'IA'
    return False

def verif_coup():
    nb = input("Le nombre de bâtonnets : ")
    while nb == '':
        nb = input("RECOMMENCE : ")
    nb = int(nb)
    while nb not in [1, 2, 3]:
        print("Le coup n'est pas compté, recommencez.")
        nb = int(input("Le nombre de bâtonnets : "))
    return nb

def J():
    print(L)
    print('Combien voulez-vous retirer de bâtonnets ? (1, 2 ou 3)')
    nb = verif_coup()
    enleve_baton(nb)
    return nb

def J_auto():
    nb = random.choice([1, 2, 3])
    while len(L) < nb:
        nb = random.choice([1, 2, 3])
    enleve_baton(nb)
    return nb

def att():
    index = len(L) - 1
    if 0 <= index < nb_baton and choix[index]:
        return random.choice(choix[index])
    return random.choice([1, 2, 3])

def Ia_intelligente():
    global dernier_coup_ia, dernier_index
    index = len(L) - 1
    nb = att()
    while len(L) < nb:
        if nb in choix[index]:
            choix[index].remove(nb)
        if not choix[index]:
            nb = random.choice([1, 2, 3])
        nb = att()
    dernier_coup_ia = nb
    dernier_index = index
    enleve_baton(nb)
    return nb

def apprentissage(win):
    if win == 'J':
        if dernier_coup_ia in choix[dernier_index]:
            choix[dernier_index].remove(dernier_coup_ia)

# Chargement si fichier existant
if os.path.exists("Nym_stock.json"):
    with open("Nym_stock.json", "r") as f:
        choix = json.load(f)
else:
    choix = [[1, 2, 3] for _ in range(nb_baton)]

dernier_coup_ia = 0
dernier_index = 0

# Phase d'apprentissage
compteur = 0
ac = 1000000




"""
while ac > compteur :
    L = ['|'] * nb_baton
    t = 'j'
    win = False

    while not win:
        if t == 'j':
            Jnb = J_auto()
            t = 'ia'
        else:
            Inb = Ia_intelligente()
            t = 'j'
        win = verif_win(t)

    apprentissage(win)
    compteur +=1
"""








for _ in tqdm(range(ac), desc="Apprentissage de l'IA", unit="itération"):
    L = ['|'] * nb_baton
    t = 'j'
    win = False

    while not win:
        if t == 'j':
            Jnb = J_auto()
            t = 'ia'
        else:
            Inb = Ia_intelligente()
            t = 'j'
        win = verif_win(t)

    apprentissage(win)

# Sauvegarde finale
with open("choix.json", "w") as f:
    json.dump(choix, f)

# Affichage de l'état final des choix
print("État actuel :")
for k in range(nb_baton):
    print(f"{k + 1}: {choix[k]}")

# Partie interactive
r = 'oui'
while r == 'oui':
    r = input("Voulez-vous faire une partie contre l'IA ? (oui/non) : ").lower()
    if r == 'oui':
        L = ['|'] * nb_baton
        t = 'j'
        win = False
        while not win:
            if t == 'j':
                Jnb = J()
                t = 'ia'
            else:
                Inb = Ia_intelligente()
                t = 'j'
            win = verif_win(t)
        if t == 'ia':
            print("C'est le joueur qui a gagné.")
        else:
            print("C'est l'IA qui a gagné.")
