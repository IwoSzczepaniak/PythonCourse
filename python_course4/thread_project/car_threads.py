import pygame
from threading import Thread, Event
from car_class import *
from random import choice as choice_f
from time import sleep

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((screen_WIDTH + 200, screen_HEIGHT))
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()

driving_history = [
    "Mission Objective: Race to Victory",
    "",
    "Mission Briefing:",
    
    "Your objective is to participate in a high-stakes race through the streets of San Andreas.",
    "Your mission is to ensure that the red car emerges as the winner by eliminating any competing vehicles.",
    "Unfortunately our snipers are daltonists and do not recognize colors - the kill the drivers randomly",
    "Be cautious not to harm the red car or jeopardize its chances of winning.",
    f"Remember that every shot costs {SHOT_EXPENCE}$ and our budget is only {BUDGET}$.",
    f"You will be able to earn money({LAP_INCOME}$) by letting drivers do laps around the circuit.",
    "Use red buttons or space key to kill!"
    "Good luck, and may the fastest car prevail!",
    "",
]


def show_driving_history():
    font = pygame.font.Font(None, 24)

    scrolling = True
    y_position = screen_HEIGHT
    skip_button_pressed = False

    skip_button_rect = pygame.Rect(50, screen_HEIGHT - 80, 100, 40)


    while scrolling:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or pygame.K_SPACE:
                    scrolling = False
                    skip_button_pressed = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if skip_button_rect.collidepoint(event.pos):
                    scrolling = False
                    skip_button_pressed = True


        screen.fill(GREY)

        if skip_button_pressed:
            skip_text = font.render("Skipping...", True, WHITE)
            skip_text_rect = skip_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT//2))
            screen.blit(skip_text, skip_text_rect)
        
        else:
            # Render and display the driving history
            for i, line in enumerate(driving_history):
                text = font.render(line, True, WHITE)
                text_rect = text.get_rect(center=((screen_WIDTH+200) // 2, y_position + (i * 30)))
                screen.blit(text, text_rect)


        pygame.draw.rect(screen, WHITE, skip_button_rect)
        skip_text = font.render("Skip", True, GREY)
        skip_text_rect = skip_text.get_rect(center=skip_button_rect.center)
        screen.blit(skip_text, skip_text_rect)


        pygame.display.flip()
        clock.tick(60)
        if skip_button_pressed: sleep(1)

        # Scroll the text upwards
        y_position -= 1
        if y_position < -(len(driving_history) * 30):
            scrolling = False


# Define the menu function
def show_menu():
    menu_running = True

    while menu_running:
        # Process menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or pygame.K_SPACE:
                    menu_running = False

        # Update the menu screen
        screen.fill(GREY)
        menu_text = pygame.font.Font(None, 48).render("Car Race", True, RED)
        menu_text_rect = menu_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2))
        screen.blit(menu_text, menu_text_rect)

        press_enter_text = pygame.font.Font(None, 24).render("When ready - click ENTER to start! Good luck!", True, WHITE)
        press_enter_rect = press_enter_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2 + 50))
        screen.blit(press_enter_text, press_enter_rect)

        pygame.display.flip()
        clock.tick(60)

def show_win():
    screen = pygame.display.set_mode((screen_WIDTH + 200, screen_HEIGHT))
    win_running = True

    while win_running:
        # Process menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    win_running = False

        # Update the menu screen
        screen.fill(GREY)
        menu_text = pygame.font.Font(None, 48).render("You Win!", True, RED)
        menu_text_rect = menu_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2))
        screen.blit(menu_text, menu_text_rect)

        press_enter_text = pygame.font.Font(None, 24).render("Click ENTER to exit", True, WHITE)
        press_enter_rect = press_enter_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2 + 50))
        screen.blit(press_enter_text, press_enter_rect)

        pygame.display.flip()
        clock.tick(60)

