import pygame
pygame.init()

FRAMERATE=33
TICK_DELAY=int(1000 / FRAMERATE)
Black = 0,0,0
Red = 255,255,255
Red = 255,0,0
Blue = 0,0,255
Orange = 255,165,0


class Screen(object):
    WIDTH = 1080
    HEIGHT = 600
    pygame.display.set_caption("Table tennis")

class TableTennis(object):
    def __init__(self):
        # abstraction: table
        self.win = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        # abstraction: the instance of a Player, that we call player one
        player_one = Player(facing = +1, initial_x= Screen.WIDTH/4, initial_y=Screen.HEIGHT/2, color=Red, keys=(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
        # abstraction: the instance of a Player, that we call player two
        player_two = Player(facing = -1, initial_x = (Screen.WIDTH/4) * 3, initial_y=Screen.HEIGHT/2, color=Blue, keys=(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
        # instance of Ball
        self.ball = Ball(initial_x = Screen.WIDTH/2, initial_y = Screen.HEIGHT/2, color = Orange)
        #instance of player 1's goal
        goal1 = Goal(initial_x = 0 - Ball.WIDTH, initial_y = 0, color = Black, facing = -1)
        #instance of player 2's goal
        goal2 = Goal(initial_x = Screen.WIDTH + Ball.WIDTH, initial_y = 0, color = Black, facing = +1)
        # instance of wall
        wall1 = Wall(y = 0)
        #instance of wall
        wall2 = Wall(y = Screen.HEIGHT - Wall.WIDTH)
        #instance of net
        net = Net()
        self.game_objects = [ player_one, player_two, self.ball, goal1, goal2, wall1, wall2, net ]
        
        self.input_receivers = [ game_object for game_object in self.game_objects if hasattr(game_object, "handle_input") ]
        self.drawables = [ game_object for game_object in self.game_objects if hasattr(game_object, "draw") ]
        self.tickables = [ game_object for game_object in self.game_objects if hasattr(game_object, "tick") ]
        self.collidables = [ game_object for game_object in self.game_objects if hasattr(game_object, "collision")]
    # abstraction: game loop
    def game_loop(self):
        run = True
        while run:

            # abstraction: tick rate
            pygame.time.delay(TICK_DELAY)

            # abstraction: command, quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            for i in self.input_receivers:
                i.handle_input(keys)    

            # abstraction: draw entire scene 

            # abstraction: draw, clear screen after movement
            self.win.fill(Black)
            # colors screen black to remove movement after effect

            for d in self.drawables:
                d.draw(self.win)

            for t in self.tickables:
                t.tick()
        
            for c in self.collidables:
                c.collision(self.ball)
            # abstraction: update the actual display
            pygame.display.update() 

class Net(object):
    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (Screen.WIDTH/2, 0, 10, Screen.HEIGHT))

# the concept of a ball
class Ball(object):
    WIDTH = 30
    HEIGHT = 30
    SPEED_X = 10
    SPEED_Y = 0
    def __init__(self, initial_x, initial_y, color):
        """this initialieses the ball and tells it how to start"""
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.serve_direction = +1
        Ball.SPEED_X = 10
        Ball.SPEED_Y = 0
        
    
    def tick(self):
        """this handles the movement"""
        self.x += Ball.SPEED_X
        self.y += Ball.SPEED_Y

    def hit_wall(self):
        """this tells the ball what to do when it hits a wall"""
        Ball.SPEED_Y = Ball.SPEED_Y * -1

    def hit_paddle(self, facing):
        """handles what happens when the ball hits a player"""
        Ball.SPEED_X = facing * abs(Ball.SPEED_X)
        if Ball.SPEED_Y == 0:
            Ball.SPEED_Y = 10

    def draw(self, win):
        """draws the ball"""
        pygame.draw.rect(win, self.color, (self.x, self.y, Ball.WIDTH, Ball.HEIGHT))

    def ballpointA(self):
        """upper left corner"""
        point_A_location = (self.x, self.y)
        return point_A_location

    def ballpointB(self):
        """upper right corner"""
        point_B_location = ((self.x + Ball.WIDTH), self.y)
        return point_B_location

    def ballpointC(self):
        """lower right corner"""
        point_C_location = ((self.x + Ball.WIDTH), (self.y + Ball.HEIGHT))
        return point_C_location

    def ballpointD(self):
        """lower left corner"""
        point_D_location = (self.x, (self.y + Ball.HEIGHT))
        return point_D_location

    def ball_reset(self,facing):
        """when this function is called it will reset the ball to it's start"""
        self.x = self.initial_x
        self.y = self.initial_y
        Ball.SPEED_Y = 0
        self.serve_direction = facing
        Ball.SPEED_X = 10 * self.serve_direction

    def get_collision_points(self):
        """all the corners are used in figuring out if the ball hit's anything"""
        return [self.ballpointA(), self.ballpointB(), self.ballpointC(), self.ballpointD()]

# abstraction: the concept of a player
class Player(object):
    WIDTH = 50
    HEIGHT = 50
    SPEED = 11
    def __init__(self, facing, initial_x, initial_y, color, keys):
        """this initialises the players"""
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.key_left, self.key_right, self.key_up, self.key_down = keys
        self.facing = facing

    def handle_input(self, keys):
        """this handles player controls"""
        if keys[self.key_left]:
            self.x -= Player.SPEED

        if keys[self.key_right]:
            self.x += Player.SPEED

        if keys[self.key_up]:
            self.y -= Player.SPEED

        if keys[self.key_down]:
            self.y += Player.SPEED

    def draw(self, win):
        """this draws the player"""
        pygame.draw.rect(win, self.color, (self.x, self.y, Player.WIDTH, Player.HEIGHT))

    def collision(self,collidable):
        """this handles player and ball collisions"""
        for x, y in collidable.get_collision_points():    
            if x >= self.x and x <= self.x + Player.WIDTH and y >= self.y and y <= self.y + Player.HEIGHT:
                collidable.hit_paddle(self.facing)
                return

# a goal
class Goal(object):
    WIDTH = 10
    def __init__(self, initial_x, initial_y, color, facing):
        """this initialises the goal class"""
        self.x = initial_x
        self.y = initial_y
        self.color = color
        self.facing = facing

    def draw(self, win):
        """this draws the goals"""
        pygame.draw.rect(win, self.color, (self.x, self.y, Goal.WIDTH, Screen.HEIGHT))

    def collision(self, collidable):
        """this tells the ball what to do when it hits a goal"""
        for x, y in collidable.get_collision_points():    
            if x  == self.x:
                collidable.ball_reset(self.facing)
                return

class Wall(object):
    LENGTH = Screen.WIDTH
    WIDTH = 10
    """this initialises the walls"""
    def __init__(self, y):
        self.y = y
    
    def draw(self, win):
        """this draws the walls"""
        pygame.draw.rect(win, (255,255,255), (0, self.y, Wall.LENGTH, Wall.WIDTH))

    def collision(self, collidable):
        """this tells the ball what to do when it hits a wall"""
        for point in collidable.get_collision_points():    
            x, y = point
            if y  == self.y:
                collidable.hit_wall()
                return

game = TableTennis()
game.game_loop()
pygame.quit()
