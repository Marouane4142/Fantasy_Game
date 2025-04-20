# RPG Game Marouane ARNAUD EL MAGHNOUJI, Jad BOUDISSA
import subprocess
import sys

# Liste des bibliothèques requises
required_packages = ["pygame", "pyscroll", "pytmx","Image"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} non installé. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import pygame
import os
import sqlite3
from jeu import Jeu
from pygame import mixer

# Initialisation de Pygame
pygame.init()
mixer.init()

# Définition de la taille de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fantasy Game")

# Définition des polices
font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "menu graphics\THE LAST KINGDOM.ttf"), 28)
commande = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\commande.png'))
commande2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\commande2.png'))

# Définition des options du menu
options = ["Nouvelle partie", "Charger partie", "Quitter"]
selected_option = 0

# Musique du menu
title_theme = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi_-_Title_Theme_Loop.wav')

""" Méthode qui relève l'élément voulu de la sauvegarde stocké dans un fichier sql """

def releve_sql(element,id):
    save = sqlite3.connect(os.path.join(os.path.dirname(__file__), ("save/save.db")))
    save.row_factory = sqlite3.Row
    curseur = save.cursor()
    curseur.execute(" SELECT {} FROM Sauvegarde WHERE id = {}".format(element,id))
    retour = curseur.fetchone()
    curseur.close()
    save.row_factory = None
    save.close()
    return retour[0]

# Activation de la boucle
running = True
# Activation musique du menu
mixer.music.load(title_theme)
pygame.mixer.music.set_volume(0.8)
mixer.music.play(-1)
# Relancement par defaut faux
actif = False

# Attente en cas de spam du joueur
wait1 = 0

# Chargement des sons
pause = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/unpause.wav'))
no = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/no.wav'))

# Boucle principale du menu
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Parcours option (clavier)
        elif event.type == pygame.KEYDOWN:
            # Parcourir vers le haut
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options)
            # Parcourir vers le bas
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            # Quitter le jeu
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.Sound.play(pause).set_volume(0.5)
                mixer.music.stop()
                running = False
            # Retour du choix
            elif event.key == pygame.K_RETURN:
                # Lancer une nouvelle partie
                if selected_option == 0:
                    pygame.mixer.Sound.play(pause).set_volume(0.5)
                    mixer.music.stop()
                    jeu = Jeu(selected_option)
                    screen.blit(commande,(0,0))
                    pygame.display.flip()
                    pygame.time.wait(8000)
                    screen.blit(commande2,(0,0))
                    pygame.display.flip()
                    pygame.time.wait(8000)
                    jeu.run()
                    actif = True
                    mixer.music.load(title_theme)
                    pygame.mixer.music.set_volume(0.8)
                    mixer.music.play(-1)
                # Charger une partie
                elif selected_option == 1 and wait1 == 0:
                    # Cas ou il n'y a pas de sauvegarde
                    if releve_sql("Niveau",1) == 0:
                        wait1 += 1
                        pygame.mixer.Sound.play(no).set_volume(0.5)
                    else:
                        pygame.mixer.Sound.play(pause).set_volume(0.5)
                        mixer.music.stop()
                        jeu = Jeu(selected_option)
                        jeu.run()
                        actif = True
                        mixer.music.load(title_theme)
                        pygame.mixer.music.set_volume(0.8)
                        mixer.music.play(-1)
                # Quitter le jeu 
                elif selected_option == 2:
                    pygame.mixer.Sound.play(pause).set_volume(0.5)
                    mixer.music.stop()
                    quit()

        # Parcours option (souris)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Récupérer la position de la souris
            pos = pygame.mouse.get_pos()
            # Vérifier si l'utilisateur a cliqué sur une option
            for i, option in enumerate(options):
                text = font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(800/2, 600/2 + i*80))
                # Retour du choix
                if text_rect.collidepoint(pos):
                    selected_option = i
                    # Lancer une nouvelle partie
                    if selected_option == 0:
                        pygame.mixer.Sound.play(pause).set_volume(0.5)
                        mixer.music.stop()
                        jeu = Jeu(0)
                        screen.blit(commande,(0,0))
                        pygame.display.flip()
                        pygame.time.wait(8000)
                        screen.blit(commande2,(0,0))
                        pygame.display.flip()
                        pygame.time.wait(8000)
                        jeu.run()
                        actif = True
                        mixer.music.load(title_theme)
                        pygame.mixer.music.set_volume(0.8)
                        mixer.music.play(-1)
                    # Charger une partie
                    elif selected_option == 1 and wait1 == 0:
                        # Cas ou il n'y a pas de sauvegarde
                        if releve_sql("Niveau",1) == 0:
                            wait1 += 1
                            pygame.mixer.Sound.play(no).set_volume(0.5)
                        else:
                            pygame.mixer.Sound.play(pause).set_volume(0.5)
                            mixer.music.stop()
                            jeu = Jeu(selected_option)
                            jeu.run()
                            actif = True
                            mixer.music.load(title_theme)
                            pygame.mixer.music.set_volume(0.8)
                            mixer.music.play(-1)
                    # Quitter le jeu
                    elif selected_option == 2:
                        pygame.mixer.Sound.play(pause).set_volume(0.5)
                        mixer.music.stop()
                        quit()

    # Condition de redémarrage automatique à la dernière sauvegarde en cas de game over
    if actif:
        if jeu.relance:
            mixer.music.stop()
            jeu = Jeu(1)
            jeu.run()
            mixer.music.load(title_theme)
            pygame.mixer.music.set_volume(0.8)
            mixer.music.play(-1)

    # Cooldown pour éviter un crash par spam
    if wait1 > 0:
        wait1 += 1
        if wait1 > 150:
            wait1 = 0


    # Selection du fond principal
    drawn_background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\menu_background.png'))
    # Upscale de l'image pour adaptation a la fenêtre
    drawn_background = pygame.transform.scale(drawn_background,(800,600))
    # Affichage du fond principal
    screen.blit(drawn_background,(0,0))
    # Affichage des options réparties sur l'écran en vertical
    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        text_rect = text.get_rect(center=(800/2, 600/2 + i*80))
        if i == selected_option:
            selection_color = pygame.Color("#7A8CCD")
            pygame.draw.rect(screen, selection_color, text_rect.inflate(20, 20))
        screen.blit(text, text_rect)
    # Mise à jour de l'écran (Actualisé)
    pygame.display.flip()

# Stop de la musique
mixer.music.stop()
