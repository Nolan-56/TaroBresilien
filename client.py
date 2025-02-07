"""
Fichier client.py
"""
import pygame
import re
from Network import Network
import Fonction_a_utiliser
import time
import sys
import os
import socket



class Network:
    def __init__(self,addresse):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.112" # Remplacez par l'adresse IP de votre serveur
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except Exception as e:
            print(f"Impossible de se connecter au serveur : {e}")

    def send(self, data):
        try:
            self.client.send(data.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")

    def receive(self):
        try:
            return self.client.recv(2048).decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")
            return None


# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
nombreJoueurs = 4

CHEMIN_RESSOURCE = "image"

def getRessource(ressource):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, CHEMIN_RESSOURCE) + "/" + ressource


# Chargement de l'image
BACKGROUND_IMAGE = pygame.image.load(getRessource("essai.jpg"))

# Classes
class Client:
    def __init__(self, client_id, name="Player"):
        self.id = client_id
        self.name = name
        self.score = 0

    def update_score(self, value):
        self.score -= value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

# Fonctions utilitaires
def decrypt_id(message):
    resultat = re.search(r'\d+', message)
    if resultat:
        print(resultat.group()) 
        return resultat.group()

def decrypt_message(message):
    """Extrait les cartes du message reçu."""
    pattern = r"Vos cartes : \[([^\]]+)\]"
    match = re.search(pattern, message)
    if match:
        cards_str = match.group(1)
        return [int(card) for card in cards_str.split(", ")]
    return []

def decrypt_card_value(card_path):
    """Extrait la valeur de la carte à partir de son chemin d'image."""
    pattern = r"Demi_Valeur(\d+)\.jpg"
    match = re.search(pattern, card_path)
    if match:
        return int(match.group(1))
    return None

def decrypt_pos_carte(message):
    pattern = r"(\d+),(\d+)$"
    match = re.search(pattern, message)
    if match:
        x,y = match.groups()
        return (x,y)
    return []

def decryptId(message):
    pattern = r"(\d+)$"
    match = re.search(pattern, message)
    if match:
        result = match.group(1)
        return result


def decryptDerniereCarte(message):
    numbers = re.findall(r'\d+',message)
    result = list(map(int,numbers))
    return result

def decrypt_nom(list_of_strings):
    pattern = r"\((\d+),([a-zA-Z]+)\)"

    # Transformation en liste de tuples
    list_of_tuples = [tuple(match) for match in (re.match(pattern, s).groups() for s in list_of_strings)]

    # Optionnel : convertir les chiffres en entiers
    list_of_tuples = [(int(num), text) for num, text in list_of_tuples]
    
    return list_of_tuples

def decrypt_mise(message):
    pattern = r"\((\d+),(\d+)\)"
    match = re.match(pattern, message)
    if match:
        result = (int(match.group(1)), int(match.group(2)))
        return result



def send_value(value, network):
    """Envoie une valeur au serveur."""
    try:
        network.send(str(value))
        print(f"Valeur envoyée : {value}")
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")

def verifNom(nom):
    for e in nom:
        if not (('a' <= e <= 'z') or ('A' <= e <= 'Z')):
            return False
    return True



# Fonctionnalités du jeu
def initialize_player(network,scoreTour):
    """Initialise le joueur en demandant son nom."""
    name = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Nom ?", getRessource("essai.jpg"),scoreTour)
    if verifNom(name) == False:
        while verifNom(name) != True:
           name = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Nom incorrect, recommencer", getRessource("essai.jpg"),scoreTour) 
    network.send(name)
    Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente des joueurs...", getRessource("essai.jpg"),scoreTour)
    data = ""
    while data == "" or data == None:
        print("dataaaaa : ",data)
        data = wait_for_server_message(network)
        if data != "" or data != None:
            print("dardlzdldz : ",data)
            data = decrypt_id(data)
            Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,str(data), getRessource("essai.jpg"),scoreTour)
            return data


def wait_for_server_message(network):
    try:
        message = network.receive()
        print(f"Message reçu du serveur : {message}")  # Log à ajouter
        return message
    except Exception as e:
        print(f"Erreur lors de la réception du message du serveur : {e}")
        return None

