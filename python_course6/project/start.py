from main import *

LABEL ='NAND'

root = tk.Tk()
root.title('Digital Circuit Simulator Menu')
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

curr = 0
label = tk.Label(root, text=FUNCTIONS[0])
label.place(x=160, y=100)
n_LEDS = 2

def change_function():
    global curr, LABEL
    label.configure(text=FUNCTIONS[curr])
    LABEL = FUNCTIONS[curr]
    curr += 1
    curr %= len(FUNCTIONS)
    if curr>5:
        n_LEDS_label.place_forget()
        increase_n_button.place_forget()
        decrease_n_button.place_forget()
        in_de_label.place_forget()
        in_de_label2.place_forget()
    elif curr==1:
        n_LEDS_label.place(x=250, y=100)
        increase_n_button.place(x=270, y=90)
        decrease_n_button.place(x=270, y=110)
        in_de_label.place(x=250, y=70)
        in_de_label2.place(x=200, y=370)
change_button = tk.Button(root, text=f'Different logical function', command=change_function)
change_button.config(width=25)
change_button.place(x=120, y=200)

def increase_n():
    global n_LEDS
    n_LEDS += 1
    n_LEDS_label.configure(text=f'{n_LEDS}')

def decrease_n():
    global n_LEDS
    if n_LEDS > 0: 
        n_LEDS -= 1
        n_LEDS_label.configure(text=f'{n_LEDS}')

n_LEDS_label = tk.Label(root, text=n_LEDS)
n_LEDS_label.place(x=250, y=100)

increase_n_button = tk.Button(root, text=f'^', command=increase_n)
increase_n_button.place(x=270, y=90)
increase_n_button.config(width=2)

decrease_n_button = tk.Button(root, text=f'v', command=decrease_n)
decrease_n_button.config(width=2)
decrease_n_button.place(x=270, y=110)

in_de_label = tk.Label(root, text="SET N*")
in_de_label2 = tk.Label(root, text="*NUMBER OF INPUT SIGNALS")
in_de_label.place(x=265, y=70)
in_de_label2.place(x=200, y=370)



def start_sim():
    print(f"Label name: {LABEL}")
    try:
        if curr > 5: start_simulation(LABEL)
        else: start_simulation(LABEL, n_LEDS)
    except tk.TclError:
        return
    root.quit()

start_sim_button = tk.Button(root, text=f'Start simulation', command=start_sim)
start_sim_button.config(width=25)
start_sim_button.place(x = 120, y = 250)

root.mainloop()

