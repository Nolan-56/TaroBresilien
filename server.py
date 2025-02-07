import socket
import random
import threading
import sys
import pygame
import time 
import re

# Configuration du serveur
SERVER = "0.0.0.0"
PORT = 5555

# Création du socket serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER, PORT))
except socket.error as e:
    print(f"Erreur lors de la liaison du socket : {e}")
    sys.exit()

s.listen(4)
print("Serveur démarré, en attente de connexions...")

# Variables globales
player_cards = {}
Vue = []
Joueurs = []
player_id = 0
#NB_CARTES_PAR_JOUEUR = 5

# Classe Joueur
class Joueur:
    def __init__(self, id, conn=None, nom=""):
        self.id = id
        self.nom = nom
        self.score = 20
        self.firstPlayer = False
        self.conn = conn

    def set_score(self, val):
        self.score -= val

    def get_id(self):
        return self.id

    def get_nom(self):
        return self.nom

# Fonctions Utilitaires
def envoyer_message(conn, message):
    """Envoie un message à un joueur spécifique."""
    try:
        conn.sendall(message.encode("utf-8"))
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

def broadcast(message):
    """Envoie un message à tous les joueurs connectés."""
    global Joueurs
    for joueur in Joueurs:
        if joueur.conn:
            envoyer_message(joueur.conn, message)

def broadcast_1(conn,message):
    global Joueurs
    for joueur in Joueurs:
        if joueur.conn != conn:
            envoyer_message(joueur.conn,message)


def recevoir_message(conn):
    """Reçoit un message d'un joueur."""
    try:
        data = conn.recv(2048).decode("utf-8")
        if data:
            return data
    except Exception as e:
        print(f"Erreur lors de la réception du message : {e}")
    return None

# Initialisation des Joueurs
def init_joueur(conn, id_joueur):
    """Initialise un joueur en lui demandant son nom."""
    global Joueurs
    try:
        envoyer_message(conn, "Salut à toi ! Quelle est ton nom ? ")
        nom = recevoir_message(conn)
        if nom:
            joueur = Joueur(id_joueur, conn=conn, nom=nom)
            Joueurs.append(joueur)
            print(f"Joueur {joueur.nom} (ID: {joueur.id}) connecté.")
            envoyer_message(conn,str(player_id))
            return joueur
    except Exception as e:
        print(f"Erreur lors de l'initialisation du joueur {id_joueur} : {e}")
    return None

# Gestion des cartes
def distribuer_cartes(joueur, nb_cartes,envoyer=True):
    """Distribue des cartes à un joueur."""
    global Vue, player_cards
    cartes = []
    for _ in range(nb_cartes):
        carte = random.randint(1, 22)
        while carte in Vue:
            carte = random.randint(1, 22)
        cartes.append(carte)
        Vue.append(carte)
    player_cards[joueur.id] = cartes
    if envoyer:
        envoyer_message(joueur.conn, f"Vos cartes : {cartes}")
    else:
        broadcast_1(joueur.conn, "["+str(joueur.id)+","+str(cartes)+"]")
        return cartes
    print(f"Cartes distribuées à {joueur.nom} : {cartes}")

# Gestion du client
def threaded_client(joueur, nb_cartes):
    """Gère les interactions avec un joueur."""
    try:
        distribuer_cartes(joueur, nb_cartes)
        while True:
            data = recevoir_message(joueur.conn)
            if not data:
                print(f"{joueur.nom} (ID: {joueur.id}) s'est déconnecté.")
                break
            print(f"{joueur.nom} : {data}")
            if "Carte jouée :" in data:
                carte_jouee = data.split(": ")[1]
                print(f"{joueur.nom} a joué : {carte_jouee}")
                broadcast(f"{joueur.nom} a joué : {carte_jouee}")
    except Exception as e:
        print(f"Erreur avec le joueur {joueur.id} : {e}")
    finally:
        nettoyer_joueur(joueur)

