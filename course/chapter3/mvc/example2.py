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
    """Représente un événement simple auquel on peut s'inscrire
    pour recevoir des notifications.
    """

    def __init__(self):
        """Initialise l'événement avec une liste vide d'observeurs."""
        self.observers = []

    def subscribe(self, observer):
        """Inscrit une fonction ou une méthode receveuse de 
        notifications.
        """
        self.observers.append(observer)

    def send(self, sender, **arguments):
        """Envoie une notification aux observateurs inscrits."""
        for observer in observers:
            observer(sender=sender, **arguments)


class Position(tuple):
    """Objet représentant une position sur un espace de jeu dont
    les coordonnées sont exprimées en pixels.
    
    Les positions étant dans pygame exprimée par des tuples, on
    décide d'hériter d'un tuple.
    """

    def __new__(cls, x, y):
        """Constructeur.

        Comme le tuple est un objet immutable, nous devons 
        surcharger son constructeur __new__.

        """
        return super().__init__(cls, (x, y))

    @property
    def x(self):
        """Abscisse du système de coordonnée représentant
        la position sur le plateau de jeu.

        L'abscisse de 0 représente le bord gauche du plateau
        de jeu.
 
        """
        return self[0]

    @property
    def y(self):
        """Ordonnée du système de coordonnée représentant
        la position sur le plateau de jeu.

        L'ordonnée de 0 représente le bord supérieur du plateau
        de jeu.

        """
        return self[1]

    def up(self):
        """Retourne la position adjacente au dessus."""
        return type(self)(self.x, self.y - settings.VELOCITY)

    def down(self):
        """Retourne la position adjacente au dessous."""
        return type(self)(self.x, self.y + settings.VELOCITY)

    def right(self):
        """ Retourne la position adjacente à droite."""
        return type(self)(self.x + settings.VELOCITY, self.y)

    def left(self):
        """Retourne la position adjacente à gauche."""
        return type(self)(self.x - settings.VELOCITY, self.y)

    def __getitem__(self, direction):
        """Retourne une position adjacente lorsque la
        position (up, down, left, right) est exprimée
        sous forme de chaine.
        
        """
        if hasattr(self, direction):
            return getattr(self, direction)()
        else:
            return self


class GameBoard:
    """Modèle représentant le plateau de jeu."""

    def __contains__(self, position):
        """Test si une position est à l'intérieur de la
        surface de jeu à l'aide de l'opérateur in.

        """
        if hasattr(position, "x") and hasattr(position, "y"):
            return (
                0 <= position.x < settings.WIDTH - settings.VELOCITY and 
                0 <= position.y < settings.HEIGHT - settings.VELOCITY
            )
        return False


class Mushroom:
    """Modèle représentant le personnage principal du 
    plateau de jeu.

    """

    # Evénement envoyé lorsque le personnage s'est déplacé
    moved_event = Event()

    def __init__(self, gameboard):
        """Initialise du personnage."""
        self.position = Position(0, 0)
        self.gameboard = gameboard

    def move(self, direction):
        """Déplace le personnage dans une direction donnée."""
        new_position = self.position[direction]
        if new_position in self.gameboard():
            self.position = new_position
            self.moved_event.send(sender=self)

    def move_at(self, position):
        """Déplace le personnage à une position donnée."""
        if position in self.gameboard():
            self.position = new_position
            self.moved_event.send(sender=self)

class GameModel:
    """Modèle représentant le jeu lui-même. Point d'entrée
    des modèles de l'application.

    """

    def __init__(self):
        """Initialise le modèle du jeu."""
        self.gameboard = GameBoard()
        self.mushroom = Mushroom(self.gameboard)

    def move_mushroom(self, direction):
        """Demande au personnage principal de se déplacer dans
        une direction donnée.
        
        """
        self.mushroom.move(direction)

    def move_mushroom(self, x, y):
        """Demande au personnage principal de se déplacer à une
        position x, y donnée.
    
        """
        self.mushroom.move_at(Position(x, y))


class KeyboardController:
    """Contrôleur écoutant et gérant les événements du clavier."""

    def __init__(self, model):
        """Initialise le contrôleur du clavier."""
        self.model = model
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        """Gestionnaire exécuté à chaque tick_event envoyé
        par le AppController.
        """
        pressed = self.get_pressed_key()
        for key in pressed:
            if key in ('up', 'right', 'bottom', 'left'):
                mushroom = self.model.move_mushroom(key)


    def get_pressed_key(self):
        """Retourne les noms des touches pressées par l'utilisateur."""
        return [
            pg.key.name(key).lower() 
            for key, pressed in enumerate(pg.key.get_pressed())
            if pressed
        ]

class MouseController:
    """Contrôleur écoutant et gérant les événements de la souris."""

    def __init__(self, model):
        """Initialise le contrôleur de la souris."""
        self.model = model
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        """Gestionnaire exécuté à chaque tick_event envoyé par le
        AppController.
        """
        if pg.mouse.get_pressed()[0]
            self.model.move_at(*pg.mouse.get_pos())

        for event in pg.event.get(pg.QUIT):
            # Si l'utilisateur a clické sur la croix de fermeture de 
            # la fenêtre: mettre self.running à False pour quitter
            # l'application
            AppController.quit_event.send(sender=self)


class MushroomSprite(pg.sprite.Sprite):
    """Sprite représentant le personnage principal du jeu sur l'interface."""

    def __init__(self):
        """Initialise la sprite Mushroom."""
        # On appelle la classe mère pour initialiser la sprite
        super().__init__()
        # L'image représentant le champignon est stockée dans l'attribut 
        # image et sa position dans l'attribut rect.
        self.image = pg.image.load(sprites.MUSHROOM).convert_alpha()
        self.rect = self.image.get_rect()
        # On écoute les moved_event envoyé par le modèle du personnage.
        Mushroom.move_event.subscribe(self.on_moved)

    def on_moved(self, sender):
        """Gestionnaire exécuté à la réception d'un moved_event provenant
        du modèle.
        """
        self.rect.x = sender.position.x 
        self.rect.y = sender.position.y 


class View:
    """Interface graphique du jeu."""

    def __init__(self):
        """Initialise l'interface graphique."""
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

        # Sert à limiter le nombre de frames par sec en limitant la vitesse
        # d'exécution de la boucle principale.
        self.clock = pg.time.Clock()

        # On écoute les ticks de l'AppController
        AppController.tick_event.subscribe(self.on_tick)

    def on_tick(self, sender):
        # Ralentit la boucle à un nombre spécifié de frames par sec
        self.clock.tick(settings.FPS)
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
        # Création d'une variable indiquant si le jeu est en cours
        self.running = False

        # On écoute l'événement quit_event
        self.quit_event.subscribe(self.on_quit)

    def start(self):
        """Démarre la boucle principale du jeu."""
        # Variable qui continue la boucle sa valeur est True. 
        self.running = True

        # Boucle principale du jeu
        while self.running:
            # Envoyer un tick event
            self.tick_event.send(sender=self)

    def on_quit(self, sender):
        """Gestionnaire exécuté à la réception d'un tick_event."""
        self.running = False

def main():
    """Point d'entrée principal du jeu."""
    # Initialisation des modèles, contrôleurs et vues
    game = GameModel()
    keyboard = KeyboardController(game)
    mouse = MouseController(game)
    app = AppController()
    gui = View()

    # Démarrage du jeu
    app.start()


if __name__ == "__main__":
    main()
