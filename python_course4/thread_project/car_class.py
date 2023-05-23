from random import randint, uniform, choice as choice_f
from math import cos, sin
import pygame

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GREY = (128, 128, 128)
DARK_GREY = (90, 90, 90)
YELLOW = (255, 255, 0)

META_X = 300

# Set the CAR_WIDTH and CAR_HEIGHT of the screen
screen_WIDTH = 800
screen_HEIGHT = 600

# set the middle rect
middle_rect_x = (150, 500)  # [0] min x, [1] width
middle_rect_y = (200, 200)  # [0] min y, [1] height

# Create car consts
CAR_WIDTH = 20
CAR_HEIGHT = 20
CAR_STARTING_X = 60
CAR_STARTING_Y = 100

MAX_CIRCLES = 5


# CAR CLASS
class Car(pygame.sprite.Sprite):
    def __init__(self, color, CAR_WIDTH, CAR_HEIGHT, x, y):
        super().__init__()

        # Set the car's properties
        self.image = pygame.Surface([CAR_WIDTH, CAR_HEIGHT])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.CAR_STARTING_X = x
        self.CAR_STARTING_Y = y
        self.circles = 0
        self.starts = 0
        self.stop_event = False


    def move(self):
        c_flag = 10
        while self.circles < MAX_CIRCLES and not self.stop_event:
            forward = randint(3, 5)
            angle = uniform(0.9, 1.1)
            c_flag += 1


            # Check if the car crosses the boundaries of the circuit area
            if self.rect.x < 0 or self.rect.x >= screen_WIDTH or self.rect.y < 0 or self.rect.y >= screen_HEIGHT:
                self.rect.x = self.CAR_STARTING_X
                self.rect.y = self.CAR_STARTING_Y
                self.starts += 1
                self.circles = 0

            # check if not inside race highway
            if middle_rect_x[0] <= self.rect.x <= middle_rect_x[0] + middle_rect_x[1] and middle_rect_y[0] <= self.rect.y <= middle_rect_y[0] + middle_rect_y[1]:
                self.rect.x = self.CAR_STARTING_X
                self.rect.y = self.CAR_STARTING_Y
                self.starts += 1
                self.circles = 0

            if self.rect.y <= 200 and 5 >= META_X - self.rect.x >= 0 and c_flag > 10:
                self.circles += 1
                c_flag = 0
                # print(self.circles)

            forward = randint(3,5)
            angle = uniform(0.9,1.1)
            # check self position

            if (800 > self.rect.x >= 700) and (450 >= self.rect.y >= 150):
                choice = 1
            elif (0 < self.rect.y <= 150) and (700 >= self.rect.x >= 100):
                choice = 2
            elif (0 < self.rect.x <= 100) and (450 >= self.rect.y >= 150): 
                choice = 3
            elif (600 > self.rect.y >= 450) and (700 >= self.rect.x >= 100):
                choice = 4
            elif (800 > self.rect.x >= 700) and (self.rect.y <= 150):
                choice = choice_f([1,2,1,2,4]) # 1/2
            elif (0 < self.rect.x <= 100) and (self.rect.y <= 150):
                choice = choice_f([2,3,2,3,4]) # 2/3 
            elif (0 < self.rect.x <= 100) and (self.rect.y >= 450):
                choice = choice_f([1,3,4,3,4]) # 3/4
            elif (800 > self.rect.x >= 700) and (self.rect.y >= 450):
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

            self.rect.x += forward * cos(angle)
            self.rect.y += forward * sin(angle)

            pygame.time.wait(5)
