import pygame
import pytmx
import pyscroll
import os
import math
import sqlite3
from PIL import Image, ImageFilter 
from pygame import mixer
from projectile import Projectile

pygame.init()
mixer.init()

from boss import Boss
from medaille import Medaille
from monster import Monstre
from joueur import Joueur

class Jeu:

    def __init__(self,save):
        # Choix de sauvegarde
        self.saveid = save
        # Fenêtre du jeu
        self.screen = pygame.display.set_mode((800,600))
        # Direction du joueur
        self.direction = self.releve_sql("Direction")
        # Phase du monstre
        self.phase = 'pause'
        # Image pour le HUD affichage des pierres obtenue
        self.image_med = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\medaille.png')).convert_alpha()
        # Activation mini map
        self.minimap = False
        self.map = False
        # Récupération des images de la map
        minimap_img = pygame.image.load(os.path.join(os.path.dirname(__file__),'TSX/Sprites/world_map_image_blank.png')).convert_alpha()
        map_img = pygame.image.load(os.path.join(os.path.dirname(__file__),'TSX/Sprites/world_map_image_full.png')).convert_alpha()
        # Upscale des images
        self.map_img = pygame.transform.scale(map_img,(528,397))
        self.minimap_img = pygame.transform.scale(minimap_img,(170,125))

        # Chargement de la carte en tmx
        self.world = self.releve_sql("Monde")

        # Si dans le monde normal
        if self.world == "world":

            # Chargement de la map monde
            self.tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), 'worldmap.tmx'))

            # Définir une liste stockant tous les rectangles de collisions des murs
            self.walls = []
            for obj in self.tmx_data.objects:
                if obj.type == "collision":
                    self.walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir une liste stockant tous les rectangles de collisions des piques
            self.spikes = []
            for obj in self.tmx_data.objects:
                if obj.type == "spike":
                    self.spikes.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))


            # Définir une liste stockant tous les rectangles de collisions de la cave
            self.cave = []
            for obj in self.tmx_data.objects:
                if obj.type == "cave":
                    self.cave.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
    
            # Définir une liste stockant tous les rectangles de collisions de la forêt
            self.forest = []
            for obj in self.tmx_data.objects:
                if obj.type == "forest":
                    self.forest.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir une liste stockant tous les rectangles de collisions du volcan
            self.volcano = []
            for obj in self.tmx_data.objects:
                if obj.type == "volcano":
                    self.volcano.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir une liste stockant tous les rectangles de collisions des îles
            self.islands = []
            for obj in self.tmx_data.objects:
                if obj.type == "thunder":
                    self.islands.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir une liste stockant tous les rectangles de collisions des sauvegardes
            self.savezone = []
            for obj in self.tmx_data.objects:
                if obj.type == "save":
                    self.savezone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir la zone de la pierre rouge
            self.red_zone = []
            for obj in self.tmx_data.objects:
                if obj.type == "red":
                    self.red_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir la zone de la pierre verte
            self.green_zone = []
            for obj in self.tmx_data.objects:
                if obj.type == "green":
                    self.green_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir la zone de la pierre bleu
            self.blue_zone = []
            for obj in self.tmx_data.objects:
                if obj.type == "blue":
                    self.blue_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir la zone de la pierre violet
            self.purple_zone = []
            for obj in self.tmx_data.objects:
                if obj.type == "purple":
                    self.purple_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Localisation de la zone d'entré du château
            enter_castle = self.tmx_data.get_object_by_name('enter_castle')

            # Définition de la zone d'entré du château
            self.enter_castle_rect = pygame.Rect(enter_castle.x,enter_castle.y,enter_castle.width,enter_castle.height)

        # Si dans le château
        else:

            # Chargement de la map château
            self.tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), 'inside_castlemap.tmx'))

            # Définir une liste stockant tous les rectangles de collisions des murs
            self.walls = []
            for obj in self.tmx_data.objects:
                if obj.type == "collision":
                    self.walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            # Définir une liste stockant tous les rectangles de collisions des sauvegardes
            self.savezone = []
            for obj in self.tmx_data.objects:
                if obj.type == "save":
                    self.savezone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
                
            # Localisation de la zone de sortie du château
            exit_castle = self.tmx_data.get_object_by_name('exit_castle')
            # Définition de la zone de sortie du château
            self.exit_castle_rect = pygame.Rect(exit_castle.x,exit_castle.y,exit_castle.width,exit_castle.height)

        # 
        map_data = pyscroll.TiledMapData(self.tmx_data)

        # Création du zoom et de la caméra suivant le joueur
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Génération du joueur en fonction des éléments de sauvegarde
        self.player = Joueur(self.releve_sql("Position_x"),self.releve_sql("Position_y"),self.releve_sql("PV"),self.releve_sql("PVMAX"),self.releve_sql("Attaque"),self.releve_sql("Niveau"),self.releve_sql("EXP"))

        # Dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.monstergroup = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 6)

        # Ajout du joueur au groupe de calque
        self.group.add(self.player)

        # Détecteur dans zone spécifique
        self.in_cave = False
        self.in_forest = False
        self.in_volcano = False
        self.in_floating_islands = False

        # Relève si pierre obtenue ou non dans sauvegarde
        self.red = self.releve_sql("Rouge")
        self.green = self.releve_sql("Vert")
        self.blue = self.releve_sql("Bleu")
        self.purple = self.releve_sql("Violet")

        # Création du stockage des pierres
        self.medaille = []

        # Si pierre non obtenue, alors crée pierre
        if self.red == 0:
            self.rouge = Medaille("red")
            self.group.add(self.rouge)
            self.medaille.append(self.rouge)

        if self.green == 0:
            self.vert = Medaille ("green")
            self.group.add(self.vert)
            self.medaille.append(self.vert)

        if self.purple == 0:
            self.violet = Medaille("purple")
            self.group.add(self.violet)
            self.medaille.append(self.violet)

        if self.blue == 0:
            self.bleu = Medaille("blue")
            self.group.add(self.bleu) 
            self.medaille.append(self.bleu)

        # Mise en pause du jeu
        self.pause = False
        # Maintient la touche espace activé pour avoir un intervalle de temps d'attaque et terminé animation d'attaque
        self.prev_space_pressed = False
        # Mets fin a la boucle pour retouner dans le menu
        self.STOP = False
        # Cycle pour touche echap
        self.cycle1 = 0
        # Cycle d'éxecution 1 fois d'initilisation du game over
        self.cycle2 = 0
        # Le joueur est attaqué
        self.player_attacked = False
        # initialisation du dictionnaire de monstre et leurs précense dans le jeu
        self.liste = {"slime": [],"champi": [],"boss": []}
        # Association des listes de monstres
        self.classe_monstre = self.liste["slime"] + self.liste["champi"] + self.liste["boss"]
        # Liste rassemblant tout les slimes présent
        self.liste_slime = []
        # Liste rassemblant tout les champi présent
        self.liste_champi = []
        # Redéfinition de la sauvegarde par défaut
        self.saveid = 1
        # Game Over
        self.game_over = False
        # Relancer une partie en cas de Game Over
        self.relance = False
        # Compteur qui active la régénération quand le temps indiqué sera passer
        self.timer1 = 0
        # Cooldown d'ajout d'exp
        self.timer2 = 0
        # Temps sans se prendre de dégât pour se régénéré
        self.temps = 3600
        # Cooldown pour ne pas crash pour spam
        self.wait1 = 0
        # Cas ou spawn dans le monde normal ou chateau directement
        self.music1 = 0
        self.get = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/get.wav'))
        self.cycle3 = 0

    """ Méthode qui sauvegarde les infos et variable actuelle du joueur """

    def save(self):
        if self.wait1 == 0:
            self.wait1 += 1  
            save_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/save.wav'))
            save = sqlite3.connect(os.path.join(os.path.dirname(__file__), ("save/save.db")))
            save.row_factory = sqlite3.Row
            curseur = save.cursor()
            curseur.execute("UPDATE Sauvegarde SET Position_x = {},Position_y = {},PV = {},PVMAX = {},Attaque = {},Niveau = {},EXP = {},Direction = '{}',Rouge = '{}',Vert = '{}',Bleu = '{}',Violet = '{}',Monde = '{}' WHERE ID = 1".format(self.player.position[0],self.player.position[1],self.player.pv,self.player.pv_max,self.player.attaque,self.player.niveau,self.player.exp,self.direction,self.red,self.green,self.blue,self.purple,self.world))
            save.commit()
            curseur.close()
            save.row_factory = None
            save.close()
            pygame.mixer.Sound.play(save_sound).set_volume(0.5)

    """ Méthode qui relève les infos de la sauvegarde """

    def releve_sql(self,element):
        save = sqlite3.connect(os.path.join(os.path.dirname(__file__), ("save/save.db")))
        save.row_factory = sqlite3.Row
        curseur = save.cursor()
        curseur.execute(" SELECT {} FROM Sauvegarde WHERE id = {}".format(element,self.saveid))
        retour = curseur.fetchone()
        curseur.close()
        save.row_factory = None
        save.close()
        return retour[0]
    
    """ Méthode qui défnit les spawn des monstres et optimise le programme """

    def spawn_monstre(self):


        if self.world == "castle":
            pos = self.tmx_data.get_object_by_name("boss")
            if math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) < 600 and math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) > 550 and self.cycle3 == 0 :
                self.cycle3 = 1
                self.spawn_boss()
            nb = 6
            nb2 = 6
        else:
            nb = 49
            nb2 = 41
 
        # Boucle vérifiant tout les Slimes
        for i in range(nb):
                
            # Recherche du Slime dans la map TMX
            slime = globals()["nom"+str(i)]='slime'+str(i)
            pos = self.tmx_data.get_object_by_name("slime{}".format(i))

            # Si ID du monstre non dans la liste de monstre présent
            if i not in self.liste_slime:
                
                # Si joueur a la fois pas trop proche et pas trop loin du spawn
                if math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) < 600 and math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) > 550:

                    # Création du monstre de la classe monstre et ajout dans la liste de monstre et ID du monstre et ajout du sprite du monstre
                    self.liste_slime.append(i)
                    slime = Monstre(pos.x,pos.y,i,"slime",self.player.niveau)
                    self.liste["slime"].append(slime)
                    self.group.add(slime)
                    self.monstergroup.add(slime)

        # Boucle vérifiant tout les Champis
        for i in range(nb2):

            # Recherche du Champi dans la map TMX
            champi = globals()['nom'+str(i)]='champi'+str(i)
            pos = self.tmx_data.get_object_by_name("champi{}".format(i))

            # Si ID du monstre non dans la liste de monstre présent 
            if i not in self.liste_champi:

                # Si joueur a la fois pas trop proche et pas trop loin du spawn
                if math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) < 600 and math.sqrt((pos.x - self.player.rect.centerx)**2 + (pos.y - self.player.rect.centery)**2) > 550:

                    # Création du monstre de la classe monstre et ajout dans la liste de monstre et ID du monstre et ajout du sprite du monstre
                    self.liste_champi.append(i)
                    champi = Monstre(pos.x,pos.y,i,"champi",self.player.niveau)
                    self.liste["champi"].append(champi)
                    self.group.add(champi)
                    self.monstergroup.add(champi)

    """ Méthode qui l'intéraction entre les touches et le jeu """
        
    def input(self):

        # Initialisation d'une touche "pressée"
        pressed = pygame.key.get_pressed()
        # Compteur de nombre de touche directionnel pressée
        num_directions_pressed = 0

        # La touche echap n'est pas pressée et ne lance donc pas le menu pause
        if not pressed[pygame.K_ESCAPE]:
            self.pause = False
            self.cycle1 = 0
        # Menu pause - ECHAP
        elif pressed[pygame.K_ESCAPE] and not self.pause and self.cycle1 == 0:

            # Musique en pause
            pygame.mixer.music.pause()

            # Définition des options du menu
            options = ["Reprendre", "Menu"]
            selected_option = 0

            # Définition des polices
            font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "menu graphics\determinationmonoweb-webfont.ttf"), 34)

            # Prendre un screenshot de l'écran avant le menu pause
            pygame.image.save(self.screen, os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu graphics\overlay_pause.png"))

            # Définition des sons de menu
            pause = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/pause.wav'))
            unpause = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/unpause.wav'))
            pygame.mixer.Sound.play(pause).set_volume(0.5)

            # Menu pause True pour activé la boucle
            self.pause = True
            # Temps de transition 
            time = 0
            # Boucle principale du menu
            while self.pause:
                # Gestion des événements
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.mixer.Sound.play(unpause).set_volume(0.5)
                        pygame.mixer.music.unpause()
                        self.pause = False
                    # Parcours option (clavier)
                    elif event.type == pygame.KEYDOWN:
                        # Parcourir vers le haut
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(options)
                        # Parcourir vers le bas
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(options)
                        # Quitter le menu pause
                        elif event.key == pygame.K_ESCAPE:
                            pygame.mixer.Sound.play(unpause).set_volume(0.5)
                            pygame.mixer.music.unpause()
                            self.pause = False
                            self.cycle1 = 1
                        # Retour du choix
                        elif event.key == pygame.K_RETURN:
                            # Reprendre
                            if selected_option == 0:
                                pygame.mixer.Sound.play(unpause).set_volume(0.5)
                                pygame.mixer.music.unpause()
                                self.pause = False
                                pass
                            # Retour au menu
                            elif selected_option == 1:
                                pygame.mixer.Sound.play(unpause).set_volume(0.5)
                                pygame.mixer.music.unpause()
                                self.pause = False
                                self.STOP = True

                    # Parcours option (souris)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Récupérer la position de la souris
                        pos = pygame.mouse.get_pos()
                        # Vérifier si l'utilisateur a cliqué sur une option
                        for i, option in enumerate(options):
                            text = font.render(option, True, (255, 255, 255))
                            text_rect = text.get_rect(center=(800/5, 600/2 + i*50))
                            # Retour du choix
                            if text_rect.collidepoint(pos):
                                selected_option = i
                                # Reprendre
                                if selected_option == 0:
                                    pygame.mixer.Sound.play(unpause).set_volume(0.5)
                                    pygame.mixer.music.unpause()
                                    self.pause = False
                                    pass
                                # Retour au menu
                                elif selected_option == 1:
                                    pygame.mixer.Sound.play(unpause).set_volume(0.5)
                                    pygame.mixer.music.unpause()
                                    self.pause = False
                                    self.STOP = True          

                # Transition durant 15 cycles
                if time < 15:
                    # Sélection du screenshot
                    overlay_pause = Image.open(os.path.join(os.path.dirname(__file__), "menu graphics\overlay_pause.png"))
                    # Application de l'effet blur sur l'image
                    overlay_pause = overlay_pause.filter(ImageFilter.BLUR)
                    # Remplacement du screenshot par le screenshot avec effet
                    overlay_pause.save(os.path.join(os.path.dirname(__file__), "menu graphics\overlay_pause.png"))
                    # Ajout d'un cycle
                    time += 1
                
                # Sélection du screenshot avec effet
                drawn_background2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\overlay_pause.png'))
                # Sélection d'une image d'interface
                drawn_background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\pause_background.png'))
                # Affichage du screenshot avec effet
                self.screen.blit(drawn_background2,(0,0))
                # Affichage de l'image d'interface
                self.screen.blit(drawn_background,(0,0))

                # Affichage des options réparties sur l'écran en vertical
                for i, option in enumerate(options):
                    text = font.render(option, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(800/5, 600/2 + i*50))
                    if i == selected_option:
                        selection_color = pygame.Color("#000080")
                        pygame.draw.rect(self.screen, selection_color, text_rect.inflate(20, 20))
                    self.screen.blit(text, text_rect)
                # Mis à jour de l'écran (Actualisé)
                pygame.display.flip()


        # Le joueur attaque pas si touche ESPACE non pressée
        if not pressed[pygame.K_SPACE]:
            self.prev_space_pressed = False
        # Le joueur attaque - ESPACE et l'intervalle d'attaque est fini
        elif pressed[pygame.K_SPACE] and not self.prev_space_pressed:
            self.prev_space_pressed = True
            if not self.player.is_attacking:
                self.player.attack(self.direction)

        # Le joueur cours - SHIFT GAUCHE
        if pressed[pygame.K_LSHIFT]:
            self.player.speed = 2.5
        
        # Le joueur se déplace en haut - TOUCHE DIRECTION HAUT OU Z
        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.animate('up_walk')
            self.direction = 'up'
            num_directions_pressed += 1
        # Le joueur se déplace en bas - TOUCHE DIRECTION BAS OU S
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.animate('down_walk')
            self.direction = 'down'
            num_directions_pressed += 1
        # Le joueur se déplace à gauche - TOUCHE DIRECTION GAUCHE OU Q
        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.animate('left_walk')
            self.direction = 'left'
            num_directions_pressed += 1
        # Le joueur se déplace à droite - TOUCHE DIRECTION DROITE OU D
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.animate('right_walk')
            self.direction = 'right'
            num_directions_pressed += 1

        # Le joueur sauvegarde si il est dans une zone de sauvegarde
        if pressed[pygame.K_e]:

            # Si joueur dans zone de sauvegarde
            if self.verify_currently_in_save():
                self.save()
            
            # Si joueur dans zone de pierre rouge
            if self.verify_currently_in_red() and self.red == 0:
                self.rouge.val = 1

            # Si joueur dans zone de pierre vert
            if self.verify_currently_in_green() and self.green == 0:
                self.vert.val = 1

            # Si joueur dans zone de pierre bleu
            if self.verify_currently_in_blue() and self.blue == 0:
                self.bleu.val = 1

            # Si joueur dans zone de pierre violet
            if self.verify_currently_in_purple() and self.purple == 0:
                self.violet.val = 1
            
            # Si le joueur est dans le monde normal
            if self.world == "world":
                # Si joueur dans zone d'entrée
                if self.player.feet.colliderect(self.enter_castle_rect):
                    # Si le joueur a les conditions requis pour y rentré
                    if self.player.niveau >= 18 and self.red == 1 and self.blue == 1 and self.green == 1 and self.purple == 1:
                        # Tue tout les monstres du monde normal
                        self.kill_monsters()
                        # Transfert vers le château
                        self.switch_to_castle()
                        # Définition du monde en château
                        self.world = "castle"

            # Si le joueur est dans le château
            if self.world == "castle":
                # Si joueur dans zone de sortie
                if self.player.feet.colliderect(self.exit_castle_rect):
                    # Tue tout les monstres du château
                    self.kill_monsters()
                    # Transfert vers le monde normal
                    self.switch_to_world()
                    # Définition du monde en monde normal
                    self.world = "world"


        # Activation de l'animation sur place si aucune touche directionnelle pressée
        if num_directions_pressed == 0:
            # Joueur sur place en bas
            if self.direction == 'down':
                self.player.animation_rate = 8
                self.player.animate('down')
            # Joueur sur place en haut
            if self.direction == 'up':
                self.player.animation_rate = 8
                self.player.animate('up')
            # Joueur sur place à gauche
            if self.direction == 'left':
                self.player.animation_rate = 8
                self.player.animate('left')
            # Joueur sur place à droite
            if self.direction == 'right':
                self.player.animation_rate = 8
                self.player.animate('right')

        # Si 2 touches directionnelles enfoncée, adaptation vitesse et animation
        if num_directions_pressed == 2:
            self.player.animation_rate = 8
            self.player.speed = 1.7
        # Si 3 touches directionnelles enfoncée, adaptation animation
        elif num_directions_pressed == 3:
            self.player.animation_rate = 12
        # Si 4 touches directionnelles enfoncée, adaptation animation
        elif num_directions_pressed == 4:
            self.player.animation_rate = 16
        # Si 1 touche directionnelle enfoncée, adaptation vitesse et animation
        else:
            self.player.animation_rate = 4
            self.player.speed = 2

        for ev in pygame.event.get():
            if ev.type == pygame.KEYUP:
                # Si la minimap et la map sont désactivées, on active la minimap
                if pressed[pygame.K_w] and self.minimap == False and self.map == False:
                    self.minimap = True
                # Si la minimap est activée, on la désactive, on active la map
                elif pressed[pygame.K_w] and self.minimap == True and self.map == False:
                    self.minimap = False
                    self.map = True
                # Si la map est activée, on la désactive
                elif pressed[pygame.K_w] and self.minimap == False and self.map == True:
                    self.minimap = False
                    self.map = False

        """# DEBUG test PV et exp
        if pressed[pygame.K_v]:
            self.player.remove_pv(4)
        if pressed[pygame.K_b]:
            self.player.add_pv(4)
        if pressed[pygame.K_n]:
            self.player.add_exp(100)"""

    """ Méthode d'affichage des informations sur le joueur """

    def hud(self):
        # Police pour les textes
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "menu graphics\determinationmonoweb-webfont.ttf"), 30)
        fontexp = pygame.font.Font(os.path.join(os.path.dirname(__file__), "menu graphics\determinationmonoweb-webfont.ttf"), 18)

        # Couleurs
        white = (255, 255, 255)
        blue = (30,144,255)
        green = (0,201,87)
        red = (255,0,0)
        violet = (148,0,211)
        black = (0, 0, 0)

        # Récupération des informations du joueur
        pv = self.player.pv
        niveau = self.player.maj_niveau()[0]
        exp = self.player.exp
        seuil_exp = self.player.maj_niveau()[1]

        # Création des surfaces de texte
        pv_surf = font.render(f"PV ", True, white)
        no_surf = fontexp.render(f"Vous n'avez pas les éléments requis pour accéder au château ", True, white)
        yes_surf = fontexp.render(f"Appuie sur E pour accéder au château ", True, white)
        exit_surf = fontexp.render(f"Appuie sur E pour sortir du château ", True, white)
        save_surf = fontexp.render(f"Appuie sur E pour sauvegarder",True,white)
        medaille_surf = fontexp.render(f"Appuie sur E pour prendre la pierre",True,white)

        # Couleur d'affichage en fonction du niveau
        if self.player.niveau >= 6 and self.player.niveau < 12:
            niveau_surf = font.render(f"Niveau: {niveau}", True, blue)
        elif self.player.niveau >= 12 and self.player.niveau < 18:
            niveau_surf = font.render(f"Niveau: {niveau}", True, green)
        elif self.player.niveau >= 18 and self.player.niveau < 25:
            niveau_surf = font.render(f"Niveau: {niveau}", True, red)
        elif self.player.niveau == 25:
            niveau_surf = font.render(f"Niveau: {niveau}", True, violet)
        else:
            niveau_surf = font.render(f"Niveau: {niveau}", True, white)

        if self.minimap == True and self.map == False and self.world == "world":
            self.screen.blit(self.minimap_img,(600,80))
        elif self.map == True and self.world == "world":
            self.screen.blit(self.map_img,(140,100))
        if self.world == "castle":
            self.minimap = False
            self.map = False

        # Ne pas affiché l'exp si level max
        if self.player.niveau != 25:
            exp_surf = fontexp.render(f"EXP: {exp}/{seuil_exp}",True,white)
        else:
            exp_surf = fontexp.render(f"MAX",True,white)

        # Récupération de la largeur de l'écran
        screen_width = pygame.display.get_surface().get_width()

        # Largeur des éléments du HUD
        element_width = max(pv_surf.get_width(), niveau_surf.get_width())

        # Position et dimensions des rectangles de fond
        bg_rect = pygame.Rect(0, 0, screen_width, 60)
        bg_rect2 = pygame.Rect(0, 540, screen_width, 60)

        # Position des éléments du HUD
        niveau_pos = (screen_width - element_width) // 2
        if self.player.niveau != 25:
            exp_pos = (screen_width - element_width) // 1.95
        else: 
            exp_pos = (screen_width - element_width) // 1.70
        save_pos = (screen_width - element_width) // 2.5
        no_pos = (screen_width - element_width) // 7
        yes_pos = (screen_width - element_width) // 3

        # Affichage des éléments du HUD
        self.screen.fill(black, bg_rect)
        self.screen.fill(black, bg_rect2)
        self.screen.blit(niveau_surf, (niveau_pos, 10))
        self.screen.blit(self.image_med, (650, 550))
        self.screen.blit(exp_surf,(exp_pos,39))

        # Affichage des pierres si obtenu
        if self.red == 1:
            self.screen.blit(pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\ROUGE.png')).convert_alpha(), (757, 554))
        if self.green == 1:
            self.screen.blit(pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\VERT.png')).convert_alpha(), (689, 556))
        if self.blue == 1:
            self.screen.blit(pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\BLEU.png')).convert_alpha(), (655, 558))
        if self.purple == 1:
            self.screen.blit(pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\VIOLET.png')).convert_alpha(), (723, 555))

        # Si dans zone de sauvegarde
        if self.verify_currently_in_save():
            self.screen.blit(save_surf,(save_pos,560))

        # Si dans zone de pierre rouge
        if self.verify_currently_in_red() and self.red == 0:
            self.screen.blit(medaille_surf,(save_pos,560))

        # Si dans zone de pierre vert
        if self.verify_currently_in_green() and self.green == 0:
            self.screen.blit(medaille_surf,(save_pos,560))

        # Si dans zone de pierre bleu
        if self.verify_currently_in_blue() and self.blue == 0:
            self.screen.blit(medaille_surf,(save_pos,560))

        # Si dans zone de pierre violet
        if self.verify_currently_in_purple() and self.purple == 0:
            self.screen.blit(medaille_surf,(save_pos,560))
        
        # Si dans monde normal
        if self.world == "world":
            # Si dans zone d'entrée
            if self.player.feet.colliderect(self.enter_castle_rect):
                # Si le joueur a les éléments requis
                if self.player.niveau >= 18 and self.red == 1 and self.blue == 1 and self.green == 1 and self.purple == 1:
                    self.screen.blit(yes_surf,(yes_pos,560))
                else:
                    self.screen.blit(no_surf,(no_pos,560))

        # Si dans château
        if self.world == "castle":
            if self.player.feet.colliderect(self.exit_castle_rect):
                self.screen.blit(exit_surf,(yes_pos,560))    
 
        # Définition d'une couleur pour PV monstre (vert clair)
        bar_color = (111, 210, 46)

        # Définition d'une couleur pour l'arriere plan de la barre de PV (gris foncé)
        back_bar_color =(60, 63, 60)

        # Définition de la position de la barre de vie du monstre
        for i in range(len(self.classe_monstre)):
            self.screen.fill(back_bar_color,pygame.Rect(550,10 + 10*i, self.classe_monstre[i].pv_max,5))
            self.screen.fill(bar_color,pygame.Rect(550,10 + 10*i, self.classe_monstre[i].pv,5))

        """ Fonction d'affichage des PV du joueur selon son niveau de PV """

        def affichage_pv(pv):
            # 
            if self.player.pv_max == 100:
                possible = [i for i in range(100,-5,-5)]
            elif self.player.pv_max == 120:
                possible = [i for i in range(120,-5,-5)]
            else:
                possible = [i for i in range(140,-5,-5)]
            for i in range(len(possible)):
                if pv == possible[i]:
                    return possible[i]
                if pv < possible[i] and pv > possible[i+1]:
                    return possible[i+1]
                
        # Prise de fichier en fonction des PV MAX du joueur
        if self.player.pv_max == 100:
            barre_vie = pygame.image.load(os.path.join(os.path.dirname(__file__), "TSX\Sprites\hearts_sprites\health" + "{}".format(affichage_pv(pv))+".png"))
        elif self.player.pv_max == 120:
            barre_vie = pygame.image.load(os.path.join(os.path.dirname(__file__), "TSX\Sprites\hearts_sprites2\health" + "{}".format(affichage_pv(pv))+".png"))
        else:
            barre_vie = pygame.image.load(os.path.join(os.path.dirname(__file__), "TSX\Sprites\hearts_sprites3\health" + "{}".format(affichage_pv(pv))+".png"))

        # Affichage des PV
        self.screen.blit(barre_vie,(20,20))

    """ Méthode de démarrage du jeu """

    def run(self):
        
        #
        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True
        # Initialisation des musiques en jeu
        changed_ost = False
        main_playing = True
        ice_cave_playing = False
        forest_playing = False
        volcano_playing = False
        islands_playing = False
        adventure_ost = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi_-_Exploring_The_Unknown_Loop.wav')
        icy_cave_ost = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi_-_The_Icy_Cave_Loop.wav')
        forest_ost = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi-And-The-Journey-Begins-_Loop.mp3')
        volcano_ost = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi-Mysterious-Dungeon.mp3')
        islands_ost = os.path.join(os.path.dirname(__file__), 'OST/Adventure Begins (Loopable).mp3')
        castle_ost = os.path.join(os.path.dirname(__file__), 'OST/Castle.wav')
        game_over_ost = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'OST/Game_Over.wav'))

        # Chargement des choix en cas de game over
        selected_option = 0

        # Boucle principal du jeu
        while running:
            
            # Tant que joueur en vie 
            if not self.game_over:
                
                # Amélioration en fonction du niveau
                if self.player.niveau >= 10 and self.player.niveau < 17:
                    self.player.pv_max = 120
                elif self.player.niveau >= 17 and self.player.niveau < 24:
                    self.player.pv_max = 140
                elif self.player.niveau >= 24:
                    self.player.attaque = 50

                # Réduction de temps pour se régénéré en fonction du niveau
                if self.player.niveau >= 13 and self.player.niveau < 20:
                    self.temps = 2700
                elif self.player.niveau >= 20:
                    self.temps = 1800

                # Reset d'exp si level max
                if self.player.niveau == 25:
                    self.player.exp = 0

                # Game Over si PV du joueur à 0 
                if self.player.pv <= 0:
                    self.game_over = True

                # Arrêt de la boucle si retour dans le menu sélectionné ou ECHAP sur le menu pause
                if self.STOP:
                    running = False
                # Initialisation si reprise
                self.STOP = False

                # Si l'on doit changer d'OST
                if changed_ost == True and self.world == "world":

                    #
                    if ice_cave_playing:
                        mixer.music.set_volume(self.ost_volume())
                        # 
                        if mixer.music.get_volume() == 0:
                            self.change_ost(icy_cave_ost)
                            changed_ost = False
                    #
                    if main_playing:

                        mixer.music.set_volume(self.ost_volume())
                        #
                        if mixer.music.get_volume() == 0:
                            self.change_ost(adventure_ost)
                            changed_ost = False
                    
                    #
                    if forest_playing:

                        mixer.music.set_volume(self.ost_volume())
                        #
                        if mixer.music.get_volume() == 0:
                            self.change_ost(forest_ost)
                            changed_ost = False

                    #
                    if volcano_playing:
                        mixer.music.set_volume(self.ost_volume())
                        #
                        if mixer.music.get_volume() == 0:
                            self.change_ost(volcano_ost)
                            changed_ost = False

                    #
                    if islands_playing:
                        mixer.music.set_volume(self.ost_volume())
                        #
                        if mixer.music.get_volume() == 0:
                            self.change_ost(islands_ost)
                            changed_ost = False

                # Sauvegarde de l'emplacement des monstres
                for monstre in self.classe_monstre:
                    monstre.save_location()
                    # Mise à jour de la position du joueur pour la classe monstre
                    monstre.position_joueur = self.player.position

                # Sauvegarde de l'emplacement du joueur
                self.player.save_location()
                # Détection des touches
                self.input()
                # Mise à jour de l'écran et des événements
                self.update(self.phase)
                # Vérification si pique touché par le joueur
                if self.verify_spikes():
                    self.player.remove_pv(3)
                #
                self.group.center(self.player.rect.center)
                # Affichage des sprites du groupe
                self.group.draw(self.screen)

                # Affichage des information
                self.hud()

                # Vérification si le joueur est dans la cave pour activer le filtre / la musique
                if self.verify_currently_in_cave() == True and self.world == "world":
                    self.music1 += 1
                    # Statut "dans la grotte" vrai
                    self.in_cave = True
                    # Mise à jour du filtre sombre autour du joueur
                    self.update_filter()
                    #
                    if ice_cave_playing == False:
                        changed_ost = True
                        main_playing = False
                        ice_cave_playing = True
                else:
                    #
                    if self.in_cave == True:
                        self.in_cave = False
                        changed_ost = True
                        main_playing = True
                        ice_cave_playing = False

                # Vérification si le joueur est dans la forêt pour activer la musique
                if self.verify_currently_in_forest() == True and self.world == "world":
                    self.music1 += 1
                    self.in_forest = True
                    #
                    if forest_playing == False:
                        changed_ost = True
                        main_playing = False
                        forest_playing = True
                else:
                    #
                    if self.in_forest == True:
                        self.in_forest = False
                        changed_ost = True
                        main_playing = True
                        forest_playing = False

                # Vérification si le joueur est dans la zone de feu pour activer la musique
                if self.verify_currently_in_volcano() == True and self.world == "world":
                    self.music1 += 1
                    self.in_volcano = True
                    #
                    if volcano_playing == False:
                        changed_ost = True
                        main_playing = False
                        volcano_playing = True
                else:
                    #
                    if self.in_volcano == True:
                        self.in_volcano = False
                        changed_ost = True
                        main_playing = True
                        volcano_playing = False

                # Vérification si le joueur est dans la zone des îles flottantes pour activer la musique
                if self.verify_currently_in_islands() == True and self.world == "world":
                    self.music1 += 1
                    self.in_floating_islands = True
                    #
                    if islands_playing == False:
                        changed_ost = True
                        main_playing = False
                        islands_playing = True
                else:
                    #
                    if self.in_floating_islands == True:
                        self.in_floating_islands = False
                        changed_ost = True
                        main_playing = True
                        islands_playing = False
                
                # Cas exeptionnelle ou le joueur débute directement dans le château ou dans le monde normal
                if not self.verify_currently_in_islands() and not self.verify_currently_in_volcano() and not self.verify_currently_in_forest() and not self.verify_currently_in_cave() and self.music1 == 0:
                    self.music1 += 1
                    # Si dans monde normal
                    if self.world == "world":
                        # Jouer musique theme principal
                        mixer.music.load(adventure_ost)
                        pygame.mixer.music.set_volume(0.4)
                        mixer.music.play(-1)
                    else:
                        # Jouer musique château
                        mixer.music.load(castle_ost)
                        pygame.mixer.music.set_volume(1)
                        mixer.music.play(-1)


                # Mise à jour de l'écran
                pygame.display.flip()

                # Si jeu quitté
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Cas du Game Over
            else:
                # Création de latence pour mettre brutalement la mélodie du game over
                if self.cycle2 == 0:
                    mixer.music.stop()
                elif self.cycle2 == 60:
                    pygame.mixer.Sound.play(game_over_ost).set_volume(0.9)   
                self.cycle2 += 1

                # Définition de la police d'écriture
                font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "menu graphics\determinationmonoweb-webfont.ttf"), 28)
                # Option du game over
                options = ["Réessayer", "Menu", "Quitter"]

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
                            game_over_ost.stop()
                            running = False
                        # Retour du choix
                        elif event.key == pygame.K_RETURN:
                            # Relance à la dernière sauvegarde
                            if selected_option == 0:
                                game_over_ost.stop()
                                self.relance = True
                                running = False
                            # Menu
                            elif selected_option == 1:
                                game_over_ost.stop()
                                running = False
                            # Quitter le jeu 
                            elif selected_option == 2:
                                game_over_ost.stop()
                                pygame.QUIT()

                    # Parcours option (souris)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Récupérer la position de la souris
                        pos = pygame.mouse.get_pos()
                        # Vérifier si l'utilisateur a cliqué sur une option
                        for i, option in enumerate(options):
                            text = font.render(option, True, (255, 255, 255))
                            text_rect = text.get_rect(center=(800/2, 600/2 + i*50))
                            # Retour du choix
                            if text_rect.collidepoint(pos):
                                selected_option = i
                                # Relance à la dernière sauvegarde
                                if selected_option == 0:
                                    game_over_ost.stop()
                                    self.relance = True
                                    running = False
                                # Menu
                                elif selected_option == 1:
                                    game_over_ost.stop()
                                    running = False
                                    pass
                                # Quitter le jeu
                                elif selected_option == 2:
                                    game_over_ost.stop()
                                    pygame.QUIT()

                # Selection du fond principal
                drawn_background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'menu graphics\GameOver.png'))
                self.screen.blit(drawn_background,(0,0))
                # Affichage des options réparties sur l'écran en vertical

                for i, option in enumerate(options):
                    text = font.render(option, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(800/2, 600/2 + i*50))
                    if i == selected_option:
                        selection_color = pygame.Color("#7A8CCD")
                        pygame.draw.rect(self.screen, selection_color, text_rect.inflate(20, 20))
                    self.screen.blit(text, text_rect)
                # Mis à jour de l'écran (Actualisé)
                pygame.display.flip()
                
            # Définition des cycles du jeu
            clock.tick(60)


    """ Mise à jour de tous les objets sur la carte, et vérification des collisions """

    def update(self,phase):

        # Fusion actualisé des listes contenant les objets des classes monstres
        self.classe_monstre = self.liste["slime"] + self.liste["champi"] + self.liste["boss"]
        # Spawn des monstres
        self.spawn_monstre()

        # Mise à jour du monstre
        for monstre in self.classe_monstre:
            # Mise à jour du monstre
            monstre.update(phase,self.direction)
            if monstre.type == "boss":
                monstre.update_boss()
            # Si le joueur est devant ou attaque le monstre, sprite du joueur qui passe avant celui du monstre
            if self.player.rect.y + 19 > monstre.rect.y or self.player.is_attacking == True:
                # Changement de calque pour priorisé le joueur
                self.monstergroup.change_layer(monstre, 7)
                self.group.change_layer(monstre, 6)
            else:
                # Changement de calque pour priorisé le monstre
                self.monstergroup.change_layer(monstre, 6)
                self.group.change_layer(monstre, 7)
                    
            # Si le monstre a un projectile actif
            if monstre.type != "boss":
                if monstre.projectile == True:
                    # Execution qu'une fois par projectile
                    if monstre.cycle5 == 0:
                        monstre.cycle5 += 1
                        # Ajout du projectile au groupe de sprite
                        self.group.add(monstre.projectile_var)
                    # Vérifie la collision entre le joueur et le projectile
                    if pygame.sprite.collide_mask(self.player, monstre.projectile_var):
                        self.player_attacked = True
                        # Enlève 10 PV au joueur si touché
                        self.player.remove_pv(monstre.attaque)
                        self.player_attacked = False
                        # Suppression du projectile après avoir touché
                        monstre.projectile_var.kill()
                    # Mise à jour du projectile
                    monstre.projectile_var.update()
                    # Suppression du projectile du groupe de sprite et reset des variables
                    if monstre.projectile_var.actif == False:
                        monstre.cycle5 = 0
                        self.group.remove(monstre.projectile_var)
                        monstre.cycle4 = 0
                        monstre.projectile = False

        # Mise à jour des pierres
        for medaille in self.medaille:
            medaille.update()

        # Mise à jour du joueur
        self.player.update(self.direction)

        # Mise à jour intéraction Monstre/Joueur
        self.interaction_monstre()
        self.medaille_pris()
        self.regeneration(self.temps)

        # Cooldown d'ajout d'exp
        if self.timer2 > 0:
            self.timer2 += 1
            if self.timer2 > 20:
                self.timer2 = 0

        # Vérification des collisions
        for sprite in self.group.sprites():
            if not isinstance(sprite, Projectile) and not isinstance(sprite,Medaille):

                # Créer un masque de collision pour le sprite
                sprite_mask = sprite.mask_fixe

                # Créer un masque de collision modifié pour le sprite
                sprite_mask_modified = pygame.mask.Mask(sprite_mask.get_size())
                sprite_mask_modified.clear()

                # Trouver la partie la plus basse non transparente du sprite
                for x in range(sprite_mask.get_size()[0]):
                    for y in range(sprite_mask.get_size()[1]-1, -1, -1):
                        if sprite_mask.get_at((x, y)) == 1:
                            sprite_mask_modified.set_at((x, y+3), 1)
                            break

                # Vérifier si le sprite entre en collision avec un mur
                for wall_rect in self.walls:
                    # Créer un masque de collision pour le mur
                    wall_mask = pygame.mask.Mask(wall_rect.size)
                    wall_mask.fill()

                    # Calculer la position relative du masque de collision modifié du sprite par rapport au mur
                    offset = (wall_rect.x - sprite.rect.x, wall_rect.y - sprite.rect.y)

                    # Vérifie si les masques de collision se superposent
                    if sprite_mask_modified.overlap(wall_mask, offset) is not None:
                        # Si c'est un mur, le joueur n'avance pas plus
                        sprite.move_back()

        # Cooldown pour évité crash par cause de spam donc création de latence
        if self.wait1 > 0:
            self.wait1 += 1
            if self.wait1 > 90:
                self.wait1 = 0

    """ Méthode qui gère les comportement et les intéraction entre le joueur et le monstre """

    def interaction_monstre(self):
        
        # Pour chaque monstre de la liste de monstre
        for monstre in self.classe_monstre:
            
            # Si monstre pas mort
            if not monstre.is_dead:
                
                # Définition de l'emplacement du joueur par rapport au monstre
                if monstre.position[0] < self.player.position[0]:
                    monstre.placement_joueur = "droite"
                else:
                    monstre.placement_joueur = "gauche"

                # Changement de type de mask utilisé pour le joueur
                self.player.mask_deplacement = False
                self.player.type_mask()

                # Détection si le monstre et le joueur se touchent et n'est pas mort
                if pygame.sprite.collide_mask(self.player, monstre):                 

                    # Si le joueur est en train d'attaquer et que le cycle du cooldown d'attaque est finie
                    if self.player.is_attacking and not monstre.direction == "cache" and not monstre.direction == "cache_droite":
                        monstre.is_attacked = True
                        monstre.remove_pv(self.player.attaque)
                        if self.timer2 == 0:
                            self.timer2 += 1
                            # Ajout d'exp en fonction du niveau des monstres si pas level max
                            if self.player.niveau != 25:
                                if monstre.color == "blue":
                                    self.player.add_exp(125)
                                elif monstre.color == "green":
                                    self.player.add_exp(200)
                                elif monstre.color == "red":
                                    self.player.add_exp(350)
                                
                        monstre.is_attacked = False
                    
                # Si le monstre et le joueur ne se touche plus (reset)
                else:
                    self.player_attacked = False
                    monstre.is_attacked = False

                # Changement de type de mask utilisé pour le joueur
                self.player.mask_deplacement = True
                self.player.type_mask()

                # Si le joueur n'est pas en train d'attaquer et que le monstre n'est pas attaqué et que le joueur n'est pas déjà attaqué
                if pygame.sprite.collide_mask(self.player, monstre) and not self.player.is_attacking and not monstre.is_attacked_anime and not self.player_attacked:
                    self.player_attacked = True
                    self.player.remove_pv(monstre.attaque)
                    self.player_attacked = False

                # Si le monstre et le joueur ne se touche plus (reset)
                else:
                    self.player_attacked = False
                    monstre.is_attacked = False

                # Détection si le monstre et le joueur sont proches
                if math.sqrt((monstre.rect.centerx - self.player.rect.centerx)**2 + (monstre.rect.centery - self.player.rect.centery)**2) < 160 and not monstre.type == "champi" and not monstre.type == "champi":
                    if math.sqrt((monstre.rect.centerx - self.player.rect.centerx)**2 + (monstre.rect.centery - self.player.rect.centery)**2) > 40 and not monstre.type == "boss":
                        monstre.animate_monstre("deplacement")
                    elif not monstre.type == "boss":
                        monstre.animate_monstre("attack")

                    # Déplacement en cohérence avec l'animation
                    if monstre.animation_timer < 5 and monstre.en_deplacement and monstre.animation_timer > 1 or monstre.type == "boss":
                        # Calculer le centre du joueur
                        player_center_x = self.player.position[0] + (self.player.rect.width - 14) / 2
                        player_center_y = self.player.position[1] + self.player.rect.height / 2

                        # Calculer le centre du monstre
                        monster_center_x = monstre.position[0] + monstre.rect.width / 2
                        monster_center_y = monstre.position[1] + monstre.rect.height / 2

                        # Calculer le vecteur de direction vers le joueur
                        dx = player_center_x - monster_center_x
                        dy = player_center_y - monster_center_y

                        # Normaliser le vecteur de direction pour obtenir une vitesse constante
                        magnitude = math.sqrt(dx**2 + dy**2)
                        if magnitude > 0:
                            dx /= magnitude
                            dy /= magnitude

                        # Selection d'un 2ème monstre
                        for monstre2 in self.monstergroup:
                            # Si 2 monstres différents se touche et ne sont pas mort
                            if monstre != monstre2 and pygame.sprite.collide_mask(monstre, monstre2) and not monstre2.is_dead:
                                    
                                # Calcule de l'écart
                                deca_x = monstre.position[0] - monstre2.position[0]
                                deca_y = monstre.position[1] - monstre2.position[1]
                                    
                                # Création d'un écart en x entre les monstres pour évité la superposition des monstres
                                if deca_x > -12 and deca_x < 12 :
                                    if deca_x > 0:
                                        monstre.position[0] += monstre.speed
                                    else:
                                        monstre.position[0] -= monstre.speed
                                # Création d'un écart en y entre les monstres pour évité la superposition des monstres
                                if deca_y > -12 and deca_y < 12 :
                                    if deca_y > 0:
                                        monstre.position[1] += monstre.speed
                                    else:
                                        monstre.position[1] -= monstre.speed

                        # Le monstre ne bouge plus si le joueur et le monstre se touche
                        if pygame.sprite.collide_mask(self.player, monstre) or monstre.is_attacked:

                            # Reset de la position
                            monstre.position[0] -= dx * monstre.speed
                            monstre.position[1] -= dy * monstre.speed

                        # Ajouter la distance parcourue à la position actuelle du monstre pour le déplacer
                        monstre.position[0] += dx * monstre.speed
                        monstre.position[1] += dy * monstre.speed

                        # Mettre à jour la position du sprite
                        monstre.rect.x = monstre.position[0]
                        monstre.rect.y = monstre.position[1]

                # Si monstre proche joueur et non mort
                if math.sqrt((monstre.rect.centerx - self.player.rect.centerx)**2 + (monstre.rect.centery - self.player.rect.centery)**2) < 160:
                    monstre.proche = True
                else:
                    monstre.proche = False
            # Cas ou monstre mort
            else:
                if monstre.cycle6 == 0:
                    monstre.cycle6 += 1
                    # Ajout d'exp en fonction du niveau des monstres si pas level max
                    if self.player.niveau != 25:
                        if monstre.color == "blue":
                            self.player.add_exp(200)
                        elif monstre.color == "green":
                            self.player.add_exp(500)
                        elif monstre.color == "red":
                            self.player.add_exp(700)
                
            # Si monstre trop loin du joueur
            if math.sqrt((monstre.position[0] - self.player.rect.centerx)**2 + (monstre.position[1] - self.player.rect.centery)**2) > 600:
                if monstre.type != "boss":
                    # Suppression des objets de la classe monstre et des sprites stocké dans le groupe de sprite
                    self.liste[monstre.type].remove(monstre)
                    if monstre.type == "slime":
                        self.liste_slime.remove(monstre.nombre)
                    if monstre.type == "champi":
                        self.liste_champi.remove(monstre.nombre)
                    self.group.remove(monstre)
                    self.monstergroup.remove(monstre)
                    del(monstre)


    """ Méthode qui vérifie si un sprite touche les piques """

    def verify_spikes(self):
        for sprite in self.group.sprites():
            if not isinstance(sprite, Projectile) and not isinstance(sprite, Medaille) and self.world == "world":
                if sprite.feet.collidelist(self.spikes) > -1:
                    return True

    """ Mise à jour du filtre appliqué quand le joueur se trouve dans une grotte """

    def update_filter(self):
        cave_filter = pygame.image.load(os.path.join(os.path.dirname(__file__), "screen filters\cave_filter.png"))
        self.screen.blit(cave_filter, (0, 60))

    """ Méthode qui vérifie si le joueur est dans les zones spécifiques """

    def verify_currently_in_cave(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.cave) > -1:
                return True
            return False
    
    def verify_currently_in_forest(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.forest) > -1:
                return True
            return False

    def verify_currently_in_volcano(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.volcano) > -1:
                return True
            return False

    def verify_currently_in_islands(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.islands) > -1:
                return True
            return False
    
    def verify_currently_in_save(self):
            if self.player.feet.collidelist(self.savezone) > -1:
                return True
            return False
    
    def verify_currently_in_red(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.red_zone) > -1:
                return True
            return False
    
    def verify_currently_in_green(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.green_zone) > -1:
                return True
            return False
    
    def verify_currently_in_blue(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.blue_zone) > -1:
                return True
            return False
    
    def verify_currently_in_purple(self):
        if self.world == "world":
            if self.player.feet.collidelist(self.purple_zone) > -1:
                return True
            return False
    
    """ Méthode qui régénère les PV du joueur après un temps selon le niveau du joueur sans s'être fais attaquer """
    
    def regeneration(self,time):
        # Si joueur attaqué, reset du timer
        if self.player.repos:
            self.timer1 = 0
        else:
            self.timer1 += 1
        # Régénère PV joueur au bout du temps définit en fonction du niveau du joueur
        if self.timer1 > time and self.player.pv != self.player.pv_max:
            self.player.pv += 0.083
            if self.player.pv > self.player.pv_max:
                self.player.pv = self.player.pv_max

    """ Méthode qui renvoie la prise d'une pierre et active une mélodie """

    def medaille_pris(self):
        for medaille in self.medaille:
            if medaille.val == 1:
                if medaille.color == "red" and self.red == 0:
                    pygame.mixer.Sound.play(self.get).set_volume(0.5)
                    self.red = 1
                    self.save()
                if medaille.color == "green" and self.green == 0:
                    pygame.mixer.Sound.play(self.get).set_volume(0.5)
                    self.green = 1
                    self.save()
                if medaille.color == "blue" and self.blue == 0:
                    pygame.mixer.Sound.play(self.get).set_volume(0.5)
                    self.blue = 1
                    self.save()
                if medaille.color == "purple" and self.purple == 0:
                    pygame.mixer.Sound.play(self.get).set_volume(0.5)
                    self.purple = 1
                    self.save()
                
                self.group.remove(medaille)
                del(medaille)

    """ Méthode gérant le transfert du joueur au château """

    def switch_to_castle(self):
        
        # Son de porte
        door = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/door.wav'))
        pygame.mixer.Sound.play(door).set_volume(0.5)

        # Chargement de la carte en tmx
        self.tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), 'inside_castlemap.tmx'))
        map_data = pyscroll.TiledMapData(self.tmx_data)

        # Musique du château
        castle_ost = os.path.join(os.path.dirname(__file__), 'OST/Castle.wav')

        pygame.mixer.music.stop()
        self.change_ost(castle_ost)
        pygame.mixer.music.set_volume(1)

        # Création du zoom et de la caméra suivant le joueur
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Définir une liste stockant tous les rectangles de collisions des murs
        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Définir une liste stockant tous les rectangles de collisions des sauvegardes
        self.savezone = []
        for obj in self.tmx_data.objects:
            if obj.type == "save":
                self.savezone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.monstergroup = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Rect de collision pour sortir du château
        exit_castle = self.tmx_data.get_object_by_name('exit_castle')
        self.exit_castle_rect = pygame.Rect(exit_castle.x,exit_castle.y,exit_castle.width,exit_castle.height)
        # Point de spawn dans le château
        spawn_castle_point = self.tmx_data.get_object_by_name("spawn_castle")
        self.player.position[0] = spawn_castle_point.x
        self.player.position[1] = spawn_castle_point.y

    """ Méthode gérant le transfert du joueur au monde normal """

    def switch_to_world(self):
        
        # Son de porte
        door = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/door.wav'))
        pygame.mixer.Sound.play(door).set_volume(0.5)

        # Chargement de la carte en tmx
        self.tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), 'worldmap.tmx'))
        map_data = pyscroll.TiledMapData(self.tmx_data)

        # Musique thème principale
        adventure_ost = os.path.join(os.path.dirname(__file__), 'OST/xDeviruchi_-_Exploring_The_Unknown_Loop.wav')

        pygame.mixer.music.stop()
        self.change_ost(adventure_ost)

        # Création du zoom et de la caméra suivant le joueur
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Définir une liste stockant tous les rectangles de collisions des murs
        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir une liste stockant tous les rectangles de collisions des piques
        self.spikes = []
        for obj in self.tmx_data.objects:
            if obj.type == "spike":
                self.spikes.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))


        # Définir une liste stockant tous les rectangles de collisions de la cave
        self.cave = []
        for obj in self.tmx_data.objects:
            if obj.type == "cave":
                self.cave.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
    
        # Définir une liste stockant tous les rectangles de collisions de la forêt
        self.forest = []
        for obj in self.tmx_data.objects:
            if obj.type == "forest":
                self.forest.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir une liste stockant tous les rectangles de collisions du volcan
        self.volcano = []
        for obj in self.tmx_data.objects:
            if obj.type == "volcano":
                self.volcano.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir une liste stockant tous les rectangles de collisions des îles
        self.islands = []
        for obj in self.tmx_data.objects:
            if obj.type == "thunder":
                self.islands.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir une liste stockant tous les rectangles de collisions des sauvegardes
        self.savezone = []
        for obj in self.tmx_data.objects:
            if obj.type == "save":
                 self.savezone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir zone de pierre rouge
        self.red_zone = []
        for obj in self.tmx_data.objects:
            if obj.type == "red":
                self.red_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir zone de pierre vert
        self.green_zone = []
        for obj in self.tmx_data.objects:
            if obj.type == "green":
                self.green_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir zone de pierre bleu
        self.blue_zone = []
        for obj in self.tmx_data.objects:
            if obj.type == "blue":
                self.blue_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Définir zone de pierre violet
        self.purple_zone = []
        for obj in self.tmx_data.objects:
            if obj.type == "purple":
                self.purple_zone.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        # Dessin du groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.monstergroup = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Rect de collision pour entrer dans le château
        enter_castle = self.tmx_data.get_object_by_name('enter_castle')
        self.enter_castle_rect = pygame.Rect(enter_castle.x, enter_castle.y, enter_castle.width, enter_castle.height)
        # Point de spawn dans le monde
        spawn_world_point = self.tmx_data.get_object_by_name("spawn_world")
        
        # Téléportation du joueur au spawn du château
        self.player.position[0] = spawn_world_point.x
        self.player.position[1] = spawn_world_point.y

    """ Méthode qui tue tout les monstres de la map actuelle """

    def kill_monsters(self):
        
        for monstre in self.classe_monstre:
            self.liste[monstre.type].remove(monstre)
            if monstre.type == "slime":
                self.liste_slime.remove(monstre.nombre)
                if monstre.type == "champi":
                    self.liste_champi.remove(monstre.nombre)
                self.group.remove(monstre)
                self.monstergroup.remove(monstre)
                del(monstre)

    """ Méthode qui gère la transition du volume """

    def ost_volume(self):

        delay = 0.001
        music_volume = mixer.music.get_volume()
        if music_volume >= 0 and music_volume - delay >= 0:
            music_volume -= delay
            mixer.music.set_volume(music_volume)
            return music_volume
        elif music_volume >= 0 and music_volume - delay <= 0:
            music_volume = 0
            return music_volume
        
    """ Méthode qui gère le changement d'ost """

    def change_ost(self,ost):
        mixer.music.load(ost)
        music_volume = 0.5
        pygame.mixer.music.set_volume(music_volume)
        mixer.music.play(-1)

    """ Méthode qui gère le spawn du boss """

    def spawn_boss(self):

        pos = [self.tmx_data.get_object_by_name("boss").x,self.tmx_data.get_object_by_name("boss").y]
        boss = Boss(pos[0],pos[1])
        self.liste["boss"].append(boss)
        self.group.add(boss)
        self.monstergroup.add(boss)