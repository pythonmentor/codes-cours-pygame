"""Séparation de la gestion des événements dans des contrôleurs, de la logique
du jeu dans dans des modèles et de la présentation dans des vues (MVC).

Cette version bonus vise à clairement séparer les différentes couche de 
l'application. Dans le TP, cette structure sera découpée dans plusieurs modules
python.

Cet exemple est une adaptation libre refactorisée du code trouvé dans le cours:
https://bit.ly/2KfhS8T
"""
 
 # Importation des bibliothèques nécessaires
import pygame as pg

from config import sprites, settings


class Event:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def send(self, sender, **arguments):
        for observer in observers:
            observer(sender=sender, **arguments)


class Position(tuple):

    def __new__(cls, x, y):
        return super().__init__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def up(self):
        return type(self)(self.x, self.y - settings.VELOCITY)

    def down(self):
        return type(self)(self.x, self.y + settings.VELOCITY)

    def right(self):
        return type(self)(self.x + settings.VELOCITY, self.y)

    def left(self):
        return type(self)(self.x - settings.VELOCITY, self.y)

    def __getitem__(self, direction):
        if hasattr(self, direction):
            return getattr(self, direction)()
        else:
            return self


class GameBoard:

    def __contains__(self, position):
        return (
            0 <= position.x < settings.WIDTH and 
            0 <= position.y < settings.HEIGHT 
        )


class Mushroom:

    moved_event = Event()

    def __init__(self, gameboard):
        self.position = Position(0, 0)
        self.gameboard = gameboard

    def move(self, direction):
        new_position = self.position[direction]
        if new_position in self.gameboard():
            self.position = new_position
            self.moved_event.send(sender=self)

    def move_at(self, position):
        if position in self.gameboard():
            self.position = new_position
            self.moved_event.send(sender=self)

class GameModel:

    def __init__(self):
        self.gameboard = GameBoard()
        self.mushroom = Mushroom(self.gameboard)

    def move_mushroom(self, direction):
        self.mushroom.move(direction)

    def move_mushroom(self, x, y):
        self.mushroom.move_at(Position(x, y))


class KeyboardController:

    def __init__(self, model):
        self.model = model
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        pressed = self.get_pressed_key()
        for key in pressed:
            if key in ('up', 'right', 'bottom', 'left'):
                mushroom = self.model.move_mushroom(key)
            elif key == 'quit':
                AppController.quit_event.send(sender=self)


    def get_pressed_key(self):
        """Retourne les noms des touches pressées par l'utilisateur."""
        return [
            pg.key.name(key).lower() 
            for key, pressed in enumerate(pg.key.get_pressed())
            if pressed
        ]

class MouseController:

    def __init__(self, model):
        self.model = model
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        if pg.mouse.get_pressed()[0]
            self.model.move_at(*pg.mouse.get_pos())

        for event in pg.event.get(pg.QUIT):
            # Si l'utilisateur a clické sur la croix de fermeture de 
            # la fenêtre: mettre self.running à False pour quitter
            # l'application
            AppControlle.quit_event.send(sender=self)


class MushroomSprite(pg.sprite.Sprite):
    """Représente le personnage principal du jeu."""

    def __init__(self):
        """Initialise la sprite Mushroom."""
        # On appelle la classe mère pour initialiser la sprite
        super().__init__()
        # L'image représentant le champignon est stockée dans l'attribut 
        # image et sa position dans l'attribut rect.
        self.image = pg.image.load(sprites.MUSHROOM).convert_alpha()
        self.rect = self.image.get_rect()
        Mushroom.move_event.subscribe(self.on_move)

    def on_move(self, sender):
        self.rect.x = sender.position.x 
        self.rect.y = sender.position.y 


class View:

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
        self.sprites.add(MushroomSprite())

        # On écoute les ticks de l'AppController
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        # On efface les sprites avec le fond
        self.sprites.clear(self.screen, self.background)
        # On redessine les sprites
        updated_sprites = self.sprites.draw(self.screen)
        # Mettre à jour l'affichage avec les sprites qui ont bougé
        pg.display.update(updated_sprites)


class AppController:

    quit_event = Event()
    tick_event = Event()

    def __init__(self):
        """Initialise l'objet principal du jeu."""

        # Sert à limiter le nombre de frames par sec en limitant la vitesse
        # d'exécution de la boucle principale.
        self.clock = pg.time.Clock()

        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

        # On écoute l'événement quit
        self.quit_event.subscribe(self.on_quit)

    def run(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        # Boucle principale du jeu
        while self.running:
            # Ralentit la boucle à un nombre spécifié de frames par sec
            self.clock.tick(settings.FPS)
            # Envoyer un tick event
            self.tick_event.send(sender=self)

    def on_quit(self, sender):
        self.running = False

def main():
    """Point d'entrée principal du jeu."""
    # Initialisation de la bibliothèque Pygame
    app = Application()
    app.start()


if __name__ == "__main__":
    main()