def display_background():
    """Affiche l'image de fond."""
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.display.flip()

def handle_card_click(network, card_list, card_positions,nomPartie,miseTour,scorePartie,placement,dejaUtiliser,scoreTour,carteDuTour):
    """Gère le clic sur une carte, envoie sa valeur au serveur et renvoie la carte cliquée."""
    Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,'A vous de choisir une carte', getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list,dejaUtiliser,carteDuTour)
    while True:
        card_click = Fonction_a_utiliser.clic_carte(WINDOW, WIDTH, HEIGHT, getRessource("essai.jpg"), card_list, card_positions,dejaUtiliser,placement,scorePartie,miseTour,nomPartie,scoreTour,carteDuTour)
        
        if decrypt_card_value(card_click[0]) in dejaUtiliser:
            while decrypt_card_value(card_click[0]) in dejaUtiliser:
                card_click = Fonction_a_utiliser.clic_carte(WINDOW, WIDTH, HEIGHT, getRessource("essai.jpg"), card_list, card_positions,dejaUtiliser,placement,scorePartie,miseTour,nomPartie,scoreTour,carteDuTour)
        
        if card_click:
            card_path, position = card_click  # Récupère le chemin de l'image et la position de la carte cliquée
            value = decrypt_card_value(card_path)  # Extrait la valeur de la carte
            if value == 22:
                dejaUtiliser.append(int(22))
                value = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "0 ou 22 ?", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)
                if value == 22:
                    value = 24
            if value is not None:
                deplacer_carte(WINDOW,card_path,position)
                dejaUtiliser.append(int(value))
                value = getRessource("Demi_Valeur"+str(value)+".jpg")
                #value = "Documents/client/_internal/image/Demi_Valeur"+str(value)+".jpg"
                network.send(f"CarteJouee;{value};{position[0]},{position[1]}")  # Envoie au serveur
                pygame.display.flip()
                return (dejaUtiliser,value)
                """
                return {
                    "value": value,
                    "card_path": card_path,
                    "position": position
                }"""
            
            
def deplacer_carte(screen, carte_image, pos_depart):

    pos_x = pos_depart[0]
    pos_y = pos_depart[1]-150

    largeur_rect = 100
    hauteur_rect = 140

    image_carte = pygame.image.load(carte_image)
    image_carte = pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect))
    screen.blit(image_carte,(pos_x,pos_y))
    
def deplacerCarteOther(screen,largeur,hauteur,carte_image,pos_depart,joueurId,cont = True):

    if cont:
        res = Fonction_a_utiliser.carteJoueur(joueurId,hauteur,largeur)
            
        pos_x = res[0]
        pos_y = res[1]

    largeur_rect = 70
    hauteur_rect = 110

    if joueurId == "D":
        image_carte = pygame.image.load(carte_image)
        image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),90)

        screen.blit(image_carte,(pos_x,pos_y))

    if joueurId == "G":
        image_carte = pygame.image.load(carte_image)
        image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),-90)

        screen.blit(image_carte,(pos_x,pos_y))

    if joueurId == "H":
        image_carte = pygame.image.load(carte_image)
        image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),180)

        screen.blit(image_carte,(pos_x,pos_y))

    
    pygame.display.flip()


def afficher_cartes_tour(screen, largeur, hauteur, cartes_jouees):

    for joueur, carte in cartes_jouees.items():
        res = Fonction_a_utiliser.carteJoueur(joueur,hauteur,largeur)
            
        pos_x = res[0]
        pos_y = res[1]
        
        if carte:

            if joueur == "D":
                image_carte = pygame.image.load(carte)
                image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (70,100)),90)

                screen.blit(image_carte,(pos_x,pos_y))

            if joueur == "G":
                image_carte = pygame.image.load(carte)
                image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (70,100)),-90)

                screen.blit(image_carte,(pos_x,pos_y))

            if joueur == "H":
                image_carte = pygame.image.load(carte)
                image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (70,100)),180)

                screen.blit(image_carte,(pos_x,pos_y))

            if joueur == "B":
                image_carte = pygame.image.load(carte)
                image_carte = pygame.transform.scale(image_carte, (100,140))

                screen.blit(image_carte,(pos_x,pos_y))

    pygame.display.flip()





    



