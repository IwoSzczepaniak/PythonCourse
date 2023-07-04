from main import *

LABEL ='DEFAULT'

root = tk.Tk()
root.title('Digital Circuit Simulator Menu')
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

curr = 0
label = tk.Label(root, text=FUNCTIONS[0])
label.place(x=180, y=100)

def change_function():
    global curr, LABEL
    label.configure(text=FUNCTIONS[curr])
    LABEL = FUNCTIONS[curr]
    curr += 1
    curr %= len(FUNCTIONS)

change_button = tk.Button(root, text=f'Choose logical function', command=change_function)
change_button.place(x=150, y=200)

def start_sim():
    print(f"Label name: {LABEL}")
    try:
        start_simulation(LABEL)
    except tk.TclError:
        return
    root.quit()

start_sim_button = tk.Button(root, text=f'Start simulation', command=start_sim)
start_sim_button.place(x = 150, y = 250)

root.mainloop()

