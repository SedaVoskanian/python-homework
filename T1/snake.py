"""T1 – Snake procédural : le code de départ (étape 1).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lancez-le avec :  uv run snake.py
Testez-le avec :  uv run pytest
"""

from random import randint
import random
import pygame as pg

# Le plateau : X × Y cases de W × H pixels (étape 3).
X, Y = 30, 30
W, H = 20, 20


UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)


# --- logique du jeu : aucune fonction ici ne dessine -------------------------
# Ces fonctions sont vérifiées par les tests (tests/test_snake.py) :
# gardez leur nom et leurs paramètres.


def in_scope(tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    if 0<=tile[0]<X and 0<tile[1]<Y:
        return True
    else:
        return False


def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    return (snake[-1][0]+direction[0],snake[-1][1]+direction[1])

KEYS={pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT}
def turn(direction, key):
    """La nouvelle direction après l'appui sur la touche `key` (ex. pg.K_UP)."""
    nv=direction
    if key==pg.K_UP:
        nv=UP
    elif key==pg.K_DOWN:
        nv=DOWN
    elif key==pg.K_LEFT:
        nv=LEFT
    elif key==pg.K_RIGHT:
        nv=RIGHT
    #bloque demi-tour
    if (nv[0]+direction[0]==0) and (nv[1]+direction[1]==0):
        return direction
    return nv


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    head=next_head(snake,direction)
    #vérifie que l'on reste sur le plateau
    if in_scope(head)==False:
        return "out-of-board" 
    #vérifie si y a eu self bite
    if head in snake[1:]:
        return "self-bite"
    #fait avancer la tête
    snake.append(head)
    #cas où le serpent mange le fruit
    if head==fruit :
        return "ate"
    #déplacement (on enlève la queue)
    snake.pop(0)
    return "moved"
    
    raise NotImplementedError("étapes 5, 7 et 8")


def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    x=random.randint(0,X-1)
    y=random.randint(0,Y-1)
    while (x,y) in snake :
        x=random.randint(0,X-1)
        y=random.randint(0,Y-1)
    return (x,y)



# --- la boucle de jeu --------------------------------------------------------

def main():
    pg.init()
    screen=pg.display.set_mode((X*W,Y*H))
    clock = pg.time.Clock()
    snake = [(10, 15), (11, 15), (12, 15)]
    direction=(1,0)
    fruit=random_fruit(snake)
    running=True
    while running:
        # au plus 1 image par seconde
        clock.tick(6) #si remplace 1 par 10 on aura 10 images par secondes
        
        pg.display.set_caption(f"score:{len(snake)}")
        # 1. les événements : il faut les lire, sinon la fenêtre ne répond pas
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q): #vérifie si a coché la croix rouge ou a appuyé sur la touche Echap
                running =False
            #changement de direction
            elif event.type==pg.KEYDOWN and event.key in KEYS: #vérifie si une touche du clavier qui fait partie de l'ensemble KEYS a été enfoncé
                direction=turn(direction,event.key)
        # 2. l'état (rien pour l'instant)
        outcome=move(snake,direction,fruit)
        if outcome=="ate":
            fruit=random_fruit(snake)
        elif outcome =="out-of-board" or outcome=="self-bite":
            running =False

        # 3. l'affichage du damier
        for i in range(X):
                for j in range(Y):
                    # Calcule la position en pixels de la case actuelle
                    x = j * W
                    y = i * H
                    if (i+j)%2 == 0 :
                        couleur= (255,255,255)
                    else:
                        couleur= (210,210,210)
                    rect = pg.Rect(x, y, W, H)
                    pg.draw.rect(screen, couleur, rect)
        # 4. l'affichage du serpent
        for i in snake:
            rect_snake=pg.Rect(i[0]*W,i[1]*H,W,H)
            pg.draw.rect(screen, (255,0,0), rect_snake)

        # 5. l'affichage du fruit
        rect_fruit=pg.Rect(fruit[0]*W,fruit[1]*H,W,H)
        pg.draw.rect(screen,(34,139,34),rect_fruit)
        # ... puis on l'envoie à l'écran, une seule fois par tour de boucle
        pg.display.update() #ca affiche la mise à jour de l'écran
    print(f"Game over. score final:{len(snake)}")
pg.quit()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run snake.py),
# pas quand un autre fichier fait `import snake` (les tests, par ex.).
if __name__ == "__main__":
    main()
