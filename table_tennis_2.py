import pygame
pygame.init()

# abstraction: table
win = pygame.display.set_mode((1080,600))
pygame.display.set_caption("Table tennis")

# abstraction: paddle and ball velocity
velocity = 10

# abstraction: paddle size
width = 50
height = 50

# the concept of a ball
class Ball(object):

    def __init__(self, initial_x, initial_y, color):
        self.x = initial_x
        self.y = initial_y
        self.color = color

    def tick(self):
        self.x -= velocity

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, 30, 30))

# abstraction: the concept of a player
class Player(object):

    def __init__(self, initial_x, initial_y, color, keys):
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.key_left, self.key_right, self.key_up, self.key_down = keys

    def handle_input(self, keys):
        if keys[self.key_left]:
            self.x -= velocity

        if keys[self.key_right]:
            self.x += velocity

        if keys[self.key_up]:
            self.y -= velocity

        if keys[self.key_down]:
            self.y += velocity

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, width, height))

# abstraction: the instance of a Player, that we call player one
player_one = Player(initial_x=270, initial_y=300, color=(255,0,0), keys=(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))

# abstraction: the instance of a Player, that we call player two
player_two = Player(initial_x=810, initial_y=300, color=(0,0,255), keys=(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
# instance of Ball
ball = Ball(initial_x = 540, initial_y = 300, color = (255,165,0))

game_objects = [ player_one, player_two, ball ]
input_receivers = [ game_object for game_object in game_objects if hasattr(game_object, "handle_input") ]
drawables = [ game_object for game_object in game_objects if hasattr(game_object, "draw") ]
tickables = [ game_object for game_object in game_objects if hasattr(game_object, "tick") ]

# abstraction: game loop
run = True
while run:
    # abstraction: tick rate
    pygame.time.delay(30)

    # abstraction: command, quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    for i in input_receivers:
        i.handle_input(keys)    

    for t in tickables:
        t.tick()

    # abstraction: draw entire scene 

    # abstraction: draw, clear screen after movement
    win.fill((0,0,0))
    # colors screen black to remove movement after effect

    # abstraction: line/net
    pygame.draw.rect(win, (255,255,255), (540, 0, 10, 600))
    pygame.draw.rect(win, (255,255,255), (0, 0, 1080, 10))
    pygame.draw.rect(win, (255,255,255), (0, 590, 1080, 10))

    for d in drawables:
        d.draw()

    # abstraction: update the actual display
    pygame.display.update() 

pygame.quit()