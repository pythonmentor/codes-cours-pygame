"""Exemple simple de création d'une fenêtre avec python et pygame.

Cet exemple est une adaptation libre refactorisée du code trouvé dans le cours:
https://bit.ly/2EEmtxR
"""

# Importation des bibliothèques nécessaires
import pygame as pg

from ..config import settings


class Game:
    """Représente le jeu lui-même."""

    def __init__(self):
        """Initialise l'objet principal du jeu."""
        # Initialisation de la bibliothèque Pygame
        pg.init()

        # Création de l'écran principal
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))

        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

    def start(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        print("To quit the game: press CTRL-C")
        # Boucle principale du jeu
        while self.running:
            pass


def main():
    """Point d'entrée principal du jeu."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
