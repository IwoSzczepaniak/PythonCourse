import pygame
from threading import Thread, Event
from car_class import *


# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()

driving_history = [
    "You started your journey on a sunny day.",
    "The road was winding through picturesque landscapes.",
    "You passed by a small town with colorful houses.",
    "As you continued driving, it started to rain heavily.",
    "The windshield wipers were working hard to keep the view clear.",
    "You stopped at a gas station to refuel.",
    "The rain subsided, and a beautiful rainbow appeared in the sky.",
    "You reached your destination safely. It was a memorable trip."
]

def show_driving_history():
    font = pygame.font.Font(None, 24)

    scrolling = True
    y_position = screen_HEIGHT

    while scrolling:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scrolling = False

        screen.fill(GREY)

        # Render and display the driving history
        for i, line in enumerate(driving_history):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(screen_WIDTH // 2, y_position + (i * 30)))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

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
                if event.key == pygame.K_RETURN:
                    menu_running = False

        # Update the menu screen
        screen.fill(GREY)
        menu_text = pygame.font.Font(None, 48).render("Car Race", True, RED)
        menu_text_rect = menu_text.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2))
        screen.blit(menu_text, menu_text_rect)

        press_enter_text = pygame.font.Font(None, 24).render("Press ENTER to start", True, RED)
        press_enter_rect = press_enter_text.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 50))
        screen.blit(press_enter_text, press_enter_rect)

        pygame.display.flip()
        clock.tick(60)


def show_race():


    circuit_rect = pygame.Rect(middle_rect_x[0], middle_rect_y[0], middle_rect_x[1], middle_rect_y[1])

    car1 = Car(RED, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X - 20, CAR_STARTING_Y)
    car2 = Car(YELLOW, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X, CAR_STARTING_Y)
    car3 = Car(BLUE, CAR_WIDTH, CAR_HEIGHT, CAR_STARTING_X + 20, CAR_STARTING_Y)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(car1, car2, car3)


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


    # Game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and quit_button.collidepoint(event.pos):
                    running = False
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


        for i, count in enumerate(circle_counts):
            text = font.render(f"Car {i+1}: {count} Circles", True, car_colors[i])
            text_rect = text.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2  - 50 + i * 40))
            screen.blit(text, text_rect)

        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        text_quit = font.render("Quit", True, (255, 255, 255))
        quit_button_text_rect = text_quit.get_rect(center=quit_button.center)
        screen.blit(text_quit, quit_button_text_rect)


        # Flip the display
        pygame.display.flip()
        clock.tick(60)

    # Stop the car threads
    car1_thread.join()
    car2_thread.join()
    car3_thread.join()

    # Quit the game
    pygame.quit()


show_driving_history()
show_menu()
show_race()