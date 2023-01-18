# Project on Snake Game Using Pygame Module
# Efforts by Sukhman Singh
# Github: https://github.com/Sukhman-01
# LinkedIn: https://www.linkedin.com/in/sukhman-singh-901b131b6/
# Reg No.: 12006129
# Subject: Python Programming (INT213)

# from re import I
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BG_COLOR = (126, 232, 12)
TEXT_COLOR = (255,255,255)
HEIGHT = 520
WIDTH = 1000
FONT_TYPE = 'BarlowCondensed-Bold'
DELAY = 1500
BG_TIME = 0
# begin image is not used still

IMG_START = (r"./assets/images/start.png")
IMG_INSTRUCTION = (r"assets/images/instruction.png")
IMG_MAIN = (r"./assets/images/blue bg.png")
IMG_END = (r"./assets/images/gameover.png")
IMG_SBODY = r"./assets/images/s_body.png"
IMG_SHEAD = r"./assets/images/s_head.png"
IMG_FOOD = r"./assets/images/food.png"
BG_MUSIC = r"./assets/music/bg_music.mp3"



class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen  
        self.block = pygame.image.load(IMG_SBODY).convert()  # method to load an image # r is used for raw string
        self.head = pygame.image.load(IMG_SHEAD)
        # self.x, self.y = 100, 100
        self.x = [SIZE]*length # intialise an empty array of size length
        self.y = [SIZE]*length
        self.direction = "right" # direction at start
        self.head_rotation(180)

    def draw(self):
        # self.parent_screen.fill(BG_COLOR) # background # this will delete the prev. blocks which looks like the block is moving
        for i in range(self.length):
            if i==0:
                self.parent_screen.blit(self.head,(self.x[0], self.y[0]))
            else:
                self.parent_screen.blit(self.block,(self.x[i], self.y[i]))

        pygame.display.flip() # won't show without this
         
    def length_increment(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def head_rotation(self, degree): # fix this issue
        self.head = pygame.transform.rotate(self.head, degree)
        # time.sleep(0.2) 

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def crawl(self):
        for i in range(self.length-1,0,-1): # makes the blocks follow each other
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
            # print("x,y = ",self.x[0], self.y[0]) # show x,y coordinates

        # teleportation logic
        if self.x[0] >= WIDTH:
            self.x[0] = 0 - SIZE
        elif self.x[0] < 0:
            self.x[0] = WIDTH

        if self.y[0] >= HEIGHT:
            self.y[0] = 0 - SIZE
        elif self.y[0] < 0:
            self.y[0] = HEIGHT

        # direction logic
        if self.direction == "up":
            self.y[0] -= SIZE

        if self.direction == "down":
            self.y[0] += SIZE 
            
        if self.direction == "left":
            self.x[0] -= SIZE
        
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()

class food:
    def __init__(self, parent_screen):
        self.food = pygame.image.load(IMG_FOOD).convert_alpha() # convert_alpha() removes the transparent bg which looked black
        self.parent_screen = parent_screen
        # self.x = SIZE*3 # should be a multiple of 40 to get things aligned
        # self.y = SIZE*3 
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,12)*SIZE
    
    def draw_food(self):
        self.parent_screen.blit(self.food,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE # 1000/40 is 25 increments in x direction and it will be a multiple of 40 as its the SIZE
        self.y = random.randint(1,12)*SIZE # 520/40 is 13 increments in y direction... 12 is used to prevent it from going out of range or to (25*size,13*size)

class Game:
    def __init__(self):
        pygame.init() # initialize pygame
        pygame.display.set_caption("SNAKE GAME by Sukhman Singh")
        pygame.mixer.init()
        self.play_bg_music() 

        self.surface = pygame.display.set_mode((WIDTH,HEIGHT)) # create a surface
        # self.surface.fill((126, 232, 12)) # background # self.something is a class member
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.food = food(self.surface)
        self.food.draw_food()        

    def collision(self,x1,y1,x2,y2): # x1,y1 is top-left coordinate of snake head and x2,y2 is top-left coordinate of food
        if x1 >= x2 and x1 < x2 + SIZE: # check the logic once
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont(FONT_TYPE,30, italic = True)
        score = font.render(f"SCORE: {self.snake.length-3}", True, (TEXT_COLOR))
        # timer = font.render(f"TIME: {self.display_game_over}",True,  (TEXT_COLOR)) # time
        # self.surface.blit(timer, (500,10))
        self.surface.blit(score, (10,10))

    def display_game_over(self, p_time):
        self.background()
        font = pygame.font.SysFont(FONT_TYPE,35, italic = True)
        g_over = pygame.image.load(IMG_END)
        self.surface.blit(g_over, (0,0))
        pygame.display.flip()
        line1 = font.render("Press ENTER to Play Again or Press ESCAPE to Exit!", True, (TEXT_COLOR))
        self.surface.blit(line1, (230,205))
        line2 = font.render(f"{self.snake.length-2}",True,  (TEXT_COLOR)) # score
        self.surface.blit(line2, (230,280))
        line3 = font.render(f"{p_time} sec", True, (TEXT_COLOR)) ######## time display
        self.surface.blit(line3, (720,280))
        pygame.mixer.music.pause() # pause music
        pygame.display.flip() # refreshing the UI

    def play(self):
        self.background()
        self.snake.crawl()
        self.food.draw_food()
        self.display_score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y): # logic of snake colliding with food
            print("Yummy!!!")
            self.play_sound("ding")
            self.snake.length_increment()
            self.food.move()

        # for i in range(1, self.snake.length): # Prevent snake from going to infinity
        #     if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
        #         self.play_sound("crash")
        #         raise "Collided with itself !!"
        
        for i in range(3, self.snake.length): # logic of snake colliding with itself
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collided with itself !!"

    def reset(self):
        self.snake = Snake(self.surface,3)
        self.food = food(self.surface)

    def play_sound(self, sound):
        audio = pygame.mixer.Sound(f"./assets/music/{sound}.mp3")
        pygame.mixer.Sound.play(audio) # sound is used for short sounds

    def play_bg_music(self):
        pygame.mixer.music.load(BG_MUSIC) # music is used for longer sounds or songs
        pygame.mixer.music.play()

    def background(self):
        bg = pygame.image.load(IMG_MAIN)
        self.surface.blit(bg, (0,0))

    def start_game(self):
        begin = pygame.image.load(IMG_START)
        self.surface.blit(begin, (0,0))
        pygame.display.flip()
        # pygame.mixer.music.pause() # pause music
        pygame.time.delay(1500)
        instruct = pygame.image.load(IMG_INSTRUCTION)
        self.surface.blit(instruct, (0,0))
        pygame.display.flip() # refreshing the UI
        
    def run(self):
        self.start_game()
        # self.start_time()
        running = True
        pause = True
        while running: # event loop
            for event in pygame.event.get():
                # print(event) # shows all events that are happening
                if event.type == KEYDOWN: # The keydown event is fired when a key is pressed. Unlike the keypress event, the keydown event is fired for all keys, regardless of whether they produce a character value.
                    if event.key == K_ESCAPE: # quit when you press escape key
                        running = False

                    if event.key == K_RETURN: # hit enter to replay
                        pygame.mixer.music.unpause() # restart music
                        pause = False
                        start_time = time.time()
                        # print("enter pressed!")
                        # self.start_game(1)

                    if event.key == K_SPACE:
                        print('SpaceBar Hit!')
                        pause = not pause
                    # elif event.key == K_SPACE:

                    if not pause:
                        if event.key == K_LSHIFT:
                            print('You found the Cheat Key!!')
                            self.snake.length_increment()

                        # if event.key == K_SPACE:
                        #     print('SpaceBar Pause!')
                        #     pause = True

                        if event.key == K_UP:
                            # print("up")
                            self.snake.move_up()
                            self.snake.head_rotation(90)
                            # block_y -=10 # changing cordinates with up key
                            # draw_block() # drawing the block at new location

                        if event.key == K_DOWN:
                            self.snake.move_down()
                            self.snake.head_rotation(270)

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                            self.snake.head_rotation(180)  

                        if event.key == K_LEFT:
                            self.snake.move_left()
                            self.snake.head_rotation(360)  

                elif event.type == QUIT: # when user clicks on cancel
                    running = False

            try:
                if not pause:
                    self.play()
            
            except Exception as e:
                play_time = time.time() - start_time
                self.display_game_over(int(play_time))
                pause = True
                self.reset()

            time.sleep(0.15)

if __name__ == "__main__": # run if file is being accessed directly
    game = Game() # object of game class
    game.run()



