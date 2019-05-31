"""Exemple de gestion des événements claviers avec python et pygame.

Cet exemple est une adaptation libre refactorisée du code trouvé dans le cours:
https://bit.ly/2KfhS8T
"""

# Importation des bibliothèques nécessaires
import pygame as pg

from config import colors, sprites, settings


class Game:
    """Représente le jeu lui-même."""

    def __init__(self):
        """Initialise l'objet principal du jeu."""
        # Initialisation de la bibliothèque Pygame
        pg.init()

        # Création de l'écran principal
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))

        # Chargement et collage du fond
        self.background = pg.image.load(sprites.BACKGROUND).convert()
        self.screen.blit(self.background, (0, 0))

        # Chargement et collage du personnage
        self.mushroom = pg.image.load(sprites.MUSHROOM).convert_alpha()
        self.mushroom_rect = self.mushroom.get_rect()
        self.screen.blit(self.mushroom, self.mushroom_rect)

        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

        # Permet de laisser une touche du clavier enfoncée lors des mouvements
        pg.key.set_repeat(400, 30)

        # On termine cette méthode d'initialisation par une mise à jour de 
        # l'écran principal
        pg.display.update()

    def start(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        # Boucle principale du jeu
        while self.running:
            # On regarde quels sont les événements dans la file d'attente
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # Si l'utilisateur a clické sur la croix de fermeture de 
                    # la fenêtre: mettre self.running à False pour quitter
                    # l'application
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        # Si l'utilisateur appuie sur la flèche du bas, le
                        # champignon se déplace vers le bas
                        self.mushroom_rect.move_ip(0, 3)

            # Afficher le fond, puis le champignon
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.mushroom, self.mushroom_position)
            # Mettre à jour l'affichage
            pg.display.update()


def main():
    """Point d'entrée principal du jeu."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
