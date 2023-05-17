import pygame
from threading import Thread
from random import randint, uniform, choice as choice_f
from math import cos, sin

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139,69,19)
GREY = (128, 128, 128)
DARK_GREY = (90, 90, 90)
YELLOW = (255,255,0)

META_X = 160

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
screen_width = 800
screen_height = 600
middle_rect_x = (150, 500)
middle_rect_y = (200, 200)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()

# Define the car class
class Car(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()

        # Set the car's properties
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.starting_x = x
        self.starting_y = y
        self.circles = 0
        self.starts = 0

    def move(self, forward, angle):
        old_x = self.rect.x
        self.rect.x += forward * cos(angle)
        self.rect.y += forward * sin(angle)
        # Check if the car crosses the boundaries of the circuit area
        if (0 <= self.rect.x >= screen_width) or  (0 <= self.rect.y >= screen_width):
            self.rect.x = self.starting_x 
            self.rect.y = self.starting_y
            self.starts += 1
            self.circles = 0
        # check if not inside race highway
        if (middle_rect_x[0] <= self.rect.x <= middle_rect_x[0]+middle_rect_x[1]) and (middle_rect_y[0] <= self.rect.y <= middle_rect_y[0]+middle_rect_y[1]):
            self.rect.x = self.starting_x  
            self.rect.y = self.starting_y 
            self.starts += 1
            self.circles = 0
        if self.rect.y <= 200 and old_x >= META_X >= self.rect.x : 
            self.circles += 1
            print(self.circles)
            return

circuit_rect = pygame.Rect(middle_rect_x[0], middle_rect_y[0], middle_rect_x[1], middle_rect_y[1])



# Create car instances
WIDTH = 20
HEIGHT = 20
STARTING_X = 60
STARTING_Y = 100
car1 = Car(RED, WIDTH, HEIGHT, STARTING_X-20, STARTING_Y)
car2 = Car(YELLOW, WIDTH, HEIGHT, STARTING_X, STARTING_Y)
car3 = Car(BLUE, WIDTH, HEIGHT, STARTING_X+20, STARTING_Y)

all_sprites = pygame.sprite.Group()
all_sprites.add(car1, car2, car3)

# Define the thread function to move the cars
def move_cars():
    while True:
        for car in all_sprites:
            #calculate car movement 
            forward = randint(3,5)
            angle = uniform(0.9,1.1)
            # check car position

            if (800 > car.rect.x >= 700) and (450 >= car.rect.y >= 150):
                choice = 1
            elif (0 < car.rect.y <= 150) and (700 >= car.rect.x >= 100):
                choice = 2
            elif (0 < car.rect.x <= 100) and (450 >= car.rect.y >= 150): 
                choice = 3
            elif (600 > car.rect.y >= 450) and (700 >= car.rect.x >= 100):
                choice = 4
            elif (800 > car.rect.x >= 700) and (car.rect.y <= 150):
                choice = choice_f([1,2,1,2,4]) # 1/2
            elif (0 < car.rect.x <= 100) and (car.rect.y <= 150):
                choice = choice_f([2,3,2,3,4]) # 2/3 
            elif (0 < car.rect.x <= 100) and (car.rect.y >= 450):
                choice = choice_f([1,3,4,3,4]) # 3/4
            elif (800 > car.rect.x >= 700) and (car.rect.y >= 450):
                choice = choice_f([1,2,4,1,4]) # 1/4
            else:
                choice = randint(1,4)
            
            if choice == 1:
                angle *= 1.5 * 3.14
            elif choice == 2:
                angle *= 3.14
            elif choice == 3: 
                angle *= 0.5 * 3.14
            elif choice == 4:
                angle = uniform(-0.1, 0.1)

            
            car.move(forward, angle)


        pygame.time.wait(5)

# Create a thread for moving the cars
move_thread = Thread(target=move_cars)
move_thread.start()

# Define the circuit area

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the screen
    screen.fill(WHITE)
    
    # Draw the circuit area
    pygame.draw.rect(screen, RED, circuit_rect, 2)

    pygame.draw.rect(screen, GREY, [0, 0,screen_width, screen_height]) # ROAD
    pygame.draw.rect(screen, DARK_GREY, [0, 0,middle_rect_x[0], middle_rect_y[0]]) # OIL DROPOUT
    pygame.draw.rect(screen, DARK_GREY, [middle_rect_x[0]+middle_rect_x[1], 0,screen_width-middle_rect_x[0]+middle_rect_x[1], middle_rect_y[0]]) # OIL DROPOUT
    pygame.draw.rect(screen, DARK_GREY, [0, middle_rect_y[0]+middle_rect_y[1],middle_rect_x[0], screen_height-middle_rect_y[0]+middle_rect_y[1]]) # OIL DROPOUT
    pygame.draw.rect(screen, DARK_GREY, [middle_rect_x[0]+middle_rect_x[1], middle_rect_y[0]+middle_rect_y[1],screen_width-middle_rect_x[0]+middle_rect_x[1], screen_height-middle_rect_y[0]+middle_rect_y[1]]) # OIL DROPOUT    
    pygame.draw.rect(screen, BROWN, [middle_rect_x[0]-40, middle_rect_y[0]-40,middle_rect_x[1]+80, middle_rect_y[1]+80]) # DIRT
    pygame.draw.rect(screen, GREEN, [middle_rect_x[0]+2, middle_rect_y[0]+2,middle_rect_x[1]-4, middle_rect_y[1]-4]) # GRASS
    # add black and white meta line between (0,200) and (150,200)
    pygame.draw.lines(screen, WHITE, False, [(META_X,0), (META_X,40)], 5)
    pygame.draw.lines(screen, BLACK, False, [(META_X,40), (META_X,80)], 5)
    pygame.draw.lines(screen, WHITE, False, [(META_X,80), (META_X,120)], 5)
    pygame.draw.lines(screen, BLACK, False, [(META_X,120), (META_X,160)], 5)




    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()
    clock.tick(60)

# Stop the thread
move_thread.join()

# Quit the game
pygame.quit()
