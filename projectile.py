import pygame
import math
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        # Image du sprite du projectile utilisé
        self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\projectile.png')).convert_alpha()
        # Image initialement utilisé
        self.image = self.get_image(0,0,self.sprite_sheet)
        # Définition des masks qui ne seront pas modulable
        self.mask_fixe = pygame.mask.from_surface(self.image)
        # Définition de la surface prise par le projectile
        self.rect = self.image.get_rect()
        # Définition du centre de la surface du projectile
        self.rect.center = (start_x, start_y)
        # Raccourcie
        self.target_x = target_x
        self.target_y = target_y
        # Timer pour simulé la disparition du projectile a un temps initié 
        self.timer = 0
        # Vitesse du projectile
        self.speed = 3
        # Info sur l'activité du projectile
        self.actif = True
        # Distance entre le monstre et le joueur
        distance = math.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        # Définition du déplacement du projectile et de sa direction
        self.dx = (target_x - start_x) * self.speed / distance
        self.dy = (target_y - start_y) * self.speed / distance

    """ Mise à jour du projectile """

    def update(self):
        self.timer += 1
        # Déplacement du projectile vers la position cible
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Après 230 tours, supprimer l'objet
        if self.timer > 230:
            self.actif = False
            self.kill()

    """ Méthode découpant le .png du projectile et retournant l'image du sprite"""

    def get_image(self,x,y,sprite):
        image = pygame.Surface([5,5], pygame.SRCALPHA)
        image.blit(sprite,(0,0),(x,y,5,5))
        return image