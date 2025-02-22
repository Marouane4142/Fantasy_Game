import pygame
import os

""" PAS FINIS """

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.type = "boss"

        self.spawn = [x, y]

        self.position = [x, y]

        self.sprite_boss = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/boss_spritesheet.png')).convert_alpha()
        self.sprite_boss_mask = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX/Sprites/boss_spritesheet_mask.png')).convert_alpha()

        # Points d'attaque
        self.attaque = 25
        # Vitesse du boss
        self.speed = 1.8
        # PV max du boss
        self.pv_max = 500

        self.image = self.get_image(0, 0, self.sprite_boss)
        self.images = {
            'down_walk' : [self.get_image(96,0,self.sprite_boss),self.get_image(192,48,self.sprite_boss),self.get_image(288,96,self.sprite_boss)],
            'up_walk' : [self.get_image(96,96,self.sprite_boss),self.get_image(192,96,self.sprite_boss),self.get_image(288,96,self.sprite_boss)],
            'right_walk' : [self.get_image(96,192,self.sprite_boss),self.get_image(192,192,self.sprite_boss),self.get_image(288,192,self.sprite_boss)],
            'left_walk' : [self.get_image(96,288,self.sprite_boss),self.get_image(192,288,self.sprite_boss),self.get_image(288,288,self.sprite_boss)],
            'down_action' : [self.get_image(96,384,self.sprite_boss),self.get_image(192,384,self.sprite_boss),self.get_image(288,384,self.sprite_boss),self.get_image(384,384,self.sprite_boss),self.get_image(480,384,self.sprite_boss),self.get_image(576,384,self.sprite_boss)],
            'up_action' : [self.get_image(96,480,self.sprite_boss),self.get_image(192,480,self.sprite_boss),self.get_image(288,480,self.sprite_boss),self.get_image(384,480,self.sprite_boss),self.get_image(480,480,self.sprite_boss),self.get_image(576,480,self.sprite_boss)],
            'right_action' : [self.get_image(96,576,self.sprite_boss),self.get_image(192,576,self.sprite_boss),self.get_image(288,576,self.sprite_boss),self.get_image(384,576,self.sprite_boss),self.get_image(480,576,self.sprite_boss),self.get_image(576,576,self.sprite_boss)],
            'left_action' : [self.get_image(96,672,self.sprite_boss),self.get_image(192,672,self.sprite_boss),self.get_image(288,672,self.sprite_boss),self.get_image(384,672,self.sprite_boss),self.get_image(480,672,self.sprite_boss),self.get_image(576,672,self.sprite_boss)]
            }
        
        self.images_mask = {
            'down_walk' : [self.get_image(96,0,self.sprite_boss_mask),self.get_image(192,48,self.sprite_boss_mask),self.get_image(288,96,self.sprite_boss_mask)],
            'up_walk' : [self.get_image(96,96,self.sprite_boss_mask),self.get_image(192,96,self.sprite_boss_mask),self.get_image(288,96,self.sprite_boss_mask)],
            'right_walk' : [self.get_image(96,192,self.sprite_boss_mask),self.get_image(192,192,self.sprite_boss_mask),self.get_image(288,192,self.sprite_boss_mask)],
            'left_walk' : [self.get_image(96,288,self.sprite_boss_mask),self.get_image(192,288,self.sprite_boss_mask),self.get_image(288,288,self.sprite_boss_mask)],
            'down_action' : [self.get_image(96,384,self.sprite_boss_mask),self.get_image(192,384,self.sprite_boss_mask),self.get_image(288,384,self.sprite_boss_mask),self.get_image(384,384,self.sprite_boss_mask),self.get_image(480,384,self.sprite_boss_mask),self.get_image(576,384,self.sprite_boss_mask)],
            'up_action' : [self.get_image(96,480,self.sprite_boss_mask),self.get_image(192,480,self.sprite_boss_mask),self.get_image(288,480,self.sprite_boss_mask),self.get_image(384,480,self.sprite_boss_mask),self.get_image(480,480,self.sprite_boss_mask),self.get_image(576,480,self.sprite_boss_mask)],
            'right_action' : [self.get_image(96,576,self.sprite_boss_mask),self.get_image(192,576,self.sprite_boss_mask),self.get_image(288,576,self.sprite_boss_mask),self.get_image(384,576,self.sprite_boss_mask),self.get_image(480,576,self.sprite_boss_mask),self.get_image(576,576,self.sprite_boss_mask)],
            'left_action' : [self.get_image(96,672,self.sprite_boss_mask),self.get_image(192,672,self.sprite_boss_mask),self.get_image(288,672,self.sprite_boss_mask),self.get_image(384,672,self.sprite_boss_mask),self.get_image(480,672,self.sprite_boss_mask),self.get_image(576,672,self.sprite_boss_mask)]
            }

        # Application du mask
        self.mask = pygame.mask.from_surface(self.get_image(0,0,self.sprite_boss_mask))
        # Application du mask non modulable
        self.mask_fixe = pygame.mask.from_surface(self.get_image(0,0,self.sprite_boss_mask))

        # Définition de la surface prise par le monstre
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Compteur temps animation
        self.animation_counter = 0
        # Niveau de rapidité de l'animation
        self.animation_rate = 8
        # Compteur d'étape d'animation
        self.animation_timer = 0

        # Direction du joueur par rapport au monstre
        self.position_joueur = []

        # Récupération position afin de respecter les collision
        self.old_position = self.position.copy()
        # PV du monstre
        self.pv = self.pv_max
        # Le monstre se déplace
        self.en_deplacement = False
        # Le monstre attaque
        self.attack = False
        # Le monstre est attaqué
        self.is_attacked = False
        # Le monstre est mort
        self.is_dead = False
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
        self.timer1 = 0

    def update_boss(self):
        # Cooldown d'invicibilité après dégât sur le joueur
        if self.repos:
            self.timer1 += 1
            if self.timer1 == 40:
                self.timer1 = 0
                self.repos = False


    def get_image(self, x, y,sprite):
        image = pygame.Surface([96, 96], pygame.SRCALPHA)
        image.blit(sprite, (0, 0), (x, y, 96, 96))
        return image
    
    def save_location(self):
        self.old_position = self.position.copy()
    

    def animate_monstre_boss(self):
        pass

    """ Méthodes temporaires de test, pour l'affichage des pv et le level up du joueur """

    def remove_pv(self,removed):
        # Enlèvement de PV
        if not self.repos:
            self.is_attacked_anime = True
            self.pv -= removed
            self.repos = True
            if self.pv < 0:
                self.pv = 0