def show_loose():
    loose_running = True
    screen = pygame.display.set_mode((screen_WIDTH + 200, screen_HEIGHT))

    while loose_running:
        # Process menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    loose_running = False
                    show_race()

        # Update the menu screen
        screen.fill(GREY)
        menu_text = pygame.font.Font(None, 48).render("You Loose!", True, RED)
        menu_text_rect = menu_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2))
        screen.blit(menu_text, menu_text_rect)

        press_enter_text = pygame.font.Font(None, 24).render("Click ENTER to restart", True, WHITE)
        press_enter_rect = press_enter_text.get_rect(center=((screen_WIDTH+200) // 2, screen_HEIGHT // 2 + 50))
        screen.blit(press_enter_text, press_enter_rect)

        pygame.display.flip()
        clock.tick(60)

def show_race():
    money = BUDGET
    screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))

    circuit_rect = pygame.Rect(middle_rect_x[0], middle_rect_y[0], middle_rect_x[1], middle_rect_y[1])

    car1 = Car(RED, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X - 20, CAR_STARTING_Y)
    car2 = Car(YELLOW, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X, CAR_STARTING_Y)
    car3 = Car(BLUE, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X + 20, CAR_STARTING_Y)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(car1, car2, car3)

    def kill_random_car():
        nonlocal money 
        if money > SHOT_EXPENCE:
            cars = [car1, car2, car3]
            random_car = choice_f(cars)
            random_car.kill()
            money -= SHOT_EXPENCE

    # Define the thread function for each car
    def move_car(car):
        car.move()


    # Create a thread for each car
    car1_thread = Thread(target=move_car, args=(car1,))
    car2_thread = Thread(target=move_car, args=(car2,))
    car3_thread = Thread(target=move_car, args=(car3,))

    # Start the car threads
    car1_thread.start()
    car2_thread.start()
    car3_thread.start()

    font = pygame.font.Font(None, 36)

    quit_button = pygame.Rect(20, 20, 100, 50)
    kill_car_button = pygame.Rect(140, 20, 150, 50)


    # Game loop
    running = True

    old_circle_counts = [0,0,0]
    win = False
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    kill_random_car()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and quit_button.collidepoint(event.pos):
                    running = False
                elif event.button == 1 and kill_car_button.collidepoint(event.pos):
                    kill_random_car()

            if not running:
                pygame.quit()
                car1.stop_event = True
                car2.stop_event = True
                car3.stop_event = True


        # Update the screen
        screen.fill(WHITE)

        pygame.draw.rect(screen, RED, circuit_rect, 2)


        pygame.draw.rect(screen, RED, circuit_rect, 2)

        # WORLD ELEMENTS
        pygame.draw.rect(screen, GREY, [0, 0, screen_WIDTH, screen_HEIGHT]) # ROAD
        pygame.draw.rect(screen, DARK_GREY, [0, 0,middle_rect_x[0], middle_rect_y[0]]) # OIL DROPOUT
        pygame.draw.rect(screen, DARK_GREY, [middle_rect_x[0]+middle_rect_x[1], 0,screen_WIDTH-middle_rect_x[0]+middle_rect_x[1], middle_rect_y[0]]) # OIL DROPOUT
        pygame.draw.rect(screen, DARK_GREY, [0, middle_rect_y[0]+middle_rect_y[1],middle_rect_x[0], screen_HEIGHT-middle_rect_y[0]+middle_rect_y[1]]) # OIL DROPOUT
        pygame.draw.rect(screen, DARK_GREY, [middle_rect_x[0]+middle_rect_x[1], middle_rect_y[0]+middle_rect_y[1],screen_WIDTH-middle_rect_x[0]+middle_rect_x[1], screen_HEIGHT-middle_rect_y[0]+middle_rect_y[1]]) # OIL DROPOUT    
        pygame.draw.rect(screen, BROWN, [middle_rect_x[0]-40, middle_rect_y[0]-40,middle_rect_x[1]+80, middle_rect_y[1]+80]) # DIRT
        pygame.draw.rect(screen, GREEN, [middle_rect_x[0]+2, middle_rect_y[0]+2,middle_rect_x[1]-4, middle_rect_y[1]-4]) # GRASS
        #META
        pygame.draw.lines(screen, WHITE, False, [(META_X,0), (META_X,40)], 5)
        pygame.draw.lines(screen, BLACK, False, [(META_X,40), (META_X,80)], 5)
        pygame.draw.lines(screen, WHITE, False, [(META_X,80), (META_X,120)], 5)
        pygame.draw.lines(screen, BLACK, False, [(META_X,120), (META_X,160)], 5)

        all_sprites.draw(screen)

        circle_counts = [car.circles for car in all_sprites.sprites()]
        car_colors = [car.color for car in all_sprites.sprites()]
        for i in range(len(old_circle_counts)):
            if circle_counts[i] != old_circle_counts[i]: money+=LAP_INCOME
        old_circle_counts = circle_counts

        for i, count in enumerate(circle_counts):
            text = font.render(f"Car {i+1}: {count} Circles", True, car_colors[i])
            text_rect = text.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2  - 50 + i * 40))
            screen.blit(text, text_rect)
            if count == 5:
                running = False
                if car_colors[i] != RED: win = False
                else: win = True 
        
        text = font.render(f"MONEY {money}$", True, YELLOW)
        text_rect = text.get_rect(center=(screen_WIDTH- 100, 30))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        text_quit = font.render("Quit", True, (255, 255, 255))
        quit_button_text_rect = text_quit.get_rect(center=quit_button.center)
        screen.blit(text_quit, quit_button_text_rect)

        pygame.draw.rect(screen, (255, 0, 0), kill_car_button)
        text_kill_car = font.render("Kill Random", True, (255, 255, 255))
        kill_car_button_text_rect = text_kill_car.get_rect(center=kill_car_button.center)
        screen.blit(text_kill_car, kill_car_button_text_rect)


        # Flip the display
        pygame.display.flip()
        clock.tick(60)

    if win:
        show_win()
    else:
        show_loose()


    # Quit the game
    pygame.quit()

show_driving_history()
show_menu()
show_race()