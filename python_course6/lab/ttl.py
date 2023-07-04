import msvcrt
import time

UKLAD = []  # lista zawieraj�ca bramki symulowanego uk�adu
num = 0

# funkcje wstawiaj�ce bramki do symulowanego uk�adu

def NAND(wy,*we):
  UKLAD.append(('_nand',wy,we))


def AND(wy,*we):
  UKLAD.append(('_and',wy,we))


def NOR(wy,*we):
  UKLAD.append(('_nor',wy,we))


def OR(wy,*we):
  UKLAD.append(('_or',wy,we))


def XOR(wy,*we):
  UKLAD.append(('_xor',wy,we))


def NOT(wy,we):
  UKLAD.append(('_not',wy,we))



STAN = {}  # s�wnik stan�w symulowanego uk�adu

STAN['1'] = 1  # sta�y stan jedynki logicznej
STAN['0'] = 0  # sta�y stan zera logicznego

# funkcje obliczaj�ce stany na wyj�ciach bramek symulowanego uk�adu

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


# prosta realizacja wej�� w symulowanym uk�adzie

def inputs():
  if msvcrt.kbhit():
    k = msvcrt.getch().decode('utf-8')
    if k in STAN:
      STAN[k]=1-STAN[k]


# prosta wizualizacja wyj�� w symulowanym uk�adzie

def outputs():
  for k in STAN.keys():
    if k in "abcdefghijklmnopqrstuvwxyz":
      print(STAN[k],' ',end ='')
  print()


# utworzenie zmiennych, kt�re b�d� wizualizowane

def variables(*v):
  for x in v:
    STAN[x] = 0


# tworzenie punktu ��cz�cego wyj�cie bramki z innymi wej�ciami
def pin():
  global num
  num+=1
  v = f'p{num}'
  STAN[v] = 0
  return v


# funkcja wykonuj�ca symulacj�
def sim():
  t1 = time.time()

  while True:
    inputs()    # odczytanie stanu wej��
    # realizacja zegara jako punktu 'z'
    if time.time()-t1>0.5:       # 0.5 sek to po�owa okresu zegara
      STAN['z'] = 1-STAN['z']
      t1 = time.time()
    
    # obliczanie stanu wyj�� bramek
    for el in UKLAD:
      eval(el[0])(el[1],el[2])

    outputs()  # wypisywanie stanu wyj��


variables('a','b','c','d','e','z')


# realizacja przerzutnika asynchronicznego RS
def RS(a,b,c,d):
  NAND(c,a,d)
  NAND(d,b,c)


# realizacja przerzutnika synchronicznego JK master-slave
def JK(clk,clr,j,k,q,nq):
  p1 = pin()
  p2 = pin()
  p3 = pin()
  p4 = pin()
  p5 = pin()
  p6 = pin()
  nclk = pin()
  NOT(nclk,clk)
  NAND(p1,j,clk,nq)
  NAND(p2,k,q,clk)
  NAND(p3,p1,p4)
  NAND(p4,p2,p3,clr)
  NAND(p5,p3,nclk)
  NAND(p6,p4,nclk)
  NAND(q,p5,nq)
  NAND(nq,p6,q,clr)


# realizacja przerzutnika synchronicznego D zmienianego zboczem narastaj�cym
def D2(clk,clr,d,q,nq):
  p1 = pin()
  p2 = pin()
  p3 = pin()
  p4 = pin()
  NAND(p1,p2,p3)
  NAND(p2,d,p4)
  NAND(p3,p1,clk,clr)
  NAND(p4,p2,p3,clk)
  NAND(q,p3,nq)
  NAND(nq,p4,q,clr)


# realizacja Przerzutnika D z przerzutnika JK
def D(clk,clr,d,q,nq):
  p1 = pin()
  NOT(p1,d)
  JK(clk,clr,d,p1,q,nq)


# realizacja COUNTERa 4 bitowego
def COUNTER16(clk,clr,q3,q2,q1,q0):
  JK(clk,clr,"1","1",q0,pin())
  JK(q0,clr,"1","1",q1,pin())
  JK(q1,clr,"1","1",q2,pin())
  JK(q2,clr,"1","1",q3,pin())



# realizacja COUNTERa modulo 10
def COUNTER10(clk,clr,q0,q1,q2,q3):
  p = pin()
  nq3 = pin()
  JK(clk,clr,"1","1",q0,pin())
  JK(q0,clr,nq3,"1",q1,pin())
  JK(q1,clr,"1","1",q2,pin())
  JK(q0,clr,p,"1",q3,nq3)
  AND(p,q1,q2)


# realizacja 4 bitowego rejestru szeregowego
def REJ4(clk,clr,we,q0,q1,q2,q3):
  D(clk,clr,we,q0,pin())
  D(clk,clr,q0,q1,pin())
  D(clk,clr,q1,q2,pin())
  D(clk,clr,q2,q3,pin())


# realizacja przerzurniak typu LATCH
def LATCH(clk,d,q,nq):
  p1 = pin()
  p2 = pin()
  NAND(p1,clk,d)
  NAND(p2,clk,p1)
  NAND(q,p1,nq)
  NAND(nq,p2,q)


# NOT("b","a")
# XOR('d','a','b','c')
# AND('c','a','b')
XOR('c','a','b')
# XOR3('d','a','b','c')

# RS('a','b','c','d')

# JK('z','1','1','c','d')

# D('z','a','e','d','e')

# COUNTER16('z','1','a','b','c','d')
# NAND('e','c','a')

# COUNTER10('z','1','d','c','b','a')

# p1 = pin()
# REJ4('z','1',p1,'a','b','c','d')
# NOT(p1,'d')

# LATCH('c','d','e','f')

sim()

