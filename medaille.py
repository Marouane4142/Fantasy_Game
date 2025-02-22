import pygame
import os
import pytmx
import math

class Medaille(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        # Chargement de la carte en tmx
        self.tmx_data = pytmx.util_pygame.load_pygame(os.path.join(os.path.dirname(__file__), 'worldmap.tmx'))

        # Couleur de la pierre
        self.color = color

        if self.color == "red":
            # Image du sprite du projectile utilisé
            self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\ROUGE.png')).convert_alpha()
            # Position de la pierre
            self.position = self.tmx_data.get_object_by_name("rouge")
        if self.color == "green":
            # Image du sprite du projectile utilisé
            self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\VERT.png')).convert_alpha()
            # Position de la pierre
            self.position = self.tmx_data.get_object_by_name("vert")
        if self.color == "purple":
            # Image du sprite du projectile utilisé
            self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\VIOLET.png')).convert_alpha()
            # Position de la pierre
            self.position = self.tmx_data.get_object_by_name("violet")
        if self.color == "blue":
            # Image du sprite du projectile utilisé
            self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\BLEU.png')).convert_alpha()
            # Position de la pierre
            self.position = self.tmx_data.get_object_by_name("bleu")

        # Partie d'image initialement en cours d'utilisation
        self.image = self.get_image(0,0,self.sprite_sheet)
        # Définition des masks qui ne seront pas modulable
        self.mask_fixe = pygame.mask.from_surface(self.image)
        # Définition de la surface prise par la pierre
        self.rect = self.image.get_rect()
        # Définition du centre de la surface de la pierre
        self.rect.center = (self.position.x, self.position.y)
        # Timer (x d'une fonction)
        self.timer = 0
        # Obtenue ou non
        self.val = 0
        # Sauvegarde de la position y de base
        self.ybase = self.rect.centery


    """ Mise à jour du projectile """

    def update(self):
        # Simulation mouvement sinusoïdale 
        amplitude = 10
        periode = 200
        self.timer += 1
        delta_y = amplitude * math.sin((2 * math.pi * self.timer/periode))

        # Application du mouvement à self.rect.centery
        self.rect.centery = self.ybase + delta_y

    """ Méthode découpant le .png du projectile et retournant l'image du sprite"""

    def get_image(self,x,y,sprite):
        image = pygame.Surface([30,30], pygame.SRCALPHA)
        image.blit(sprite,(0,0),(x,y,30,30))
        return image
        