import pygame
import os
from pygame import mixer

from projectile import Projectile

class Monstre(pygame.sprite.Sprite):
    def __init__(self, x, y,nombre,type,lvl):
        super().__init__()
        # Type de monstre
        self.type = type
        # ID du monstre 
        self.nombre = nombre
        # Stock de la position du monstre (spawn)
        self.spawn = [x,y]
        # Stock de la position du monstre modulable
        self.position = [x,y]

        # Si le monstre est un slime
        if self.type == "slime":
            # Niveau du monstre en fonction du niveau du joueur
            if lvl < 12:
                # Image du sprite du monstre utilisé
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/slime.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 10
                # Vitesse du monstre
                self.speed = 1.6
                # PV max du monstre
                self.pv_max = 50
                # Niveau du monstre
                self.color = "blue"

            elif lvl >= 12 and lvl < 18:
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/green_slime.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 15
                # Vitesse du monstre
                self.speed = 1.8
                # PV max du monstre
                self.pv_max = 130
                # Niveau du monstre
                self.color = "green"
            else:
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/red_slime.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 20
                # Vitesse du monstre
                self.speed = 2
                # PV max du monstre
                self.pv_max = 200
                # Niveau du monstre
                self.color = "red"
            
            # Image initialement utilisé
            self.image = self.get_image(0,0,self.sprite_monstre)
            # Dictionnaire stockant les animations par actions du Slime
            self.images = {
                'pause' : [self.get_image(0,0,self.sprite_monstre), self.get_image(32,0,self.sprite_monstre), self.get_image(64,0,self.sprite_monstre), self.get_image(96,0,self.sprite_monstre)],
                'deplacement' : [self.get_image(0,32,self.sprite_monstre), self.get_image(32,32,self.sprite_monstre), self.get_image(64,32,self.sprite_monstre), self.get_image(96,32,self.sprite_monstre), self.get_image(128,32,self.sprite_monstre), self.get_image(160,32,self.sprite_monstre)],
                'deplacement_gauche' : [pygame.transform.flip(self.get_image(0,32,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,32,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,32,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(96,32,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(128,32,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(160,32,self.sprite_monstre), True, False)],
                'attack': [self.get_image(0,64,self.sprite_monstre), self.get_image(32,64,self.sprite_monstre), self.get_image(64,64,self.sprite_monstre), self.get_image(96,64,self.sprite_monstre), self.get_image(128,64,self.sprite_monstre), self.get_image(160,64,self.sprite_monstre)],
                'attack_gauche' : [pygame.transform.flip(self.get_image(0,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(96,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(128,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(160,64,self.sprite_monstre), True, False)],
                'degat': [self.get_image(0,96,self.sprite_monstre), self.get_image(32,96,self.sprite_monstre), self.get_image(64,96,self.sprite_monstre)],
                'degat_droite': [pygame.transform.flip(self.get_image(0,96,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,96,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,96,self.sprite_monstre), True, False)],
                'mort': [self.get_image(0,128,self.sprite_monstre), self.get_image(32,128,self.sprite_monstre), self.get_image(64,128,self.sprite_monstre), self.get_image(96,128,self.sprite_monstre), self.get_image(128,128,self.sprite_monstre), self.get_image(160,128,self.sprite_monstre)],
                'mort_gauche': [self.get_image(0,128,self.sprite_monstre), self.get_image(32,128,self.sprite_monstre), self.get_image(64,128,self.sprite_monstre), self.get_image(96,128,self.sprite_monstre), self.get_image(128,128,self.sprite_monstre), self.get_image(160,128,self.sprite_monstre)],
                }
            # Définition des masks
            self.mask = pygame.mask.from_surface(self.image)
            # Définition des masks qui ne seront pas modulable
            self.mask_fixe = pygame.mask.from_surface(self.image)
            # Définition de la surface prise par le monstre
            self.rect = self.image.get_rect()

            #
            self.rect.x = x
            self.rect.y = y

            # Définition de la surface prise par le slime
            self.rect.width = 15
            self.rect.height = 15
            # Emplacement des pieds du slime
            self.feet = pygame.Rect(0,0,self.rect.width * 0.5,12)
            
        if self.type == "champi":

            # Image du sprite du monstre utilisé
            if lvl < 12:
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/mushroom_spritesheet.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 10
                # PV max du monstre
                self.pv_max = 50
                # Niveau du monstre
                self.color = "blue"

            elif lvl >= 12 and lvl < 18:
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/green_mushroom_spritesheet.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 15
                # PV max du monstre
                self.pv_max = 130
                # Niveau du monstre
                self.color = "green"
            else:
                self.sprite_monstre = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/red_mushroom_spritesheet.png')).convert_alpha()
                # Point d'attaque du monstre
                self.attaque = 20
                # PV max du monstre
                self.pv_max = 200
                # Niveau du monstre
                self.color = "red"

            # Vitesse du monstre
            self.speed = 1.6

            # Image du mask du sprite du monstre utilisé
            self.sprite_monstre_mask = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/mushroom_spritesheet_mask.png')).convert_alpha()
            # Image initialement utilisé
            self.image = self.get_image(0,0,self.sprite_monstre)
            # Dictionnaire stockant les animations par actions du Champi
            self.images = {
                'pause' : [self.get_image(0,0,self.sprite_monstre), self.get_image(32,0,self.sprite_monstre), self.get_image(64,0,self.sprite_monstre), self.get_image(96,0,self.sprite_monstre)],
                "pause_gauche": [pygame.transform.flip(self.get_image(0,0,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,0,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,0,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(96,0,self.sprite_monstre), True, False)],
                'attack': [self.get_image(0,64,self.sprite_monstre), self.get_image(32,64,self.sprite_monstre), self.get_image(64,64,self.sprite_monstre), self.get_image(96,64,self.sprite_monstre), self.get_image(128,64,self.sprite_monstre), self.get_image(160,64,self.sprite_monstre), self.get_image(192,64,self.sprite_monstre)],
                'attack_gauche' : [pygame.transform.flip(self.get_image(0,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(96,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(128,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(160,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(192,64,self.sprite_monstre), True, False)],
                'degat_droite': [self.get_image(0,64,self.sprite_monstre), self.get_image(32,64,self.sprite_monstre), self.get_image(64,64,self.sprite_monstre), self.get_image(32,64,self.sprite_monstre),self.get_image(0,64,self.sprite_monstre)],
                'degat': [pygame.transform.flip(self.get_image(0,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(64,64,self.sprite_monstre), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(0,64,self.sprite_monstre), True, False)],
                'cache':[self.get_image(192,96,self.sprite_monstre),self.get_image(160,96,self.sprite_monstre),self.get_image(128,96,self.sprite_monstre),self.get_image(96,96,self.sprite_monstre),self.get_image(64,96,self.sprite_monstre),self.get_image(32,96,self.sprite_monstre),self.get_image(0,96,self.sprite_monstre),self.get_image(32,96,self.sprite_monstre),self.get_image(64,96,self.sprite_monstre),self.get_image(96,96,self.sprite_monstre),self.get_image(128,96,self.sprite_monstre),self.get_image(160,96,self.sprite_monstre),self.get_image(192,96,self.sprite_monstre)],
                'cache_droite':[pygame.transform.flip(self.get_image(192,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(0,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(192,96,self.sprite_monstre), True, False)],
                'mort': [self.get_image(192,96,self.sprite_monstre),self.get_image(160,96,self.sprite_monstre),self.get_image(128,96,self.sprite_monstre),self.get_image(96,96,self.sprite_monstre),self.get_image(64,96,self.sprite_monstre),self.get_image(32,96,self.sprite_monstre),self.get_image(0,96,self.sprite_monstre)],
                'mort_gauche': [pygame.transform.flip(self.get_image(192,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre), True, False),pygame.transform.flip(self.get_image(0,96,self.sprite_monstre), True, False)]
                }
            # Dictionnaire stockant les masks des animations par actions du Champi
            self.images_mask = {
                'pause' : [self.get_image(0,0,self.sprite_monstre_mask), self.get_image(32,0,self.sprite_monstre_mask), self.get_image(64,0,self.sprite_monstre_mask), self.get_image(96,0,self.sprite_monstre_mask)],
                "pause_gauche": [pygame.transform.flip(self.get_image(0,0,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(32,0,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(64,0,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(96,0,self.sprite_monstre_mask), True, False)],
                'attack': [self.get_image(0,64,self.sprite_monstre_mask), self.get_image(32,64,self.sprite_monstre_mask), self.get_image(64,64,self.sprite_monstre_mask), self.get_image(96,64,self.sprite_monstre_mask), self.get_image(128,64,self.sprite_monstre_mask), self.get_image(160,64,self.sprite_monstre_mask), self.get_image(192,64,self.sprite_monstre_mask)],
                'attack_gauche' : [pygame.transform.flip(self.get_image(0,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(64,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(96,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(128,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(160,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(192,64,self.sprite_monstre_mask), True, False)],
                'degat_droite': [self.get_image(0,64,self.sprite_monstre_mask), self.get_image(32,64,self.sprite_monstre_mask), self.get_image(64,64,self.sprite_monstre_mask), self.get_image(32,64,self.sprite_monstre_mask),self.get_image(0,64,self.sprite_monstre_mask)],
                'degat': [pygame.transform.flip(self.get_image(0,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(64,64,self.sprite_monstre_mask), True, False), pygame.transform.flip(self.get_image(32,64,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(0,64,self.sprite_monstre_mask), True, False)],
                'cache':[self.get_image(192,96,self.sprite_monstre_mask),self.get_image(160,96,self.sprite_monstre_mask),self.get_image(128,96,self.sprite_monstre_mask),self.get_image(96,96,self.sprite_monstre_mask),self.get_image(64,96,self.sprite_monstre_mask),self.get_image(32,96,self.sprite_monstre_mask),self.get_image(0,96,self.sprite_monstre_mask),self.get_image(32,96,self.sprite_monstre_mask),self.get_image(64,96,self.sprite_monstre_mask),self.get_image(96,96,self.sprite_monstre_mask),self.get_image(128,96,self.sprite_monstre_mask),self.get_image(160,96,self.sprite_monstre_mask),self.get_image(192,96,self.sprite_monstre_mask)],
                'cache_droite':[pygame.transform.flip(self.get_image(192,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(0,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(192,96,self.sprite_monstre_mask), True, False)],
                'mort': [self.get_image(192,96,self.sprite_monstre_mask),self.get_image(160,96,self.sprite_monstre_mask),self.get_image(128,96,self.sprite_monstre_mask),self.get_image(96,96,self.sprite_monstre_mask),self.get_image(64,96,self.sprite_monstre_mask),self.get_image(32,96,self.sprite_monstre_mask),self.get_image(0,96,self.sprite_monstre_mask)],
                'mort_gauche': [pygame.transform.flip(self.get_image(192,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(160,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(128,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(96,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(64,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(32,96,self.sprite_monstre_mask), True, False),pygame.transform.flip(self.get_image(0,96,self.sprite_monstre_mask), True, False)]
                }
            
            # Définition des masks
            self.mask = pygame.mask.from_surface(self.get_image(0,0,self.sprite_monstre_mask))
            # Définition des masks qui ne seront pas modulable
            self.mask_fixe = pygame.mask.from_surface(self.get_image(0,0,self.sprite_monstre_mask))
            # Définition de la surface prise par le monstre
            self.rect = self.image.get_rect()
            # Emplacement des pieds du slime
            self.feet = pygame.Rect(0,0,self.rect.width * 0.5,12)

        # Direction du joueur par rapport au monstre
        self.placement_joueur = ""
        # Récupération position afin de respecter les collision 
        self.old_position = self.position.copy()
        # Compteur temps animation
        self.animation_counter = 0
        # Niveau de rapidité de l'animation
        self.animation_rate = 8
        # Compteur d'étape d'animation
        self.animation_timer = 0
        # PV du monstre
        self.pv = self.pv_max
        # Attente pour cycle animation
        self.wait = 0
        # Simulation attente du champi
        self.wait2 = 0
        # Le monstre se déplace
        self.en_deplacement = False
        # Le monstre attaque
        self.attack = False
        # Le monstre est attaqué
        self.is_attacked = False
        # Le monstre est mort
        self.is_dead = False
        # Cycle pour reset 1 fois les variable a chaque degat au monstre
        self.cycle1 = 0
        # Cycle Activation 1 fois déplacement
        self.cycle2 = 0
        # Cycle qui active 1 seul fois la réinitialisation des variables
        self.cycle3 = 0
        # Cycle qui active 1 fois la création d'un projectile
        self.cycle4 = 0
        # Cycle qui active 1 fois l'ajout du sprite dans un groupe
        self.cycle5 = 0
        # Cycle donnant de l'exp au joueur en cas de mort du monstre
        self.cycle6 = 0
        # Timer simulant le temps de réaction après s'être fais attaquer
        self.timer = 0
        # Timer du cooldown intervalle de dégât reçu
        self.timer2 = 0
        # Timer simulant le temps de réactions pour attaquer du champi
        self.timer3 = 0
        # Direction ou va le monstre en train de se faire attaquer
        self.recule = "down"
        # Action du monstre
        self.direction = ""
        # Cooldown intervalle de dégât reçu
        self.repos = False
        # Animation actif de dégât reçu
        self.is_attacked_anime = False
        # Reçois l'information True si le joueur est proche
        self.proche = False
        # Reçois les coordonnées du joueur
        self.position_joueur = []
        # Renvoie True si le projectile est actif
        self.projectile = False
        # Variable qui stock l'objet de la classe projectile 
        self.projectile_var = 0
        
        

    """ Méthode lancement animation """

    def animate_monstre(self, phase):
        # Si le monstre ne se déplace pas et n'est pas mort
        if not self.en_deplacement and not self.pv <= 0 and not self.is_attacked_anime:
            # Si le monstre ne fais rien
            if phase == 'pause':
                # Si le monstre ne fais rien et est de type champi
                if self.type ==  "champi" and not self.direction == "attack" and not self.direction == "cache":
                    self.animation_rate = 18
                    # Réglage de la direction du monstre par rapport au joueur
                    if self.placement_joueur == "gauche":
                        self.image = self.images['pause'][self.animation_timer]
                    else:
                        self.image = self.images['pause_gauche'][self.animation_timer]
                    # Timer pour cycle d'attaque 
                    self.timer3 += 1
                    if self.timer3 >= 120 and self.proche:
                        self.direction = "attack"
                # Faire animation de pause pour autre type que champi
                if not self.type ==  "champi" and not self.direction == "attack" and not self.direction == "cache":
                    self.animation_rate = 8
                    self.image = self.images['pause'][self.animation_timer]

            # Si le monstre se déplace ou attaque
            if phase == 'deplacement' or phase == "attack":
                # Reset des variables
                self.animation_timer = 0
                self.attack_animation_counter = 0
                # Activation du cycle
                self.cycle2 += 1
                # Le monstre se déplace
                if phase == 'deplacement':
                    # Réglage de la direction du monstre par rapport au joueur
                    if self.placement_joueur == "droite":
                        self.image = self.images['deplacement'][self.animation_timer]
                    else:
                        self.image = self.images['deplacement_gauche'][self.animation_timer]
                # Le monstre attaque
                if phase == 'attack':
                    # Réglage de la direction du monstre par rapport au joueur
                    if self.placement_joueur == "droite":
                        self.image = self.images['attack'][self.animation_timer]
                    else:
                        self.image = self.images['attack_gauche'][self.animation_timer]
                # Initilisation des variables
                if self.cycle2 == 1:
                    self.en_deplacement = True
                    self.direction = phase

    """ Mise à jour du monstre """

    def update(self,phase,direction):
        
        #
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        # Animation pause si rien ne se passe
        self.animate_monstre(phase)
        self.event(phase,direction)

        # Intervalle d'invincibilité du monstre
        if self.repos:
            self.timer2 += 1
            if self.timer2 == 20:
                self.timer2 = 0
                self.repos = False

    """ Méthode gérant les événement et le comportement du monstre """

    def event(self,phase,direction):
        # Si monstre mort
        if self.pv <= 0:
            self.cycle3 += 1
            if self.cycle3 == 1:
                # Reset des variables
                self.animation_timer = 0
                self.animation_counter = 0
                self.animation_rate = 8
                self.wait = 0
                self.en_deplacement = False
                self.recule = direction
                self.is_dead = True
                # Joue un son
                hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds\dead.wav'))
                pygame.mixer.Sound.play(hit_sound).set_volume(1)
            # Execution tant que l'animation est non finie
            if len(self.images['mort']) > self.animation_timer:
                # Réglage de la direction du monstre par rapport au joueur
                if self.placement_joueur == "gauche":
                    self.image = self.images['mort'][self.animation_timer]
                else:
                    self.image = self.images['mort_gauche'][self.animation_timer]
                # Compteur temps de l'animation
                self.animation_counter += 1
                # Change l'étape de l'animation et ralentie l'animation
                if self.animation_counter % self.animation_rate == 0:
                    self.animation_timer += 1
                if self.animation_counter % self.animation_rate == 0:
                        self.animation_timer += 1
            else:
                # Reset des variables
                phase = 'pause'
                direction = 'pause'
                self.is_attacked_anime = False
                self.en_deplacement = False
                self.timer = 0
                self.cycle1 = 0
                self.wait = 0
                self.cycle2 = 0
                self.wait2 = 0
                self.timer2 = 0
        # Si le monstre est un champi, qu'il attaque et qu'il n'est pas mort
        if self.type == "champi" and self.direction == "attack" and not self.pv <= 0:
            self.animation_rate = 8
            # Execution du lancement de projectile en cohérence avec l'animation
            if self.animation_timer == 6 and self.cycle4 == 0:
                self.projectile_var = Projectile(self.rect.centerx,self.rect.centery,self.position_joueur[0]+21,self.position_joueur[1]+30)
                self.cycle4 +=1
                self.projectile = True
            # Execution tant que l'animation est non finie
            if len(self.images['attack']) > self.animation_timer:
                # Réglage de la direction du monstre par rapport au joueur
                if self.placement_joueur == "gauche":
                    self.image = self.images['attack'][self.animation_timer]
                else:
                    self.image = self.images['attack_gauche'][self.animation_timer]

            # Compteur temps de l'animation
                self.animation_counter += 1
                # Change l'étape de l'animation et ralentie l'animation
                if self.animation_counter % self.animation_rate == 0:
                    self.animation_timer += 1
            # Si animation fini
            else:
                # Attente de 20 tours
                if self.wait2 == 20:
                    # Reset des variables
                    self.animation_timer = 0
                    self.animation_counter = 0
                    self.direction = "cache"
                    self.timer3 = 0
                    self.wait2 = 0
                # Reprise de l'animation en pause
                else:
                    # Réglage de la direction du monstre par rapport au joueur
                    if self.placement_joueur == "gauche":
                        self.image = self.images['pause'][0]
                    else:
                        self.image = self.images['pause_gauche'][0]
                    self.wait2 += 1

        # Si le monstre est un champi non mort qui se cache
        if self.type == "champi" and self.direction == "cache" and not self.pv <= 0:
            self.animation_rate = 10
            # Condition en cohérence avec l'animation
            if self.animation_timer == 7:
                    self.wait2 += 1
                    # Attente de 120 tours avant reprise de l'animation
                    if self.wait2 == 120:
                        self.animation_timer = 8
                        self.wait2 = 0
            # Execution tant que l'animation est non finie
            if len(self.images['cache']) > self.animation_timer and self.wait2 == 0:
                # Réglage de la direction du monstre par rapport au joueur
                if self.placement_joueur == "gauche":
                    self.image = self.images['cache'][self.animation_timer]
                else:
                    self.image = self.images['cache_droite'][self.animation_timer]

            # Compteur temps de l'animation
                self.animation_counter += 1
                # Change l'étape de l'animation et ralentie l'animation
                if self.animation_counter % self.animation_rate == 0:
                    self.animation_timer += 1
            # Si animation fini
            else:
                # Reset des variable
                if self.wait2 == 0:
                    # Reset des variables
                    self.animation_timer = 0
                    self.animation_counter = 0
                    self.direction = "pause"
                
        # Si le monstre se déplace mais n'est pas attaqué et ni mort
        if self.en_deplacement and not self.is_attacked_anime and not self.pv <= 0:
            self.animation_rate = 8
            # Execution tant que l'animation est non finie
            if len(self.images[self.direction]) > self.animation_timer:
                # Attente de l'execution de la suite de l'animation pour animation complète et cohérente
                if self.animation_timer == 0 and self.wait < 30:
                    self.wait += 1
                else:
                    # Animation de déplacement du monstre
                    if self.direction == 'deplacement':
                        # Réglage de la direction du monstre par rapport au joueur
                        if self.placement_joueur == "droite":
                            self.image = self.images['deplacement'][self.animation_timer]
                        else:
                            self.image = self.images['deplacement_gauche'][self.animation_timer]
                    # Animation d'attaque du monstre
                    if self.direction == 'attack':
                        if self.placement_joueur == "droite":
                            # Réglage de la direction du monstre par rapport au joueur
                            self.image = self.images['attack'][self.animation_timer]
                        else:
                            self.image = self.images['attack_gauche'][self.animation_timer]
                    # Compteur temps de l'animation
                    self.animation_counter += 1
                    # Change l'étape de l'animation et ralentie l'animation
                    if self.animation_counter % self.animation_rate == 0:
                        self.animation_timer += 1
            # Si animation fini
            else:
                # Reset des variables
                self.animation_timer = 0
                self.animation_counter = 0
                self.wait = 0
                self.cycle2 = 0
                self.en_deplacement = False

        # Et si non attaqué, ni mort, ni en train d'attaquer ou se cacher
        elif not self.is_attacked_anime and not self.pv <= 0 and not self.direction == "attack" and not self.direction == "cache":
            # Compteur temps de l'animation
            self.animation_counter += 1

            # Change l'étape de l'animation et ralentie l'animation
            if self.animation_counter % self.animation_rate == 0:
                self.animation_timer += 1
            # Si animation fini
            if self.animation_timer >= len(self.images[phase]):
                # Reset des variables
                self.animation_timer = 0
                self.animation_counter = 0

        # Si le monstre est attaqué
        if self.is_attacked_anime and not self.pv <= 0:
            self.cycle1 += 1
            if self.cycle1 == 1:
                # Reset des variables
                self.animation_timer = 0
                self.animation_counter = 0
                self.animation_rate = 10
                self.wait = 0
                self.cycle2 = 0
                self.en_deplacement = False
                self.recule = direction

            # Si le monstre est un Champi
            if self.type ==  "champi":
                self.animation_rate = 6

            # Execution tant que l'animation est non finie
            if len(self.images['degat']) > self.animation_timer:
                if self.placement_joueur == "droite":
                    self.image = self.images['degat'][self.animation_timer]
                else:
                    self.image = self.images['degat_droite'][self.animation_timer]
                self.animation_counter += 1
                if self.recule == "down":
                    self.position[1] += self.speed
                if self.recule == "up":
                    self.position[1] -= self.speed
                if self.recule == "left":
                    self.position[0] -= self.speed
                if self.recule == "right":
                    self.position[0] += self.speed
                    
                if self.animation_counter % self.animation_rate == 0:
                    self.animation_timer += 1
            # Temps de remise après dégats au monstre
            else:
                self.timer += 1
                if self.timer > 30:
                    # Reset des variables
                    self.animation_timer = 0
                    self.animation_counter = 0
                    self.is_attacked_anime = False
                    self.timer = 0
                    self.cycle1 = 0

    """ Méthode découpant le .png du monstre, pour utiliser chaque sprite correspondant à l'action en cours """

    def get_image(self,x,y,sprite):
        if self.type == "slime":
            image = pygame.Surface([32,32], pygame.SRCALPHA)
        if self.type == "champi":
            image = pygame.Surface([28,28], pygame.SRCALPHA)
        image.blit(sprite,(0,0),(x,y,32,32))
        return image
    
    """ Méthode replaçant le joueur à sa position précédente lorsqu'il entre en collision avec un objet """
    
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    """ Méthode sauvegardant la position du joueur, utile quand il entre en collision avec un objet """

    def save_location(self):
        self.old_position = self.position.copy()

    """ Méthodes temporaires de test, pour l'affichage des pv et le level up du joueur """

    def remove_pv(self,removed):
        # Enlèvement de PV
        if not self.repos:
            self.is_attacked_anime = True
            self.pv -= removed
            self.repos = True
            if self.pv < 0:
                self.pv = 0

    """ Méthode qui retourne un str monstre + son nombre en fonction de l'ordre de spawn"""

    def __repr__(self):
        return "Monstre{}".format(self.nombre)