def setup_cards(network,scoreTour):
    """Configure les cartes reçues du serveur."""
    #Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente des joueurs...", "Documents/Jeu Taro/image/essai.jpg")
    while True:
        server_message = wait_for_server_message(network)
        if server_message:
            print(f"Message du serveur : {server_message}")
            card_list = decrypt_message(server_message)
            if card_list:
                
                card_positions = Fonction_a_utiliser.affichage_carte(WINDOW, WIDTH, HEIGHT, card_list,getRessource("essai.jpg"),scoreTour)
                #Fonction_a_utiliser.afficher_score(WINDOW, WIDTH, HEIGHT, 0, 0, 0, 0)
                pygame.display.flip()
                return card_list, card_positions
    return card_list, card_positions   

def envoyerMise(network,card_list,nomPartie,miseTour,scorePartie,placement,nbCarte,scoreTour):
    data = wait_for_server_message(network)
    if data == "Choisit ta mise":
        mise = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Mise ?", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)
        
        if verifMise(mise) == False:
            while verifMise(mise) != True:
                 mise = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Mise incorrect, recommencer", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)
        
        
        if verifMiseTotal(mise,miseTour,nbCarte) == False:
            while verifMiseTotal(mise,miseTour,nbCarte) != True:
                 mise = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Vous ne pouvez pas miser "+str(mise), getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)

        network.send(mise)
        Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente du choix des autres",getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)
        return mise
    else:
        Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente du choix des autres",getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_list)
        return 

            
def carteDuJoueur(network):
    server_message = wait_for_server_message(network)
    if server_message[:9] == "Vos cartes":
        return decrypt_message(server_message)

def natureMessage(messageRecu,messageAttendu):
    return messageRecu == messageAttendu

def attendre_tour(card_positions,nomPartie,miseTour,scorePartie,placement,dejaUtiliser,carteTour,scoreTour):
    Fonction_a_utiliser.afficher_texte(WINDOW, WIDTH, HEIGHT, "En attente de votre tour...", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,True,card_positions,dejaUtiliser,carteTour)

def recevoirVictoire(network):
    data = wait_for_server_message(network)
    if data:
        pass



def game_loop(network):
    """Boucle principale du jeu."""
    while True:
        try:
            server_message = wait_for_server_message(network)
            if server_message == "tour":
                card_list, card_positions = setup_cards(network)
                handle_card_click(network, card_list, card_positions)
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")
            break

def faireUnTour(network,card_list,card_positions,Placement,nomPartie,miseTour,scorePartie,dejaUtiliser,carteTour,scoreTour):
    data = wait_for_server_message(network)  # Attend un message du serveur

    if data == "a ton tour":
        Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,'A vous de choisir une carte', getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,Placement,True,card_list,carteTour)
        tmp = handle_card_click(network, card_list, card_positions,nomPartie,miseTour,scorePartie,Placement,dejaUtiliser,scoreTour,carteTour)  # Récupère la carte jouée
        dejaUtiliser = tmp[0]

        carteTour["B"] = tmp[1]
        
        return dejaUtiliser

    elif data == "En attente":
        attendre_tour(card_list,nomPartie,miseTour,scorePartie,Placement,dejaUtiliser,carteTour,scoreTour)
        data = wait_for_server_message(network)
        if data:
            res = data.split(';')
            pos_cart = res[2].split(',')
            id = Placement[int(res[3])]
            carteTour[id] = res[1]
            deplacerCarteOther(WINDOW,WIDTH,HEIGHT,res[1],(int(pos_cart[0]),int(pos_cart[1])),id,True)
            return dejaUtiliser
        

    else:
        print(f"Message inconnu reçu : {data}")


def miseEnPlaceId(id):
    id = decryptId(id)
    print("Connexion au serveur établie.")
    pos = ["G","H","D"]
    tmp = 0
    Placement = {}
    for i in range(int(id),4):
        if i != int(id):
            Placement[i] = pos[tmp]
            tmp += 1

    for i in range(0,int(id)):
        if i != int(id):
            Placement[i] = pos[tmp]
            tmp += 1

    return Placement


