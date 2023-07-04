import tkinter as tk
from classes import DigitalCircuitSimulator, LED
from common import *
from time import time
from logical_functions import *

def _nand(wy,we):
  for x in we:
    if STAN[x]==0: 
      STAN[wy] = 1
      return
  STAN[wy] = 0 

def _and(wy,we):
  for x in we:
    if STAN[x]==0: 
      STAN[wy] = 0
      return
  STAN[wy] = 1 


def _nor(wy,we):
  for x in we:
    if STAN[x]==1: 
      STAN[wy] = 0
      return
  STAN[wy] = 1 


def _or(wy,we):
  for x in we:
    if STAN[x]==1: 
      STAN[wy] = 1
      return
  STAN[wy] = 0 


def _xor(wy,we):
  STAN[wy] = sum([STAN[x] for x in we])%2


def _not(wy,we):
  STAN[wy] = 1-STAN[we] 

def start_simulation(f_name):

    LEDS = []
    BUTTONS = []
    OUTPUTS = []

    n_LEDS = 2
    n_OUTPUTS = 2

    if f_name == "NOT": 
       n_LEDS = 1
       n_OUTPUTS = 1
       NOT(n_LEDS, 0)

    elif f_name == "NAND": 
        n_OUTPUTS = 1
        NAND(n_LEDS, *range(n_LEDS))
    elif f_name == "AND": 
       n_OUTPUTS = 1
       AND(n_LEDS, *range(n_LEDS))
    elif f_name == "OR": 
       n_OUTPUTS = 1
       OR(n_LEDS, *range(n_LEDS))
    elif f_name == "NOR": 
       n_OUTPUTS = 1
       NOR(n_LEDS, *range(n_LEDS))
    elif f_name == "XOR": 
       n_OUTPUTS = 1
       XOR(n_LEDS, *range(n_LEDS))
    elif f_name == "RS":
       n_LEDS = 4
       RS(n_LEDS, *range(4))
    elif f_name == "JK":
       n_LEDS = 3
       n_OUTPUTS = 2
       JK("time", 0, 1, 2, n_LEDS, n_LEDS+1)
    elif f_name == "RS":
       n_LEDS = 4
       RS(n_LEDS, *range(4))
    elif f_name == "JK":
       n_LEDS = 3
       n_OUTPUTS = 2
       JK("time", 0, 1, 2, n_LEDS, n_LEDS+1)
    elif f_name == "D2":
       n_LEDS = 2
       n_OUTPUTS = 2
       D2("time", 0, 1, n_LEDS, n_LEDS+1)
    elif f_name == "D":
       n_LEDS = 2
       n_OUTPUTS = 2
       D("time", 0, 1, n_LEDS, n_LEDS+1)
    elif f_name == "COUNTER16":
       n_LEDS = 1
       n_OUTPUTS = 4
       COUNTER16("time", 0, n_LEDS+3, n_LEDS+2, n_LEDS+1, n_LEDS)
    elif f_name == "COUNTER10":
       n_LEDS = 1
       n_OUTPUTS = 4
       COUNTER10("time", 0, n_LEDS+3, n_LEDS+2, n_LEDS+1, n_LEDS)
    elif f_name == "REJ4":
       n_LEDS = 2
       n_OUTPUTS = 4
       REJ4("time", 0, 1, n_LEDS, n_LEDS+1, n_LEDS+2, n_LEDS+3)
    elif f_name == "LATCH":
       n_LEDS = 1
       n_OUTPUTS = 2
       LATCH("time", 0, n_LEDS, n_LEDS+1)




    dx = min( int(WINDOW_SIZE / (n_LEDS + 2)), int(WINDOW_SIZE / (n_OUTPUTS + 1)))

    root = tk.Tk()
    root.title('Digital Circuit Simulator')
    root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

    simulator = DigitalCircuitSimulator(root)

    for i in range(n_LEDS):
        led = LED(root, f'INPUT {i}')
        LEDS.append(led)
        simulator.add_component(led)
        STAN[i] = 0

    for i in range(n_LEDS):
        LEDS[i].canvas.place(x=dx - 5 + dx * i, y=50)

    def set_led_state(led_index):
        LEDS[led_index].state = not LEDS[led_index].state
        simulator.update_circuit()
        STAN[led_index] = 1 - STAN[led_index]
        # print(STAN[led_index])

    for i in range(n_LEDS):
        BUTTONS.append(tk.Button(root, text=f'INPUT {i}', command=lambda i=i: set_led_state(i)))
        BUTTONS[i].place(x=dx - 10 + dx * i, y=100)

    for j in range(n_OUTPUTS):
        led = LED(root, f'OUTPUT {j}')
        OUTPUTS.append(led)
        simulator.add_component(led)
        OUTPUTS[j].canvas.place(x=dx - 5 + dx * j, y=300)
        STAN[j+n_LEDS] = 0

    output_label = tk.Label(root, text="OUTPUT:")
    output_label.place(x=dx - 5, y=270)


    time_led = LED(root, f'OUTPUT {n_OUTPUTS}')
    simulator.add_component(led)
    time_led.canvas.place(x=dx - 5 + dx * n_LEDS, y=50)
    time_label = tk.Label(root, text="CLOCK")
    time_label.place(x=dx - 10 + dx * n_LEDS, y=100)
    STAN["time"] = 0
    STAN["true"] = 1
    STAN["false"] = 0


    func_label = tk.Label(root, text=f_name)
    func_label.place(x=180, y=200)

    t1 = time()
    while 1:
        if time()-t1 > 0.5:       # 0.5 sek to po�owa okresu zegara
            time_led.state = not time_led.state
            time_led.update_state()
            t1 = time()
            STAN["time"] = 1 - STAN["time"]


        for el in UKLAD:
            eval(el[0])(el[1],el[2])
        
        for k in range(n_LEDS, n_LEDS+n_OUTPUTS):
            OUTPUTS[k-n_LEDS].state = not STAN[k]
            # simulator.update_circuit()

        '''visualisation''' 
        simulator.update_circuit()
            
        root.update()

if __name__ == '__main__':
    start_simulation("COUNTER16")