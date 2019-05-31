"""La gestion du personnage champignon peut être externalisée dans une classe
séparée qui hérite de pg.sprite.Sprite.
"""
 
 # Importation des bibliothèques nécessaires
import pygame as pg

from config import sprites, settings


class Mushroom(pg.sprite.Sprite):
    """Représente le personnage principal du jeu."""

    def __init__(self):
        """Initialise la sprite Mushroom."""
        # On appelle la classe mère pour initialiser la sprite
        super().__init__()
        # L'image représentant le champignon est stockée dans l'attribut 
        # image et sa position dans l'attribut rect.
        self.image = pg.image.load(sprites.MUSHROOM).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        """Met à jour la sprite en fonction des événements."""
        pressed = self.get_pressed_keys()

        for key in pressed:
            if hasattr(self, key): 
                getattr(self, key)()  

    def up(self):
        """Déplace le personnage vers le haut."""
        if self.rect.top > 0:
            self.rect.move_ip(0, -settings.VELOCITY)

    def down(self):
        """Déplace le personnage vers le bas."""
        if self.rect.bottom < settings.HEIGHT:
            self.rect.move_ip(0, settings.VELOCITY)

    def right(self):
        """Déplace le personnage vers la droite."""
        if self.rect.right < settings.WIDTH:
            self.rect.move_ip(settings.VELOCITY, 0)

    def left(self):
        """Déplace le personnage vers la gauche."""
        if self.rect.left > 0:
            self.rect.move_ip(-settings.VELOCITY, 0)

    def get_pressed_keys(self):
        """Retourne les noms des touches pressées par l'utilisateur."""
        return [
            pg.key.name(key).lower() 
            for key, pressed in enumerate(pg.key.get_pressed())
            if pressed
        ]


class Game:
    """Représente le jeu lui-même."""

    def __init__(self):
        """Initialise l'objet principal du jeu."""
        # Initialisation de la bibliothèque Pygame
        pg.init()

        # Création de l'écran principal
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption("Mushrooms paradise")

        # Chargement et collage du fond
        self.background = pg.image.load(sprites.BACKGROUND).convert()
        self.screen.blit(self.background, (0, 0))

        # Groupe contenant les sprites de notre jeu
        self.sprites = pg.sprite.RenderUpdates()
        self.sprites.add(Mushroom())

        # Sert à limiter le nombre de frames par sec en limitant la vitesse
        # d'exécution de la boucle principale.
        self.clock = pg.time.Clock()

        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

    def start(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        # Boucle principale du jeu
        while self.running:
            # Limite la vitesse d'exécution de la boucle à 30 frames par sec
            self.clock.tick(30)
            # On efface les sprites avec le fond
            self.sprites.clear(self.screen, self.background)
            # La gestion des événements est confiée à une méthode séparée
            self.process_events()
            # On appelle la méthode de mise à jour des sprites
            self.sprites.update()
            # On redessine les sprites
            updated_sprites = self.sprites.draw(self.screen)
            # Mettre à jour l'affichage avec les sprites qui ont bougé
            pg.display.update(updated_sprites)

    def process_events(self):
        """Traite les événements présents dans la file d'attente de pygame."""
        # On regarde quels sont les événements dans la file d'attente
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Si l'utilisateur a clické sur la croix de fermeture de 
                # la fenêtre: mettre self.running à False pour quitter
                # l'application
                self.running = False


def main():
    """Point d'entrée principal du jeu."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