def nettoyer_joueur(joueur):
    """Nettoie les données du joueur lorsqu'il se déconnecte."""
    global player_cards
    if joueur.id in player_cards:
        del player_cards[joueur.id]
    if joueur in Joueurs:
        Joueurs.remove(joueur)
    if joueur.conn:
        joueur.conn.close()
    print(f"Connexion avec {joueur.nom} (ID: {joueur.id}) terminée.")

def win(dico):
    for e in dico:
        if dico[e] == 0:
            print(str(e.nom) + "A perdu")
            return True

def miseEnPlaceOrdre(dico):
    ordreTour = []
    for i in range(len(dico)):
        if dico[i].firstPlayer == True:
            ordreTour.append(dico[i])
            tmp = i

    for j in range(tmp+1,len(dico)):
        ordreTour.append(dico[j])

    for k in range(0,tmp):
        ordreTour.append(dico[k])

    return ordreTour

def decrypt_card_value(card_path):
    """Extrait la valeur de la carte à partir de son chemin d'image."""
    pattern = r"Demi_Valeur(\d+)\.jpg"
    match = re.search(pattern, card_path)
    if match:
        return int(match.group(1))
    return None

def conditionVictoireTour(score,tabScore):
    maxi = 0
    joueur = None
    for e in score:
        if e[0] > maxi:
            maxi = e[0]
            joueur = e[1]

    tabScore[joueur] += 1
    print("TabsScore ", tabScore)

    
    return(maxi,joueur)

def conditionVictoireManche(tabScore,mise,scorePartie):
    joueurPerdant = []
    for i in range(len(tabScore)):
        if tabScore[i] != mise[i]:
            joueurPerdant.append(i)
            diff = abs(tabScore[i]-mise[i])
            scorePartie[i] -= diff

    return scorePartie

def mise(ordreJoueurTour,miseTour):
    for joueur_actuel in ordreJoueurTour:
        envoyer_message(joueur_actuel.conn, "Choisit ta mise")  # Signale au joueur actuel de jouer
        broadcast_1(joueur_actuel.conn, "En attente de la mise")  # Les autres joueurs attendent
        mise = recevoir_message(joueur_actuel.conn)
        if mise:
            print("MISE :" + str(mise))
            miseTour[joueur_actuel.id] = int(mise)
            time.sleep(2)
            broadcast("("+str(joueur_actuel.id)+","+str(mise)+")")
            time.sleep(2)
    

    return miseTour

def faireUnTour(NB_CARTES_PAR_JOUEUR,ordreJoueurTour,scoreTour):
    for i in range(NB_CARTES_PAR_JOUEUR):
        time.sleep(2)
        cartePose = []
        res = []
        carte_jouee = ""
        for joueur_actuel in ordreJoueurTour:  # Parcourt chaque joueur dans l'ordre
            envoyer_message(joueur_actuel.conn, "a ton tour")  # Signale au joueur actuel de jouer
            broadcast_1(joueur_actuel.conn, "En attente")  # Les autres joueurs attendent

            carte_jouee = recevoir_message(joueur_actuel.conn)
            print("zzzzzzz",carte_jouee)
            if carte_jouee:
                res = carte_jouee.split(';')
                print(res)
            cartePose.append((decrypt_card_value(res[1]),joueur_actuel.id))
            print(cartePose)
            carte_jouee = str(carte_jouee) + ";" + str(joueur_actuel.id)
            broadcast_1(joueur_actuel.conn,carte_jouee)
            time.sleep(3)

            broadcast("Fin du Tour")  # Informe tous les joueurs que le tour est terminé
        gagnant = conditionVictoireTour(cartePose,scoreTour)
        print(gagnant)
        time.sleep(2)
        broadcast(str(gagnant[1]))
        time.sleep(2)
        return scoreTour
    
def maxiDernierTour(cartePartie):
    maxi = 0
    joueur = None
    for e in cartePartie:
        if cartePartie[e][0] > maxi:
            maxi = cartePartie[e][0]
            joueur = e 
    return (joueur,maxi)

