import pygame
from Cartes import valeur_image
import sys
import client
import os




CHEMIN_RESSOURCE = "image"

def getRessource(ressource):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, CHEMIN_RESSOURCE) + "/" + ressource


def carteJoueur(joueurId,hauteur,largeur):
    dico = {  
    "G" : (0+150,(hauteur//2)-80),
    
    "H" : ((largeur//2)-80,140),
    
    "D" : ((largeur//2)+330,hauteur//2-80),

    "B" : ((largeur//2-80),hauteur-270)
         }
    return dico[joueurId]

def affichageDerniereCarte(screen,largeur,hauteur,image_fond,joueurCarte):
    position = {
        "D" : (largeur-190, hauteur//2-80),
        "H" : (largeur//2-80, 50),
        "G" : (50, hauteur//2-80)
    }

    largeur_rect = 70
    hauteur_rect = 110

    for i in joueurCarte:
        joueurId = joueurCarte[int(i)]
        #carte_image = "Documents/client/_internal/image/Demi_Valeur"+str(i)+".jpg"
        carte_image = getRessource("Demi_Valeur"+str(i)+".jpg")
        #print(carte_image)


        if joueurId == "G":

            image_carte = pygame.image.load(carte_image)
            image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),-90)
            screen.blit(image_carte,(position["G"][0],position["G"][1]))

        
        if joueurId == "H":

            image_carte = pygame.image.load(carte_image)
            image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),180)
            screen.blit(image_carte,(position["H"][0],position["H"][1]))

        if joueurId == "D":

            image_carte = pygame.image.load(carte_image)
            image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect)),90)
            screen.blit(image_carte,(position["D"][0],position["D"][1]))

    x,y = largeur//2-80, hauteur-190
    image_carte = pygame.image.load(getRessource("Demi_Valeur23.jpg"))
    image_carte = pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect))
    screen.blit(image_carte,(x,y))
    return None




def affichage_carte(screen,largeur,hauteur,cartes,image_fond,dejaUtiliser=[],carteDuTour={}):
    position = [
        (largeur//2-80, hauteur-190),
        ((largeur//2)-120-80, hauteur-190),
        ((largeur//2)+120-80, hauteur-190),
        ((largeur//2)+120*2-80, hauteur-190),
        (((largeur//2)-120*2)-80, hauteur-190), 
    ]

    position2 = [
        (largeur-190, hauteur//2-80),
        (50, hauteur//2-80),
        
        (largeur-190, (hauteur//2)-90-80),
        (50,(hauteur//2)-90-80),

        (largeur-190, (hauteur//2)+90-80),
        (50,(hauteur//2)+90-80),

        (largeur-190, (hauteur//2)+90*2-80),
        (50,(hauteur//2)+90*2-80),

        (largeur-190, (hauteur//2)-90*2-80),
        (50,(hauteur//2)-90*2-80),
    ]

    position3 = [
        (largeur//2-80, 50),
        ((largeur//2)-120-80, 50),
        ((largeur//2)+120-80, 50),
        ((largeur//2)+120*2-80, 50),
        (((largeur//2)-120*2)-80, 50), 

    ]

    largeur_rect = 100
    hauteur_rect = 140

    largeur_rect2 = 70
    hauteur_rect2 = 110
    res = {}
    for i in range(len(cartes)):

        if cartes[i] in dejaUtiliser:
            x, y = position[i][0], position[i][1]
            image_carte = pygame.image.load(getRessource("Demi_Valeur23.jpg"))
            image_carte = pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect))
            res[(x,y)] = valeur_image(str((cartes[i])))
            screen.blit(image_carte,(x,y))

        else:
            x, y = position[i][0], position[i][1]
            image_carte = pygame.image.load(valeur_image(str(cartes[i])))
            image_carte = pygame.transform.scale(image_carte, (largeur_rect,hauteur_rect))
            res[(x,y)] = valeur_image(str((cartes[i])))
            screen.blit(image_carte,(x,y))


    for j in range(len(cartes)*2):
        x, y = position2[j][0], position2[j][1]
        image_carte = pygame.image.load(getRessource("Demi_Valeur23.jpg"))
        image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect2,hauteur_rect2)),90)

        screen.blit(image_carte,(x,y))

    for k in range(len(cartes)):
        x, y = position3[k][0], position3[k][1]
        image_carte = pygame.image.load(getRessource("Demi_Valeur23.jpg"))
        image_carte = pygame.transform.rotate(pygame.transform.scale(image_carte, (largeur_rect2,hauteur_rect2)),180)

        screen.blit(image_carte,(x,y))

    if carteDuTour != {}:
        for e in carteDuTour:
            client.afficher_cartes_tour(screen,largeur,hauteur,carteDuTour)
            #client.deplacerCarteOther(screen,hauteur,largeur,carteDuTour[e][0],(carteDuTour[e][1][0],carteDuTour[e][1][1]),e,True)

    return res

def clic_carte(screen, largeur, hauteur, image_fond, liste_messages, dico_cartes,dejaUtiliser,placement,scorePartie,miseTour,nomPartie,scoreTour,carteTour):
    """
    Détecte le clic sur une carte et retourne sa valeur et sa position.

    Args:
        screen: Surface Pygame où dessiner.
        largeur: Largeur de l'écran.
        hauteur: Hauteur de l'écran.
        image_fond: Chemin vers l'image de fond.
        liste_messages: Liste des valeurs des cartes affichées.
        dico_cartes: Dictionnaire associant des positions (x, y) à des valeurs de cartes.

    Returns:
        tuple: (valeur de la carte cliquée, (x, y) position) ou None si aucune carte n'est cliquée.
    """
    # Liste des positions des cartes
    position = [
        (largeur//2-80, hauteur-140),
        ((largeur//2)-120-80, hauteur-140),
        ((largeur//2)+120-80, hauteur-140),
        ((largeur//2)+120*2-80, hauteur-140),
        (((largeur//2)-120*2)-80, hauteur-140), 

        (largeur-140, hauteur//2-80),
        (0, hauteur//2-80),
        
        (largeur-140, (hauteur//2)-90-80),
        (0,(hauteur//2)-90-80),

        (largeur-140, (hauteur//2)+90-80),

        (largeur-140, (hauteur//2)+90*2-80),
        (0,(hauteur//2)+90*2-80),

        (largeur-140, (hauteur//2)-90*2-80),
        (0,(hauteur//2)-90*2-80),

        (largeur//2-80, 0),
        ((largeur//2)-120-80, 0),
        ((largeur//2)+120-80, 0),
        ((largeur//2)+120*2-80, 0),
        (((largeur//2)-120*2)-80, 0), 
    ]

    print("dico carte = ",dico_cartes)
    # Dimensions des cartes
    largeur_carte = 100
    hauteur_carte = 140

    # Charger et redimensionner l'image de fond
    image_fond = pygame.image.load(image_fond)
    image_fond = pygame.transform.scale(image_fond, (largeur, hauteur))


    affichage_carte(screen,largeur,hauteur,liste_messages,getRessource("essai.jpg"),dejaUtiliser)
    pygame.display.flip()
    # Couleur pour les retours visuels
    couleur_surbrillance = (255, 0, 0)  # Rouge

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Détecter un clic de souris
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                mouse_x, mouse_y = event.pos
                print(mouse_x,mouse_y)

                # Vérifier si le clic est sur une carte
                for (x, y), valeur_carte in dico_cartes.items():
                    if x <= mouse_x <= x + largeur_carte and y <= mouse_y <= y + hauteur_carte:
                        # Retourner la valeur et la position de la carte cliquée
                        print(f"Carte cliquée : {valeur_carte} en position {(x, y)}")
                        return (valeur_carte,(x,y))

        # Afficher l'image de fond
        screen.blit(image_fond, (0, 0))

        

        affichage_carte(screen,largeur,hauteur,liste_messages,getRessource("essai.jpg"),dejaUtiliser)
        afficher_nom(screen,nomPartie,largeur,hauteur,placement)
        afficher_mise(screen,miseTour,largeur,hauteur,placement,scoreTour)
        afficher_score(screen,scorePartie,largeur,hauteur,placement)
        client.afficher_cartes_tour(screen,largeur,hauteur,carteTour)

        pygame.display.flip()





def jouer_carte(screen,largeur,hauteur,image,pos,image_fond,liste_messages,dejaUtiliser):
    #importation du fond d'écran
    image_fond = pygame.image.load(image_fond)
    image_r = pygame.transform.scale(image_fond, (largeur,hauteur))

    lar_carte = 100 
    hau_cartes = 140

    x, y = pos[0], pos[1]
    image_carte = pygame.image.load(image)
    image_carte = pygame.transform.scale(image_carte, (lar_carte,hau_cartes))


    screen.blit(image_r, (0, 0))
    affichage_carte(screen,largeur,hauteur,liste_messages,dejaUtiliser)

    screen.blit(image_carte,(x,y-200))

    pygame.display.flip()



def centrer_texte(screen, texte, police, x, y, largeur_rect, hauteur_rect):
    """
    Centre le texte dans un rectangle donné et l'affiche sur la surface.
    """
    texte_surface = police.render(texte, True, (0, 0, 0))
    largeur_texte, hauteur_texte = texte_surface.get_size()
    
    # Calculer la position pour centrer le texte
    x_texte = x + (largeur_rect - largeur_texte) // 2
    y_texte = y + (hauteur_rect - hauteur_texte) // 2
    
    screen.blit(texte_surface, (x_texte, y_texte))


def centrage(taille_ecran,taille_box=0):
    """
    Cette fonction permet de centrer des box.
    
    Paramètre :
        -taille_ecran(int): largeur ou hauteur de l'ecran en pixel
        -taille_box(int): largeur ou hauteur de la box en pixel
        
    Return :
        -renvoie la position centré de la box
    """
    return taille_ecran//2-taille_box//2





def afficher_question(screen,largeur,hauteur,question,image_fond,scoreTour,nomPartie = None,miseTour= None,scorePartie= None,placement= None,afficher=False,cartes=[],dejaUtiliser=[]):
    #importation du fond d'écran
    image_fond = pygame.image.load(image_fond)
    image_r = pygame.transform.scale(image_fond, (largeur,hauteur))
    
    couleur_rect = (255, 255, 255)    
    
    # Définir les dimensions et la position du rectangle   
    largeur_rect, hauteur_rect = largeur//2.5, hauteur//3  # Dimensions du rectangle
    x, y = centrage(largeur,largeur_rect), centrage(hauteur,hauteur_rect)  # Position (haut-gauche) du rectangle
    
    BLACK = (0, 0, 0)
    
    police = pygame.font.SysFont("Arial", 36)
    
       
    
    # Variables pour la saisie
    input_box = pygame.Rect(centrage(largeur,300), centrage(hauteur,50)+50, 300, 50)
    text = ''
    

    # Boucle principale
    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if len(text)<20 or event.key == pygame.K_BACKSPACE:
                    
            
                    if event.key == pygame.K_RETURN:
                        return text
                        
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        
                    else:
                        text += event.unicode
        
        #affichage de l'image                                    
        screen.blit(image_r, (0, 0))
        
        #affichage du rectangle
        pygame.draw.rect(screen, couleur_rect, (x, y, largeur_rect, hauteur_rect), border_radius=30)

        #Affichage de la case input        
        txt_surface = police.render(text, True, BLACK)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        pygame.draw.rect(screen, BLACK, input_box, 2)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        
        #affichage de la question
        texte = police.render(question, True, (255, 0, 0))
        largeur_texte, hauteur_texte = texte.get_size()
        x_texte = x + (largeur_rect - largeur_texte) // 2
        
        screen.blit(texte,(x_texte, centrage(hauteur,50)-50))

        if afficher == True:
            affichage_carte(screen,largeur,hauteur,cartes,image_fond,dejaUtiliser)

        if afficher == "dernier":
            affichageDerniereCarte(screen,largeur,hauteur,image_fond,cartes)

        if nomPartie != None:
            afficher_nom(screen,nomPartie,largeur,hauteur,placement)
            afficher_mise(screen,miseTour,largeur,hauteur,placement,scoreTour)
            afficher_score(screen,scorePartie,largeur,hauteur,placement)
 
        



            
       


        pygame.display.flip()



def afficher_texte(screen,largeur,hauteur,texte,image_fond,scoreTour,nomPartie = None,miseTour= None,scorePartie= None,placement= None,afficher=False,cartes=[],dejaUtiliser = [],afficherCareDuTour={}):
    image_fond = pygame.image.load(image_fond)
    image_r = pygame.transform.scale(image_fond, (largeur,hauteur))
    
    couleur_rect = (255, 255, 255)    
    
    # Définir les dimensions et la position du rectangle   
    largeur_rect, hauteur_rect = largeur//3, hauteur//6  # Dimensions du rectangle
    x, y = centrage(largeur,largeur_rect), centrage(hauteur,hauteur_rect)  # Position (haut-gauche) du rectangle
    
      # Boucle principale
    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                """
                if event.key == pygame.K_RETURN:
                    return False"""
                    
        
        #affichage de l'image                                    
        screen.blit(image_r, (0, 0))

        #affichage du rectangle
        pygame.draw.rect(screen, couleur_rect, (x, y, largeur_rect, hauteur_rect),border_radius=30)
        
        #affichage du texte
        police = pygame.font.SysFont("Arial", 36)
        centrer_texte(screen, texte, police, x, y-10, largeur_rect, hauteur_rect)

        
        #affichage carte
        if afficher == True:
            affichage_carte(screen,largeur,hauteur,cartes,getRessource("essai.jpg"),dejaUtiliser)

        if afficherCareDuTour != {}:
             affichage_carte(screen,largeur,hauteur,cartes,getRessource("essai.jpg"),dejaUtiliser,afficherCareDuTour)
        
        if afficher == "dernier":
            affichageDerniereCarte(screen,largeur,hauteur,image_fond,cartes)


        if nomPartie != None:
            afficher_nom(screen,nomPartie,largeur,hauteur,placement)
            afficher_mise(screen,miseTour,largeur,hauteur,placement,scoreTour)
            afficher_score(screen,scorePartie,largeur,hauteur,placement)

        pygame.display.flip()
        return False
    
def afficher_texte_pos(fenetre,x, y, texte,rot = False,oppose = False,couleur = False):
    if not couleur:
        BLANC = (255, 255, 255)
        NOIR = (0, 0, 0)
        police = pygame.font.Font(None, 36)
    if couleur:
        BLANC = (192, 192, 192)
        NOIR = (0, 0, 0)
        police = pygame.font.Font(None, 36)

    if not rot:
        # Création du texte
        surface_texte = police.render(texte, True, NOIR)
        
        # Taille du texte
        largeur_texte = surface_texte.get_width()
        hauteur_texte = surface_texte.get_height()
        
        # Dimensions du cadre blanc
        marge = 10
        largeur_cadre = largeur_texte + 2 * marge
        hauteur_cadre = hauteur_texte + 2 * marge
        
        # Dessiner un cadre blanc
        pygame.draw.rect(fenetre, BLANC, (x - marge, y - marge, largeur_cadre, hauteur_cadre))
        
        # Afficher le texte sur la fenêtre
        fenetre.blit(surface_texte, (x, y))

    else:        
        # Créer la surface du texte
        surface_texte = police.render(texte, True, NOIR)
        
        # Obtenir les dimensions du texte
        largeur_texte = surface_texte.get_width()
        hauteur_texte = surface_texte.get_height()
        
        # Définir la marge autour du texte
        marge = 10
        
        # Calculer les dimensions du cadre blanc
        largeur_cadre = largeur_texte + 2 * marge
        hauteur_cadre = hauteur_texte + 2 * marge
        
        # Créer une surface pour le cadre blanc avec un canal alpha (transparence)
        surface_cadre = pygame.Surface((largeur_cadre, hauteur_cadre), pygame.SRCALPHA)
        
        # Remplir la surface du cadre avec la couleur blanche
        surface_cadre.fill(BLANC)
        
        # Blitter le texte sur la surface du cadre, centré
        surface_cadre.blit(surface_texte, (marge, marge))
        
        # Faire pivoter la surface du cadre de 90 degrés
        if not oppose:
            surface_cadre = pygame.transform.rotate(surface_cadre, 90)
        else:
            surface_cadre = pygame.transform.rotate(surface_cadre, -90)
        
        # Obtenir les nouvelles dimensions après rotation
        largeur_cadre, hauteur_cadre = surface_cadre.get_size()
        
        # Calculer la nouvelle position pour centrer la surface pivotée
        position_x = x - largeur_cadre // 2
        position_y = y - hauteur_cadre // 2
        
        # Blitter la surface pivotée sur la fenêtre
        fenetre.blit(surface_cadre, (position_x, position_y))



    
def afficher_score(screen,scorePartie,largeur,hauteur,placement):
    position = [
        ((largeur)//+150,hauteur-170),
        (largeur-170,40),
       ((largeur//2)-480,35),
       ((largeur)//2+295,hauteur-80)
    ]

    largeur_rect = 80
    hauteur_rect = 110


    for e in scorePartie:
        if e in placement:
            if placement[e] == "G":
                x, y = position[0][0], position[0][1]
                afficher_texte_pos(screen,x,y,"score = "+str(scorePartie[e]),False,False,True)
                pygame.display.flip()

            if placement[e] == "H":
                x, y = position[2][0], position[2][1]
                afficher_texte_pos(screen,x,y,"score = "+str(scorePartie[e]),False,False,True)
                pygame.display.flip()

            if placement[e] == "D":
                x, y = position[1][0], position[1][1]
                afficher_texte_pos(screen,x,y,"score = "+str(scorePartie[e]),False,False,True)
                pygame.display.flip()

        else:
            x, y = position[3][0], position[3][1]
            afficher_texte_pos(screen,x,y,"score = "+str(scorePartie[e]),False,False,True)
            pygame.display.flip()

def afficher_nom(screen,nomPartie,largeur,hauteur,placement):
    position = [
        (27,hauteur//2),
        (largeur-35,hauteur//2-30),
       (largeur//2-40,7),
       ((largeur)//2-35,hauteur-35)
    ]
    
    for e in nomPartie:
        if e in placement:
            if placement[e] == "G":
                x, y = position[0][0], position[0][1]
                afficher_texte_pos(screen,x,y,nomPartie[e],True,False)
                pygame.display.flip()

            if placement[e] == "H":
                x, y = position[2][0], position[2][1]
                afficher_texte_pos(screen,x,y,nomPartie[e])
                pygame.display.flip()

            if placement[e] == "D":
                x, y = position[1][0], position[1][1]
                afficher_texte_pos(screen,x,y,nomPartie[e],True,True)
                pygame.display.flip()

        else:
            x, y = position[3][0], position[3][1]
            afficher_texte_pos(screen,x,y,nomPartie[int(e)])
            pygame.display.flip()
        

def afficher_mise(screen,miseTour,largeur,hauteur,placement,scoreTour):
    WHITE = (102, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, 36)

    position = [
        (190,hauteur//2+65),
        (largeur-225,hauteur//2-150),
       (largeur//2-180,190),
       ((largeur)//2+290,hauteur-150)
    ]

    for e in miseTour:
        if e in placement:
            if placement[e] == "G":
                x, y = position[0][0], position[0][1]
                pygame.draw.circle(screen, WHITE, (x, y), 20)

                # Rendre le texte
                text_surface = font.render(str(scoreTour[e])+"/"+str(miseTour[e]), True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y))

                # Dessiner le texte
                screen.blit(text_surface, text_rect)
                pygame.display.flip()

            if placement[e] == "H":
                x, y = position[2][0], position[2][1]
                pygame.draw.circle(screen, WHITE, (x, y), 20)

                # Rendre le texte
                text_surface = font.render(str(scoreTour[e])+"/"+str(miseTour[e]), True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y))

                # Dessiner le texte
                screen.blit(text_surface, text_rect)
                pygame.display.flip()

            if placement[e] == "D":
                x, y = position[1][0], position[1][1]
                pygame.draw.circle(screen, WHITE, (x, y), 20)

                # Rendre le texte
                text_surface = font.render(str(scoreTour[e])+"/"+str(miseTour[e]), True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y))

                # Dessiner le texte
                screen.blit(text_surface, text_rect)
                pygame.display.flip()

        else:
            x, y = position[3][0], position[3][1]
            pygame.draw.circle(screen, WHITE, (x, y), 20)

            # Rendre le texte
            text_surface = font.render(str(scoreTour[e])+"/"+str(miseTour[e]), True, BLACK)
            text_rect = text_surface.get_rect(center=(x, y))

            # Dessiner le texte
            screen.blit(text_surface, text_rect)
            pygame.display.flip()




