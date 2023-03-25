from tkinter import Tk, Label, Button
import time

def greet():
  print("Pozdrawiam!")


win = Tk()

win.geometry('350x200')

win.title("Przykladowe GUI")

label = Label(win, text="Jakis tekst")
label.grid(column=1, row=1)

greet_button = Button(win, text="Greet", command=greet)
greet_button.grid(column=3, row=3)                              

close_button = Button(win, text="Close", command=quit)
close_button.grid(column=4, row=4)

win.mainloop()