def dernierTour(ordreJoueurTour,Joueurs,scorePartie):
    scoreTour = {0:0,1:0,2:0,3:0}
    cartePartie = {}
    for joueur in Joueurs:
        b = distribuer_cartes(joueur,1,False)
        cartePartie[joueur.id] = b
        time.sleep(2)

    time.sleep(4)
    miseTour = {0:0,1:0,2:0,3:0}
    miseTour = mise(ordreJoueurTour,miseTour)

    res = maxiDernierTour(cartePartie)
    scoreTour[res[0]] = 1
    time.sleep(2)
    broadcast(str(res[0]))
    time.sleep(2)
    print("llllll",scoreTour)
    scorePartie = conditionVictoireManche(scoreTour,miseTour,scorePartie)
    return scorePartie
        
def finPartie(scorePartie):
    for e in scorePartie:
        if scorePartie[e] == 0:
            print(e,"a perdu !!!!")

    
def envoyer_nom(dicoJoueur):
    for e in dicoJoueur:
        res = ""
        res = "(" + str(e.id) + "," + str(e.nom) + ")"
        broadcast(res)
        time.sleep(1)

    





# Démarrage du serveur
def start_server():
    global player_id
    nbJoueurs = 4
    init = True
    while init:
        conn, addr = s.accept()
        print(f"Connexion reçue de {addr}")
        joueur = init_joueur(conn, player_id)
        if joueur:
            broadcast(f"Joueur {joueur.nom} a rejoint la partie.")
            broadcast("\n")
            envoyer_message(conn,str(player_id))
            if player_id == 0:
                Joueurs[0].firstPlayer = True
            
            player_id += 1
            print(Joueurs)
        
        if player_id == nbJoueurs:

            time.sleep(5)
            broadcast("Debut partie")
            print("aaaaaa")
            init = False
    
    time.sleep(4)
    envoyer_nom(Joueurs)    
    print(Joueurs)
    #DEBUT DE LA PARTIE
    print("zzzzzzzzzzzzzzzzzz")
    scorePartie = {0:13,1:13,2:13,3:13}
    time.sleep(2)

    while True:
        print("nnnnnnnnnnnnnnnnnnnnnnnnnn")
        NB_CARTES_PAR_JOUEUR = 5
        miseTour = {0:0,1:0,2:0,3:0}
        ordreJoueurTour = miseEnPlaceOrdre(Joueurs)
        print(ordreJoueurTour)


        while NB_CARTES_PAR_JOUEUR > 1:
            time.sleep(3)
            global Vue
            Vue = []
            for joueur in Joueurs:
                distribuer_cartes(joueur,NB_CARTES_PAR_JOUEUR)
            

            time.sleep(2)
            miseTour = {0:0,1:0,2:0,3:0}
            miseTour = mise(ordreJoueurTour,miseTour)
            print("Mise tour = ",miseTour)
            time.sleep(2)

            
            scoreTour = {0:0,1:0,2:0,3:0}
            for j in range(NB_CARTES_PAR_JOUEUR):
                print("zzzzzz")
                scoreTour = faireUnTour(NB_CARTES_PAR_JOUEUR,ordreJoueurTour,scoreTour)
                print("bbbbbbbbbbbbbbbbbb")
                time.sleep(2)
            
            
                

            scorePartie = conditionVictoireManche(scoreTour,miseTour,scorePartie)
            fin = win(scorePartie)
            if fin:
                time.sleep(200)
                break

            NB_CARTES_PAR_JOUEUR -= 1
            time.sleep(2)

        while NB_CARTES_PAR_JOUEUR == 1:
            scorePartie = dernierTour(ordreJoueurTour,Joueurs,scorePartie)
            print("Score Partie = ",scorePartie)
            fin = win(scorePartie)
            if fin:
                time.sleep(200)
                break
            NB_CARTES_PAR_JOUEUR -= 1
            
        time.sleep(2)

        ordreJoueurTour[0].firstPlayer = False
        ordreJoueurTour[1].firstPlayer = True
        




            

# Lancer le serveur
if __name__ == "__main__":
    start_server()
