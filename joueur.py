import pygame
import os

class Joueur(pygame.sprite.Sprite):

    def __init__(self,x,y,pv,pvmax,attaque,niveau,exp):
        super().__init__()
        # Image du sprite du joueur utilisé
        self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\sprite_reference.png')).convert_alpha()
        # Image du mask du sprite du joueur utilisé
        self.sprite_sheet_mask = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\sprite_reference_mask.png')).convert_alpha()
        # Image du mask d'attaque du sprite du joueur utilisé
        self.sprite_sheet_mask_attaque = pygame.image.load(os.path.join(os.path.dirname(__file__), 'TSX\Sprites\sprite_reference_mask_attaque.png')).convert_alpha()
        # Partie d'image initialement en cours d'utilisation
        self.image = self.get_image(0,0,self.sprite_sheet)
        # Création de la surface du joueur
        self.rect = self.image.get_rect()
        # Stock de la position du joueur
        self.position = [x,y]

        # Dictionnaire de série d'animation par action
        self.images = {
            'down' : [self.get_image(0,0,self.sprite_sheet), self.get_image(48,0,self.sprite_sheet), self.get_image(96,0,self.sprite_sheet), self.get_image(144,0,self.sprite_sheet), self.get_image(192,0,self.sprite_sheet), self.get_image(240,0,self.sprite_sheet)],
            'right' : [self.get_image(0,48,self.sprite_sheet), self.get_image(48,48,self.sprite_sheet), self.get_image(96,48,self.sprite_sheet), self.get_image(144,48,self.sprite_sheet), self.get_image(192,48,self.sprite_sheet), self.get_image(240,48,self.sprite_sheet)],
            'left' : [pygame.transform.flip(self.get_image(0,48,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(48,48,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(96,48,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(144,48,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(192,48,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(240,48,self.sprite_sheet), True, False)],
            'up': [self.get_image(0,96,self.sprite_sheet), self.get_image(48,96,self.sprite_sheet), self.get_image(96,96,self.sprite_sheet), self.get_image(144,96,self.sprite_sheet), self.get_image(192,96,self.sprite_sheet), self.get_image(240,96,self.sprite_sheet)],
            'down_walk': [self.get_image(0,144,self.sprite_sheet), self.get_image(48,144,self.sprite_sheet), self.get_image(96,144,self.sprite_sheet), self.get_image(144,144,self.sprite_sheet), self.get_image(192,144,self.sprite_sheet), self.get_image(240,144,self.sprite_sheet)],
            'right_walk': [self.get_image(0,192,self.sprite_sheet), self.get_image(48,192,self.sprite_sheet), self.get_image(96,192,self.sprite_sheet), self.get_image(144,192,self.sprite_sheet), self.get_image(192,192,self.sprite_sheet), self.get_image(240,192,self.sprite_sheet)],
            'left_walk': [pygame.transform.flip(self.get_image(0,192,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(48,192,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(96,192,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(144,192,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(192,192,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(240,192,self.sprite_sheet), True, False)],
            'up_walk': [self.get_image(0,240,self.sprite_sheet), self.get_image(48,240,self.sprite_sheet), self.get_image(96,240,self.sprite_sheet), self.get_image(144,240,self.sprite_sheet), self.get_image(192,240,self.sprite_sheet), self.get_image(240,240,self.sprite_sheet)],
            'down_attack': [self.get_image(0,288,self.sprite_sheet), self.get_image(48,288,self.sprite_sheet), self.get_image(96,288,self.sprite_sheet), self.get_image(144,288,self.sprite_sheet)],
            'right_attack': [self.get_image(0,336,self.sprite_sheet), self.get_image(48,336,self.sprite_sheet), self.get_image(96,336,self.sprite_sheet), self.get_image(144,336,self.sprite_sheet)],
            'left_attack': [pygame.transform.flip(self.get_image(0,336,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(48,336,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(96,336,self.sprite_sheet), True, False), pygame.transform.flip(self.get_image(144,336,self.sprite_sheet), True, False)],
            'up_attack': [self.get_image(0,384,self.sprite_sheet), self.get_image(48,384,self.sprite_sheet), self.get_image(96,384,self.sprite_sheet), self.get_image(144,384,self.sprite_sheet)]
            }
        
        # Dictionnaire de mask de la série d'animation par action
        self.images_mask = {
            'down' : [self.get_image(0,0,self.sprite_sheet_mask), self.get_image(48,0,self.sprite_sheet_mask), self.get_image(96,0,self.sprite_sheet_mask), self.get_image(144,0,self.sprite_sheet_mask), self.get_image(192,0,self.sprite_sheet_mask), self.get_image(240,0,self.sprite_sheet_mask)],
            'right' : [self.get_image(0,48,self.sprite_sheet_mask), self.get_image(48,48,self.sprite_sheet_mask), self.get_image(96,48,self.sprite_sheet_mask), self.get_image(144,48,self.sprite_sheet_mask), self.get_image(192,48,self.sprite_sheet_mask), self.get_image(240,48,self.sprite_sheet_mask)],
            'left' : [pygame.transform.flip(self.get_image(0,48,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(48,48,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(96,48,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(144,48,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(192,48,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(240,48,self.sprite_sheet_mask), True, False)],
            'up': [self.get_image(0,96,self.sprite_sheet_mask), self.get_image(48,96,self.sprite_sheet_mask), self.get_image(96,96,self.sprite_sheet_mask), self.get_image(144,96,self.sprite_sheet_mask), self.get_image(192,96,self.sprite_sheet_mask), self.get_image(240,96,self.sprite_sheet_mask)],
            'down_walk': [self.get_image(0,144,self.sprite_sheet_mask), self.get_image(48,144,self.sprite_sheet_mask), self.get_image(96,144,self.sprite_sheet_mask), self.get_image(144,144,self.sprite_sheet_mask), self.get_image(192,144,self.sprite_sheet_mask), self.get_image(240,144,self.sprite_sheet_mask)],
            'right_walk': [self.get_image(0,192,self.sprite_sheet_mask), self.get_image(48,192,self.sprite_sheet_mask), self.get_image(96,192,self.sprite_sheet_mask), self.get_image(144,192,self.sprite_sheet_mask), self.get_image(192,192,self.sprite_sheet_mask), self.get_image(240,192,self.sprite_sheet_mask)],
            'left_walk': [pygame.transform.flip(self.get_image(0,192,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(48,192,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(96,192,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(144,192,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(192,192,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(240,192,self.sprite_sheet_mask), True, False)],
            'up_walk': [self.get_image(0,240,self.sprite_sheet_mask), self.get_image(48,240,self.sprite_sheet_mask), self.get_image(96,240,self.sprite_sheet_mask), self.get_image(144,240,self.sprite_sheet_mask), self.get_image(192,240,self.sprite_sheet_mask), self.get_image(240,240,self.sprite_sheet_mask)],
            'down_attack': [self.get_image(0,288,self.sprite_sheet_mask), self.get_image(48,288,self.sprite_sheet_mask), self.get_image(96,288,self.sprite_sheet_mask), self.get_image(144,288,self.sprite_sheet_mask)],
            'right_attack': [self.get_image(0,336,self.sprite_sheet_mask), self.get_image(48,336,self.sprite_sheet_mask), self.get_image(96,336,self.sprite_sheet_mask), self.get_image(144,336,self.sprite_sheet_mask)],
            'left_attack': [pygame.transform.flip(self.get_image(0,336,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(48,336,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(96,336,self.sprite_sheet_mask), True, False), pygame.transform.flip(self.get_image(144,336,self.sprite_sheet_mask), True, False)],
            'up_attack': [self.get_image(0,384,self.sprite_sheet_mask), self.get_image(48,384,self.sprite_sheet_mask), self.get_image(96,384,self.sprite_sheet_mask), self.get_image(144,384,self.sprite_sheet_mask)]
            }

        # Dictionnaire de mask d'attaque de la série d'animation par action
        self.images_mask_attaque = {
            'down' : [self.get_image(0,0,self.sprite_sheet_mask_attaque), self.get_image(48,0,self.sprite_sheet_mask_attaque), self.get_image(96,0,self.sprite_sheet_mask_attaque), self.get_image(144,0,self.sprite_sheet_mask_attaque), self.get_image(192,0,self.sprite_sheet_mask_attaque), self.get_image(240,0,self.sprite_sheet_mask_attaque)],
            'right' : [self.get_image(0,48,self.sprite_sheet_mask_attaque), self.get_image(48,48,self.sprite_sheet_mask_attaque), self.get_image(96,48,self.sprite_sheet_mask_attaque), self.get_image(144,48,self.sprite_sheet_mask_attaque), self.get_image(192,48,self.sprite_sheet_mask_attaque), self.get_image(240,48,self.sprite_sheet_mask_attaque)],
            'left' : [pygame.transform.flip(self.get_image(0,48,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(48,48,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(96,48,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(144,48,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(192,48,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(240,48,self.sprite_sheet_mask_attaque), True, False)],
            'up': [self.get_image(0,96,self.sprite_sheet_mask_attaque), self.get_image(48,96,self.sprite_sheet_mask_attaque), self.get_image(96,96,self.sprite_sheet_mask_attaque), self.get_image(144,96,self.sprite_sheet_mask_attaque), self.get_image(192,96,self.sprite_sheet_mask_attaque), self.get_image(240,96,self.sprite_sheet_mask_attaque)],
            'down_walk': [self.get_image(0,144,self.sprite_sheet_mask_attaque), self.get_image(48,144,self.sprite_sheet_mask_attaque), self.get_image(96,144,self.sprite_sheet_mask_attaque), self.get_image(144,144,self.sprite_sheet_mask_attaque), self.get_image(192,144,self.sprite_sheet_mask_attaque), self.get_image(240,144,self.sprite_sheet_mask_attaque)],
            'right_walk': [self.get_image(0,192,self.sprite_sheet_mask_attaque), self.get_image(48,192,self.sprite_sheet_mask_attaque), self.get_image(96,192,self.sprite_sheet_mask_attaque), self.get_image(144,192,self.sprite_sheet_mask_attaque), self.get_image(192,192,self.sprite_sheet_mask_attaque), self.get_image(240,192,self.sprite_sheet_mask_attaque)],
            'left_walk': [pygame.transform.flip(self.get_image(0,192,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(48,192,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(96,192,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(144,192,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(192,192,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(240,192,self.sprite_sheet_mask_attaque), True, False)],
            'up_walk': [self.get_image(0,240,self.sprite_sheet_mask_attaque), self.get_image(48,240,self.sprite_sheet_mask_attaque), self.get_image(96,240,self.sprite_sheet_mask_attaque), self.get_image(144,240,self.sprite_sheet_mask_attaque), self.get_image(192,240,self.sprite_sheet_mask_attaque), self.get_image(240,240,self.sprite_sheet_mask_attaque)],
            'down_attack': [self.get_image(0,288,self.sprite_sheet_mask_attaque), self.get_image(48,288,self.sprite_sheet_mask_attaque), self.get_image(96,288,self.sprite_sheet_mask_attaque), self.get_image(144,288,self.sprite_sheet_mask_attaque)],
            'right_attack': [self.get_image(0,336,self.sprite_sheet_mask_attaque), self.get_image(48,336,self.sprite_sheet_mask_attaque), self.get_image(96,336,self.sprite_sheet_mask_attaque), self.get_image(144,336,self.sprite_sheet_mask_attaque)],
            'left_attack': [pygame.transform.flip(self.get_image(0,336,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(48,336,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(96,336,self.sprite_sheet_mask_attaque), True, False), pygame.transform.flip(self.get_image(144,336,self.sprite_sheet_mask_attaque), True, False)],
            'up_attack': [self.get_image(0,384,self.sprite_sheet_mask_attaque), self.get_image(48,384,self.sprite_sheet_mask_attaque), self.get_image(96,384,self.sprite_sheet_mask_attaque), self.get_image(144,384,self.sprite_sheet_mask_attaque)]
            }

        # Application du mask
        self.mask = pygame.mask.from_surface(self.get_image(0,0,self.sprite_sheet_mask))
        # Application du mask non modulable
        self.mask_fixe = pygame.mask.from_surface(self.get_image(0,0,self.sprite_sheet_mask))
        # Surface des pieds du joueurs
        self.feet = pygame.Rect(0,0,self.rect.width * 0.5,12)
        # Récupération position afin de respecter les collision 
        self.old_position = self.position.copy()
        # Liste des couples niveau - exp
        self.niveaux_exp = [(i * 225) for i in range(1, 26)]
        # Vitesse du joueur
        self.speed = 6
        # Niveau du joueur par défaut
        self.niveau = niveau
        # PV du joueur
        self.pv = pv
        # PV max du joueur (par défaut)
        self.pv_max = pvmax
        # EXP du joueur par défaut
        self.exp = exp
        # EXP max du joueur
        self.exp_max = self.niveaux_exp[-1]
        # Compteur temps animation (déplacement)
        self.animation_counter = 0
        # Niveau de rapidité de l'animation (déplacement)
        self.animation_rate = 4
        # Compteur d'étape d'animation (déplacement)
        self.animation_timer = 0
        # Compteur temps animation (attaque)
        self.attack_animation_counter = 0
        # Niveau de rapidité de l'animation (attaque)
        self.attack_animation_rate = 5
        # Compteur d'étape d'animation (attaque)
        self.attack_animation_timer = 0
        # Si le joueur attaque ou non
        self.is_attacking = False
        # Le joueur est attaqué
        self.is_attacked = False
        # Cooldown intervalle de dégât reçu
        self.repos = False
        # Timer du cooldown intervalle de dégât reçu
        self.timer2 = 0
        # Iniatilisation de quelle mask utilisé
        self.mask_deplacement = False
        # Action du joueur
        self.action = ""
        # Point d'attaque du joueur
        self.attaque = attaque

    """ Méthodes d'animation de l'attaque du joueur """

    def attack(self, direction):
        # Détection si le joueur est en train d'attaquer ou non
        if not self.is_attacking:
            swing_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds\snd_shakerbreaker.wav'))
            # Définition du statut "en train d'attaquer" au joueur
            self.is_attacking = True
            # Si il attaque en bas
            if direction == 'down':
                self.attack_animation_timer = 0
                self.attack_animation_counter = 0
                self.image = self.images['down_attack'][self.attack_animation_timer]
                self.update_masks('down_attack',self.attack_animation_timer)
                self.action = 'down_attack'
            # Si il attaque à gauche
            if direction == 'left':
                self.attack_animation_timer = 0
                self.attack_animation_counter = 0
                self.image = self.images['left_attack'][self.attack_animation_timer]
                self.update_masks('left_attack',self.attack_animation_timer)
                self.action = 'left_attack'
            # Si il attaque à droite
            if direction == 'right':
                self.attack_animation_timer = 0
                self.attack_animation_counter = 0
                self.image = self.images['right_attack'][self.attack_animation_timer]
                self.update_masks('right_attack',self.attack_animation_timer)
                self.action = 'right_attack'
            # Si il attaque en haut
            if direction == 'up':
                self.attack_animation_timer = 0
                self.attack_animation_counter = 0
                self.image = self.images['up_attack'][self.attack_animation_timer]
                self.update_masks('up_attack',self.attack_animation_timer)
                self.action = 'up_attack'
            pygame.mixer.Sound.play(swing_sound).set_volume(0.5)

    """ Méthodes de mouvements du joueur """

    def animate(self, direction):
        # Animation lorsque le joueur ne bouge pas en bas
        if direction == 'down':
            self.image = self.images['down'][self.animation_timer]
            self.update_masks('down',self.animation_timer)
            self.action = 'down'
        # Animation lorsque le joueur ne bouge pas à gauche
        if direction == 'left':
            self.image = self.images['left'][self.animation_timer]
            self.update_masks('left',self.animation_timer)
            self.action = 'left'
        # Animation lorsque le joueur ne bouge pas à droite
        if direction == 'right':
            self.image = self.images['right'][self.animation_timer]
            self.update_masks('right',self.animation_timer)
            self.action = 'right'
        # Animation lorsque le joueur ne bouge pas en haut
        if direction == 'up':
            self.image = self.images['up'][self.animation_timer]
            self.update_masks('up',self.animation_timer)
            self.action = 'up'
        # Animation et mouvement lorsque le joueur bouge en bas
        if direction == 'down_walk':
            self.position[1] += self.speed
            self.image = self.images['down_walk'][self.animation_timer]
            self.update_masks('down_walk',self.animation_timer)
            self.action = 'down_walk'
        # Animation et mouvement lorsque le joueur bouge à gauche
        if direction == 'left_walk':
            self.position[0] -= self.speed
            self.image = self.images['left_walk'][self.animation_timer]
            self.update_masks('left_walk',self.animation_timer)
            self.action = 'left_walk'
        # Animation et mouvement lorsque le joueur bouge à droite
        if direction == 'right_walk':
            self.position[0] += self.speed
            self.image = self.images['right_walk'][self.animation_timer]
            self.update_masks('right_walk',self.animation_timer)
            self.action = 'right_walk'
        # Animation et mouvement lorsque le joueur bouge en haut
        if direction == 'up_walk':
            self.position[1] -= self.speed
            self.image = self.images['up_walk'][self.animation_timer]
            self.update_masks('up_walk',self.animation_timer)
            self.action = 'up_walk'

        # Compteur temps de l'animation
        self.animation_counter += 1

        # Change l'étape de l'animation et ralentie l'animation
        if self.animation_counter % self.animation_rate == 0:
            self.animation_timer += 1
        # Si animation fini
        if self.animation_timer >= len(self.images[direction]):
            # Reset des variables
            self.animation_timer = 0

    """ Méthode sauvegardant la position du joueur, utile quand il entre en collision avec un objet """

    def save_location(self):
        self.old_position = self.position.copy()

    """ Méthodes d'affichage HUD """

    def hud(screen, joueur):
        font = pygame.font.Font(None, 24)
        text = font.render("PV: " + str(joueur.pv) + "   Niveau: " + str(joueur.niveau) + "   Magie: " + str(joueur.magie), True, (255, 255, 255))
        screen.blit(text, (10, 10))

    """ Méthodes temporaires de test, pour l'affichage des pv et le level up du joueur """

    def remove_pv(self,removed):
        # Chargement du son
        hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds\damage.wav'))
        # Enlèvement de PV
        if not self.repos:
            self.pv -= removed
            self.repos = True
            if self.pv < 0:
                self.pv = 0
            # Jouer son
            pygame.mixer.Sound.play(hit_sound).set_volume(0.5)
            # Si les pv tombent en dessous de 0 quand le joueur prend des dégâts, ils prennent la valeur 0

    """ Méthodes ajoutant des PV au joueur """

    def add_pv(self,added):
        # Ajout de PV
        self.pv += added
        # Si les pv une fois régénérés dépassent le seuil, ils prennent la valeur du seuil
        if self.pv > self.pv_max:
            self.pv = self.pv_max

    """ Méthodes ajoutant de l'experience au joueur """

    def add_exp(self,added):
        # Ajout d'expérience
        self.exp += added

    """ Méthode mettant à jour la position du joueur à chaque déplacement """

    def update(self,direction):

        # Définition du joueur au centre de la caméra
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        # Cooldown d'invicibilité après dégât sur le joueur
        if self.repos:
            self.timer2 += 1
            if self.timer2 == 40:
                self.timer2 = 0
                self.repos = False

        # Boucle qui oblige le joueur a terminé son animation si l'animation n'est pas finis
        if self.is_attacking:
            if len(self.images['down_attack']) > self.attack_animation_timer:
                # Si il attaque en bas
                if direction == 'down':
                    self.image = self.images['down_attack'][self.attack_animation_timer]
                    self.update_masks('down_attack',self.attack_animation_timer)
                    self.action = 'down_attack'
                # Si il attaque à droite
                if direction == 'right':
                    self.image = self.images['right_attack'][self.attack_animation_timer]
                    self.update_masks('right_attack',self.attack_animation_timer)
                    self.action = 'right_attack'
                # Si il attaque à gauche
                if direction == 'left':
                    self.image = self.images['left_attack'][self.attack_animation_timer]
                    self.update_masks('left_attack',self.attack_animation_timer)
                    self.action = 'left_attack'
                # Si il attaque en haut
                if direction == 'up':
                    self.image = self.images['up_attack'][self.attack_animation_timer]
                    self.update_masks('up_attack',self.attack_animation_timer)
                    self.action = 'up_attack'
                # Compteur temps de l'animation
                self.attack_animation_counter += 1
                # Change l'étape de l'animation et ralentie l'animation
                if self.attack_animation_counter % self.attack_animation_rate == 0:
                    self.attack_animation_timer += 1
            # Si animation fini
            else:
                # Reset des variables
                self.is_attacking = False

    """ Méthode replaçant le joueur à sa position précédente lorsqu'il entre en collision avec un objet """

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    """ Méthode découpant le .png du joueur, pour utiliser chaque sprite correspondant à l'action en cours """

    def get_image(self,x,y,sprite):
        image = pygame.Surface([48,48], pygame.SRCALPHA)
        image.blit(sprite,(0,0),(x,y,48,48))
        return image

    """ Méthode de mise à jour du niveau du joueur lorsqu'il dépasse un seuil d'exp (seuil affiché au joueur pour qu'il sache combien d'exp il lui faut pour level up) avec un son de level UP """

    def maj_niveau(self):
        if self.exp >= self.niveaux_exp[self.niveau - 1]:
            levelup = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'ambient_sounds/levelup.wav'))
            self.exp =  self.exp - self.niveaux_exp[self.niveau - 1]
            self.niveau += 1
            pygame.mixer.Sound.play(levelup).set_volume(0.7)
            self.attaque += 1
        return (self.niveau,self.niveaux_exp[self.niveau-1])
    
    """ Méthode qui change le mask à utilisé en cohérence avec les actions du joueur """

    def type_mask(self):
        if self.is_attacking:
            self.update_masks(self.action,self.attack_animation_timer-1)
        else:
            self.update_masks(self.action,self.animation_timer-1)

    """ Méthode qui mets à jour le mask à utilisé """

    def update_masks(self,direction,num):
        if self.mask_deplacement:
            self.mask = pygame.mask.from_surface(self.images_mask[direction][num])
        else:
            self.mask = pygame.mask.from_surface(self.images_mask_attaque[direction][num])
        self.rect = self.image.get_rect(center=self.rect.center)