import pygame
from tkinter import Label, Entry, Button, Tk, BOTTOM
from random import choice

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
            elif grid[x][y] == RED:
                grid[x][y] = GREEN

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

    def color_neighbours(x, y):
        change_color(x, y)
        for xi in range(x-1, x+2):
                for yi in range(y-1, y+2):
                    if xi != x and not yi != y or not xi != x and yi != y:
                        change_color(xi, yi)

    def event_handler(event):
        nonlocal running
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Lewy przycisk myszy
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] // GRID_SIZE
            y = mouse_pos[1] // GRID_SIZE
            color_neighbours(x, y)
            
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            event_handler(event)

        refresh()

    pygame.quit()


def start():
    def set_values_correctly(input_val):
        global N, GRID_SIZE, HEIGHT, WIDTH, grid

        N = int(input_val.get())
        if N <= 0: 
            print_error("N musi być większe niż 0")
            return False
        GRID_SIZE = HEIGHT // N
        HEIGHT = WIDTH = N * GRID_SIZE
        if GRID_SIZE == 0:
            print_error("Ilość N na tyle duża,\nże nie ma możliwości podziału na tak wiele kafelków")
            return False
        grid = [[choice((GREEN, RED)) for _ in range(N)] for _ in range(N)]
        return True

    def print_error(err_msg):
        root = Tk()
        root.title("ERROR")

        root.geometry("500x100")

        root.configure(bg='red')

        label_input = Label(root, text=f"\n\nOtrzymano błąd: {err_msg}!\n")
        label_input.config(fg="white")
        label_input.config(font=("Courier", 14))
        label_input.configure(bg='red')
        label_input.pack()


    def setup():
        nonlocal root
        root.title("Wprowadź ilość komórek w linii")
        root.geometry("500x200")

    def texts():
        nonlocal root
        label_info = Label(root, text="Użytkownik na wejściu otrzymuje losowo wygenerowaną planszę z NxN kafelkami " +
                        "w kolorach zielonym i czerwonym. Celem gry jest wyeliminowanie koloru zielonego z planszy. "+
                        "Aby to zrobić należy kliknąć na dowolny kafelek, czego skutkiem będzie zamiana kolorów " + 
                       "w tej komórce oraz jej sąsiednich(na planie krzyżyka). \n\n", wraplength=400, justify="center")
        label_info.pack()

        label_input = Label(root, text="Wprowadź ilość komórek w linii - używaj tylko wartości całkowitych\n")
        label_input.pack()

    def start_keys():
        def define():
            input_val = enter_input
            try:
                if set_values_correctly(input_val): 
                    game_loop()
            except ValueError:
                print_error("Wprowadź liczbę całkowitą")

        nonlocal root
        enter_input = Entry(root)
        enter_input.pack()

        button_start = Button(root, text="Start", command=define)
        button_start.pack(side=BOTTOM)
        root.bind("<Return>", lambda event: define())

    root = Tk()
    setup()
    texts()
    start_keys()
    root.mainloop()


if __name__ == "__main__":
    start()