def verifMiseTotal(miseJoueur,miseTour,nbCarte):
    cpt = 0
    passage = 0
    for e in miseTour:
        if miseTour[e] != "":
            passage += 1
            cpt += miseTour[e]
    
    if passage == 3:
        if (int(miseJoueur) + cpt) == nbCarte:
            return False
        else:
            return True
    return True

def verifMise(miseJoueur):
    if int(miseJoueur) < 0 or int(miseJoueur) > 5:
        return False
    return True

def mise(network,card_list,nomPartie,miseTour,scorePartie,placement,nbCarte,scoreTour):
    S = ""
    cpt = 0
    while cpt < nombreJoueurs:
        envoyerMise(network,card_list,nomPartie,miseTour,scorePartie,placement,nbCarte,scoreTour)
        data = ""
        while data == "":
            data = wait_for_server_message(network)
            if data:
                tmp = decrypt_mise(data)
                miseTour[tmp[0]] = tmp[1]
                Fonction_a_utiliser.afficher_mise(WINDOW,miseTour,WIDTH,HEIGHT,placement,scoreTour)
                cpt += 1

    return miseTour

def miseDernier(network,card_list,nomPartie,miseTour,scorePartie,placement,scoreTour):
    cpt = 0
    while cpt < nombreJoueurs:
        envoyerMiseDernierTour(network,card_list,nomPartie,miseTour,scorePartie,placement,scoreTour)
        data = ""
        while data == "":
            data = wait_for_server_message(network)
            if data:
                tmp = decrypt_mise(data)
                miseTour[tmp[0]] = tmp[1]
                Fonction_a_utiliser.afficher_mise(WINDOW,miseTour,WIDTH,HEIGHT,placement,scoreTour)
                cpt += 1
    return miseTour


def dernier_tour_client(network, placement,nbJoueur,nomPartie,scorePartie,scoreTour):
    card_list = []
    card_positions = {}
    for i in range(nbJoueur-1):
        data = wait_for_server_message(network)
        if data:
            print("Data = ",data)
            joueur, carte = decryptDerniereCarte(data)
            chemin_carte = getRessource("Demi_Valeur{carte}.jpg")
            #chemin_carte = f"Documents/client/_internal/image/Demi_Valeur{carte}.jpg"
            card_list.append(carte)
            card_positions[carte] = placement[joueur]

    print("Card positions = ",card_positions)
    Fonction_a_utiliser.affichageDerniereCarte(WINDOW, WIDTH, HEIGHT, getRessource("essai.jpg"),card_positions)
    pygame.display.flip()
            
    time.sleep(4)
    miseTour = {0:"",1:"",2:"",3:""}
    miseTour = miseDernier(network,card_positions,nomPartie,miseTour,scorePartie,placement,scoreTour)
    return miseTour

    
def envoyerMiseDernierTour(network,card_list,nomPartie,miseTour,scorePartie,placement,scoreTour):
    print("dkzdzkpdpkozdp",card_list)
    data = wait_for_server_message(network)
    if data == "Choisit ta mise":
        mise = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Mise ?", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,"dernier",card_list)
        
        if verifMise(mise) == False:
            while verifMise(mise) != True:
                 mise = Fonction_a_utiliser.afficher_question(WINDOW, WIDTH, HEIGHT, "Mise incorrect, recommencer", getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,"dernier",card_list)
        
        
        network.send(mise)
        Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente du choix des autres",getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,"dernier",card_list)
        return 
    
    else:
        Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"En attente du choix des autres",getRessource("essai.jpg"),scoreTour,nomPartie,miseTour,scorePartie,placement,"dernier",card_list)
        return 
        

def recevoir_nom(network):
    res = []
    while len(res) != nombreJoueurs:
        data = wait_for_server_message(network)
        if data:
            res.append(data)

    tmp = decrypt_nom(res)
    nomPartie = {}
    for e in tmp:
        nomPartie[e[0]] = e[1]
    
    return nomPartie

