#!/usr/bin/python3
# -*- coding: utf-8 -*-
from threading import Thread
import time
import random
import os
def printxy(x,y,s):
 print("\033["+str(y+1)+";"+str(x+1)+"f"+s)
def clrscr():
 print(chr(27)+"[2J")
class Krolik(Thread):
 def __init__ (self,x,y):
    self.x=x
    self.y=y
    Thread.__init__(self)
 def run(self):
    while (True):
        time.sleep(1)
        nx = self.x+random.randint(-1,1)
        ny = self.y+random.randint(-1,1)
        if not (0<=nx<N and 0<=ny<N):
            continue
        printxy(self.x,self.y," ")
        wyspa[self.x][self.y] = " "
        if wyspa[nx][ny]=='k':
            break # królik ginie
            # k=Krolik(x,y) # powstaje nowy królik
            # k.start()
            # pass
        self.x = nx
        self.y = ny
        printxy(self.x,self.y,"k")
        wyspa[self.x][self.y] = "k"
    # end class

if __name__ == '__main__':
 clrscr()
 os.system('setterm -cursor off')
 N = 20
 wyspa = [[" " for _ in range(N)] for _ in range(N)]
 for n in range(10):
    x = random.randint(0,N-1)
    y = random.randint(0,N-1)
    wyspa[x][y] = "k"
    k=Krolik(x,y)
    k.start()
    time.sleep(0.1)
input()
print("stop")
os.system('setterm -cursor on')