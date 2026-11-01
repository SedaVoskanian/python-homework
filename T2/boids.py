"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math
import random
from pathlib import Path

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.ALMOND

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sky.png"  # le décor (étape 9)

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)


# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.



class Boid(arcade.Sprite): #boid appartient à Boid qui est inclu ds Sprite
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, others=None):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed = speed
        self.turning=0

        if others is None:
            self.others = []
        else:
            self.others = others

    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        #conversion de l'angle en rarun ruff cdians
        rad = math.radians(self.angle)
 
        dx,dy=self.separation(self.others)
        self.center_x += self.speed * math.cos(rad)*delta_time + dx #quand je multiplie self.speed * math.cos(rad) par delta_time, mes boids ne bougent plus
        self.center_y += -self.speed * math.sin(rad)*delta_time + dy

        #reapparition des boids
        self.center_x = self.center_x%WIDTH
        self.center_y = self.center_y%HEIGHT

        #rotation
        self.angle += self.turning * TURN_SPEED * delta_time
        bruit = random.uniform(-NOISE, NOISE)
        self.angle += bruit

        #boid transparent s'il a au moins un voisin
        voisins=self.neighbours(self.others)
        if len(voisins)>0:
            self.alpha=127 #à moitié transparent
        else:
            self.alpha=255 #opaque
                

    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        liste_voisins=[]
        for other in others:
            if other is not self : #si le boid n'est pas lui=même
                #calcul de la distance entre les deux sprites
                distance=math.dist(self.position, other.position)
                if distance < radius :
                    liste_voisins.append(other)
        return liste_voisins
    
    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        dx = 0.0
        dy = 0.0
        if others is None:
            others = self.others
        for other in others:
            if other is not self:
                d = math.dist(self.position, other.position)
                if d < radius and d > 0:  # d > 0 évite une division par zéro si deux boids sont superposés
                    # distance entre o et b
                    ob_x = (self.center_x - other.center_x)
                    ob_y = (self.center_y - other.center_y)
                    delta = 1/2 * (1 - (d / radius))
                    #On fait la somme de ces déplacements 
                    dx += ob_x * delta
                    dy += ob_y * delta
                    
        return (dx,dy)


class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""

    def __init__(self, x, y):
        super().__init__(OBSTACLE, center_x=x, center_y=y)

def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    liste_boids=[]
    for i in range (n):
        x=random.uniform(0,WIDTH)
        y=random.uniform(0,HEIGHT)
        angle=random.randint(0,360)
        nv_boid=Boid(x,y,angle,others=others)
        liste_boids.append(nv_boid)
    return liste_boids



def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    liste_obstacles=[]
    for i in range (n):
        for j in range (n):
            x=40 + i*80
            y=40 + j*80
            #on cré notre obstacle
            obstacle=Obstacle(x,y)
            liste_obstacles.append(obstacle)
    return liste_obstacles

# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale

        self.EVERYTHING=[]

        # une SpriteList : une liste de sprites, qu'arcade dessine d'un coup
        #1ere SpriteListe
        self.obstacles=arcade.SpriteList()
        grille=obstacle_grid(GRID)
        self.obstacles.extend(grille)
        self.EVERYTHING.extend(grille)
        #2e SpriteListe
        self.boids = arcade.SpriteList()
        les_boids=random_boids(N_BOIDS,others=self.EVERYTHING)
        self.boids.extend(les_boids)
        self.EVERYTHING.extend(les_boids)
        #3e
        self.sky = arcade.SpriteList()
        sky = arcade.Sprite(SKY, center_x=WIDTH/2, center_y=HEIGHT/2)
        
        #on ajuste la taille de l'image
        sky.width = WIDTH
        sky.height = HEIGHT
        self.sky.append(sky)



    def on_update(self, delta_time):
        self.boids.update(delta_time)
        

    def on_draw(self):
        self.clear()
        self.sky.draw()
        self.obstacles.draw()
        self.boids.draw()



    def on_key_press(self, symbol, modifiers): 
    # symbol vaut arcade.key.LEFT, arcade.key.RIGHT, arcade.key.Q…
    #quand on appuie sur la touche, le boid tourne
        if symbol==arcade.key.LEFT:
            for boid in self.boids:
                boid.turning=-1 #tourne à gauche
        elif symbol==arcade.key.RIGHT:
            for boid in self.boids:
                boid.turning=1
        elif symbol==arcade.key.Q:
            self.close()

    def on_key_release(self, symbol, modifiers):
    #quand on relache la touche, le boid arrête de tourner       
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            for boid in self.boids:
                boid.turning = 0


def main():
    MyWindow() #on cré l'objet MyWindow
    arcade.run() #arcade appelle on_update environ 60 fois par seconde


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