def conditionVictoireManche(tabScore,mise,scorePartie):
    joueurPerdant = []
    for i in range(len(tabScore)):
        if tabScore[i] != mise[i]:
            joueurPerdant.append(i)
            diff = abs(tabScore[i]-mise[i])
            scorePartie[i] -= diff

    return scorePartie

def win(dico):
    for e in dico:
        if dico[e] == 0:
            return True


# Fonction principale
def main(addresseServeur):
    network = Network(addresseServeur)
    scoreTour = {0:0,1:0,2:0,3:0}
    time.sleep(5)
    # Initialisation du joueur
    id = initialize_player(network,scoreTour)
    time.sleep(3)
    Placement = miseEnPlaceId(id)
    scorePartie = {0:13,1:13,2:13,3:13}
    miseTour = {0:"",1:"",2:"",3:""}
    
    


    data = None
    while not data == "Debut partie":
        data = wait_for_server_message(network)
    Fonction_a_utiliser.afficher_texte(WINDOW,WIDTH,HEIGHT,"La partie va commencer...",getRessource("essai.jpg"),scoreTour)

    time.sleep(3)
    nomPartie = recevoir_nom(network)


    #DEBUT DE LA PARTIE 
    while True:
        NB_CARTES = 5
        while NB_CARTES > 1:  # Boucle principale
            for i in range(1):
                time.sleep(5)
                dejaUtiliser = []
                scoreTour = {0:0,1:0,2:0,3:0}
                card_list, card_positions = setup_cards(network,scoreTour)  # Configure les cartes initiales
                Fonction_a_utiliser.afficher_nom(WINDOW,nomPartie,WIDTH,HEIGHT,Placement)
                Fonction_a_utiliser.afficher_score(WINDOW,scorePartie,WIDTH,HEIGHT,Placement)
                Fonction_a_utiliser.afficher_mise(WINDOW,miseTour,WIDTH,HEIGHT,Placement,scoreTour)
                pygame.display.flip()
                time.sleep(2)
                miseTour = {0:"",1:"",2:"",3:""}
                scoreTour = {0:0,1:0,2:0,3:0}
                miseTour = mise(network,card_list,nomPartie,miseTour,scorePartie,Placement,NB_CARTES,scoreTour)
                time.sleep(2)

                carteTour = {}
                scoreTour = {0:0,1:0,2:0,3:0}
                for i in range(NB_CARTES):

                    carteTour = {}
                    for j in range(nombreJoueurs):
                        dejaUtiliser = faireUnTour(network,card_list,card_positions,Placement,nomPartie,miseTour,scorePartie,dejaUtiliser,carteTour,scoreTour)
                        T = ""
                        while T != "Fin du Tour":
                            T = wait_for_server_message(network)

                    time.sleep(2)
                    data = wait_for_server_message(network)
                    if data:
                        scoreTour[int(data)] += 1
                    time.sleep(2)

                scorePartie = conditionVictoireManche(scoreTour,miseTour,scorePartie)
                fin = win(scorePartie)
                if fin:
                    time.sleep(200)
                    break

                NB_CARTES -= 1
                time.sleep(2)
        
       
        while NB_CARTES == 1:
            miseTour = {0:0,1:0,2:0,3:0}
            scoreTour = {0:0,1:0,2:0,3:0}
            miseTour = dernier_tour_client(network,Placement,nombreJoueurs,nomPartie,scorePartie,scoreTour)
            time.sleep(2)
            data = ""
            while data == "":
                print(data)
                data = wait_for_server_message(network)
                if data != "":
                    scoreTour[int(data)] = 1
                
            
            time.sleep(2)
            scorePartie = conditionVictoireManche(scoreTour,miseTour,scorePartie)
            print(scorePartie)
            fin = win(scorePartie)
            if fin:
                time.sleep(200)
                break
            NB_CARTES -= 1

            time.sleep(2)
            
            



# Exécution
if __name__ == "__main__":
    """
    b = str(input("Adresse du serveur : "))
    if b:
        main(b)"""
    
    main("192.168.1.56")
