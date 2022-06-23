import pygame
pygame.init()

# abstraction: table
win = pygame.display.set_mode((1080,600))
pygame.display.set_caption("Table tennis")

# abstraction: paddle velocity
velocity = 11

# abstraction: paddle size
width = 50
height = 50

# the concept of a ball
class Ball(object):

    def __init__(self, initial_x, initial_y, color):
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.serve_direction = +1
        self.velocity_x = 10
        self.velocity_y = 0
    
    def tick(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def hit_wall(self):
        self.velocity_y = self.velocity_y * -1

    def hit_paddle(self, facing):
        self.velocity_x = facing * abs(self.velocity_x)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, 30, 30))

    def ballpointA(self):
        point_A_location = (self.x, self.y)
        return point_A_location

    def ballpointB(self):
        point_B_location = ((self.x + 30), self.y)
        return point_B_location

    def ballpointC(self):
        point_C_location = ((self.x + 30), (self.y + 30))
        return point_C_location

    def ballpointD(self):
        point_D_location = (self.x, (self.y + 30))
        return point_D_location

    def ball_reset(self,facing):
        self.x = self.initial_x
        self.y = self.initial_y
        self.velocity_y = 0
        self.serve_direction = facing
        self.velocity_x = 10 * self.serve_direction

    def get_collision_points(self):
        return [self.ballpointA(), self.ballpointB(), self.ballpointC(), self.ballpointD()]

# abstraction: the concept of a player
class Player(object):

    def __init__(self, facing, initial_x, initial_y, color, keys):
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.key_left, self.key_right, self.key_up, self.key_down = keys
        self.facing = facing

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

    def collision(self,collidable):
        for point in collidable.get_collision_points():    
            x, y = point
            if x > self.x - 1 and x < self.x + 51 and y > self.y -1 and y < self.y +51:
                collidable.hit_paddle(self.facing)
                return

# a goal
class Goal(object):
    def __init__(self, initial_x, initial_y, color, facing):
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.facing = facing

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, 10, 600))

    def collision(self, collidable):
        for point in collidable.get_collision_points():    
            x, y = point
            if x  == self.x:
                collidable.ball_reset(self.facing)
                return

class Wall(object):
    def __init__(self, y):
        self.y = y
    
    def draw(self):
        pygame.draw.rect(win, (255,255,255), (0, self.y, 1080, 10))

    def collision(self, collidable):
        for point in collidable.get_collision_points():    
            x, y = point
            if y  == self.y:
                collidable.hit_wall()
                return
   

                
            

# abstraction: the instance of a Player, that we call player one
player_one = Player(facing = +1, initial_x=270, initial_y=300, color=(255,0,0), keys=(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
# abstraction: the instance of a Player, that we call player two
player_two = Player(facing = -1, initial_x=810, initial_y=300, color=(0,0,255), keys=(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
# instance of Ball
ball = Ball(initial_x = 540, initial_y = 300, color = (255,165,0))
#instance of player 1's goal
goal1 = Goal(initial_x = -30, initial_y = 0, color = (0,0,0), facing = -1)
#instance of player 2's goal
goal2 = Goal(initial_x = 1110, initial_y = 0, color = (0,0,0), facing = +1)
# instance of wall
wall1 = Wall(y = 0)
#instance of wall
wall2 = Wall(y = 590)
game_objects = [ player_one, player_two, ball, goal1, goal2, wall1, wall2 ]
input_receivers = [ game_object for game_object in game_objects if hasattr(game_object, "handle_input") ]
drawables = [ game_object for game_object in game_objects if hasattr(game_object, "draw") ]
tickables = [ game_object for game_object in game_objects if hasattr(game_object, "tick") ]
collidables = [ game_object for game_object in game_objects if hasattr(game_object, "collision")]

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

    # abstraction: draw entire scene 

    # abstraction: draw, clear screen after movement
    win.fill((0,0,0))
    # colors screen black to remove movement after effect

    # abstraction: line/net
    pygame.draw.rect(win, (255,255,255), (540, 0, 10, 600))

    for d in drawables:
        d.draw()

    for t in tickables:
        t.tick()
 
    for c in collidables:
        c.collision(ball)
    # abstraction: update the actual display
    pygame.display.update() 

pygame.quit()