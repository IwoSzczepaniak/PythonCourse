import msvcrt
import time

UKLAD = []

def NAND(wy,*we):
  UKLAD.append((wy,we))

STAN = {}

def nand(wy,we):
  for x in we:
    if STAN[x]==0: 
      STAN[wy] = 1
      return
  STAN[wy] = 0 

def inputs():
  if msvcrt.kbhit():
    k = msvcrt.getch().decode('utf-8')
    if k in STAN:
      STAN[k]=1-STAN[k]

def outputs():
  for k in STAN.keys():
    if k in "abcdefghijklmnopqrstuvwxyz":
      print(k,STAN[k],' ',end='')
  print()

def variables(*v):
  for x in v:
    STAN[x] = 0

def sim():
  while True:
    inputs()
    for el in UKLAD:  nand(el[0],el[1])
    outputs()
    # time.sleep(2)

variables('a','b','c')

NAND('c','a','b')

sim()
