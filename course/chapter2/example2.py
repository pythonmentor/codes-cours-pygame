"""Exemple de création d'une fenêtre avec une image en fond avec python et 
pygame.

Cet exemple est une adaptation libre refactorisée du code trouvé dans le cours:
https://bit.ly/2EEmtxR
"""

# Importation des bibliothèques nécessaires
import pygame as pg

from config import sprites, settings

class Game:
    """Représente le jeu lui-même."""

    def __init__(self):
        """Initialise l'objet principal du jeu."""
        # Initialisation de la bibliothèque Pygame
        pg.init()

        # Création de l'écran principal de taille 640px x 480px
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))

        # Chargement et collage du fond
        self.background = pg.image.load(sprites.BACKGROUND).convert()
        self.screen.blit(self.background, (0, 0))

        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

        # On termine cette méthode d'initialisation par une mise à jour de 
        # l'écran principal
        pg.display.update()

    def start(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        # Boucle principale du jeu
        while self.running:
            # Tant qu'on ne travaille pas avec les événements, appeller cette
            # fonction pour permettre à pygame de les gérer en interne.
            pg.event.pump()

            # Pour le moment, on utilise le terminal pour demander à
            # l'utilisateur s'il désire quitter l'application
            response = input("Enter quit to leave the game? ").lower()
            if response == "quit":
                self.running = False


def main():
    """Point d'entrée principal du jeu."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
