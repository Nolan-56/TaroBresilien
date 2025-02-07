"""
Fichier Cartes.py

Permet de gerer les differentes cartes utilisees dans le jeu
"""
import pygame
import os
import sys



CHEMIN_RESSOURCE = "image"
def getRessource(ressource):
    """Permet de gerer le chemin pour acceder aux images dans l'executable

    Args:
        ressource(str) : image que l'on souhaite acceder

    Returns:
        chemin de l'image    
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, CHEMIN_RESSOURCE) + "/" + ressource


def valeur_image(val):
    """Permet d'associer chaque cartes a une valeur entiere.

    Args:
        val(str) : valeur de la carte qu'on souhaite avoir son chemin

    Returns:
        chemin de la carte 
    """
    image = {
        "0" : getRessource("Demi_Valeur0.jpg"),
        "1" : getRessource("Demi_Valeur1.jpg"),
        "2" : getRessource("Demi_Valeur2.jpg"),
        "3" : getRessource("Demi_Valeur3.jpg"),
        "4" : getRessource("Demi_Valeur4.jpg"),
        "5" : getRessource("Demi_Valeur5.jpg"),
        "6" : getRessource("Demi_Valeur6.jpg"),
        "7" : getRessource("Demi_Valeur7.jpg"),
        "8" : getRessource("Demi_Valeur8.jpg"),
        "9" : getRessource("Demi_Valeur9.jpg"),
        "10" : getRessource("Demi_Valeur10.jpg"),
        "11" : getRessource("Demi_Valeur11.jpg"),
        "12" : getRessource("Demi_Valeur12.jpg"),
        "13" : getRessource("Demi_Valeur13.jpg"),
        "14" : getRessource("Demi_Valeur14.jpg"),
        "15" : getRessource("Demi_Valeur15.jpg"),
        "16" : getRessource("Demi_Valeur16.jpg"),
        "17" : getRessource("Demi_Valeur17.jpg"),
        "18" : getRessource("Demi_Valeur18.jpg"),
        "19" : getRessource("Demi_Valeur19.jpg"),
        "20" : getRessource("Demi_Valeur20.jpg"),
        "21" : getRessource("Demi_Valeur21.jpg"),
        "22" : getRessource("Demi_Valeur22.jpg"),
        "23" : getRessource("Demi_Valeur23.jpg")
    }

    return image[val]

