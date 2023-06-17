import pygame
from tkinter import Label, Entry, Button, Tk, BOTTOM

# Domyślne stawienia ekranu
WIDTH = 800
HEIGHT = 800
N = 10
FPS = 30
grid = []

# Kolory
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


def game_loop():
    def draw_grid():
        for x in range(N):
            for y in range(N):
                pygame.draw.rect(screen, grid[x][y], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    def change_color(x, y):
        if 0 <= x < N and 0 <= y < N:
            if grid[x][y] == GREEN:
                grid[x][y] = RED

    def check_game_over():
        for x in range(N):
            for y in range(N):
                if grid[x][y] == GREEN:
                    return False
        return True

    def refresh():
        nonlocal running
        screen.fill(BLACK)
        draw_grid()
        if check_game_over():
            print("Gra zakończona")
            running = False
        pygame.display.flip()

    def event_handler(event):
        nonlocal running
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Lewy przycisk myszy
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] // GRID_SIZE
            y = mouse_pos[1] // GRID_SIZE
            change_color(x, y)


    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            event_handler(event)

        refresh()

    pygame.quit()


def start():
    def define():
        text = entry_include.get().split
        try:
            global N
            N = int(text)
        except ValueError:
            print("Błędna wartość. Wprowadź liczbę całkowitą.")

        global GRID_SIZE, HEIGHT, WIDTH, grid

        grid = [[GREEN for _ in range(N)] for _ in range(N)]  # Inicjalizacja planszy

        GRID_SIZE = HEIGHT // N
        HEIGHT = WIDTH = N*GRID_SIZE

        game_loop()


    root = Tk()
    root.title("Type in amount of cells")

    root.geometry("500x300")

    label_include = Label(root, text="\Type in amount of cells - use only integer values\n")
    label_include.pack()

    entry_include = Entry(root)
    entry_include.pack()


    button_start = Button(root, text="Start", command=define)
    button_start.pack(side=BOTTOM)

    root.mainloop()


if __name__ == "__main__":
    start()