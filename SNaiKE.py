import random
from collections import namedtuple
import pygame
import tensorflow
from Text_button import textbutton
from qtrainer import qtrainer
Point = namedtuple("Point","x, y")
win_x = 480
win_y = 480
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255,255,0)
pygame.init()
pygame.display.set_caption("snaker")
win = pygame.display.set_mode((win_x,win_y))
fps = pygame.time.Clock()
quit = False
font = pygame.font.SysFont("comic sans ms", 24 )
gameovertext = font.render("Gaime over", True, red)
rectange = gameovertext.get_rect()
rectange.center = ( win_x / 2 , win_y / 2)



def placefruit():
    global fruit
    fruit = Point(random.randrange(1, win_x // 30) * 30, random.randrange(1, win_y // 30) * 30)


def retry():
    global gameover,snake,body,fruit,dur,refruit
    dur = "NORTH"
    placefruit()
    refruit = False
    gameover = False
    body = [Point(win_x / 2, win_y / 2)]
    snake = Point(win_x / 2, win_y / 2)

def step():
    global snake, body, refruit, gameover
    x = snake.x
    y = snake.y
    if dur == "NORTH":
        y -= 30
    if dur == "SOUTH":
        y += 30
    if dur == "EAST":
        x += 30
    if dur == "WEST":
        x -= 30
    snake = Point(x, y)
    if snake == fruit:
        refruit = True
    else:
        body.pop()
    if refruit:
        placefruit()
        refruit = False

    body.insert(0, snake)

    gameover = colision(snake)

playagainbutton = textbutton(win_x/2 , win_y/2 +40,200 ,50,"retry?",onclick=retry)
retry()

def colision(point):
    if (point.x == 480) or (point.x < 0) or (point.y == 480) or (point.y < 0):
        return True
    for part in body[1:6]:
        if point == part:
            return True
    return False

def linearqnet(inputsize,hiddenlay,outputsize):
    inputs = tensorflow.keras.layers.Input(shape = inputsize,name = "input")
    layer1 = tensorflow.keras.layers.Dense(hiddenlay,activation = "relu",name = "dense1")(inputs)
    action = tensorflow.keras.layers.Dense(outputsize, name= "dense2")(layer1)
    return tensorflow.keras.Model(inputs=inputs,outputs=action)



def getgamestate():
    gamestate = [
        colision(Point(snake.x, snake.y - 30)),
        colision(Point(snake.x, snake.y + 30)),
        colision(Point(snake.x - 30, snake.y)),
        colision(Point(snake.x + 30, snake.y)),
        (Point(snake.x, snake.y - 30)) == fruit,
        (Point(snake.x, snake.y + 30)) == fruit,
        (Point(snake.x - 30, snake.y)) == fruit,
        (Point(snake.x + 30, snake.y)) == fruit,
        fruit.y < snake.y,
        fruit.y > snake.y,
        fruit.x < snake.x,
        fruit.x > snake.x,
    ]
    return gamestate

def makedec(gamestate):
    global dur
    randdur = random.randint(1,4)
    if randdur == 1:
        dur = "NORTH"
    if randdur == 2:
        dur = "WEST"
    if randdur == 3:
        dur = "SOUTH"
    if randdur == 4:
        dur = "EAST"


while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dur = "NORTH"
            if event.key == pygame.K_s:
                dur = "SOUTH"
            if event.key == pygame.K_a:
                dur = "WEST"
            if event.key == pygame.K_d:
                dur = "EAST"
    if not gameover:
        gamestate = getgamestate()
        makedec(gamestate)
        step()

    win.fill(black)


    for i in range(len(body)):

        pygame.draw.rect(win,green,pygame.Rect(body[i].x,body[i].y,30,30))

    pygame.draw.rect(win,red,pygame.Rect(fruit.x,fruit.y,30,30) )
    if gameover:
        win.blit(gameovertext, rectange)
        playagainbutton.update(win)
    pygame.display.update()
    fps.tick(10)
pygame.quit()
print("Closed.")
