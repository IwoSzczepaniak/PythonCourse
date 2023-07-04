STAN = {}  # s�wnik stan�w symulowanego uk�adu
UKLAD = []  # lista zawieraj�ca bramki symulowanego uk�adu
num = 0

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
 

# realizacja przerzutnika asynchronicznego RS
def RS(a,b,c,d):
  NAND(c,a,d)
  NAND(d,b,c)


# realizacja przerzutnika synchronicznego JK master-slave
def JK(clk,clr,j,k,q,nq):
  # clr = not clr
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
  return "JK"


# realizacja przerzutnika synchronicznego D zmienianego zboczem narastaj�cym
def D2(clk,clr,d,q,nq):
  # clr = not clr
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
  JK(clk,clr,"true","true",q0,pin())
  JK(q0,clr,"true","true",q1,pin())
  JK(q1,clr,"true","true",q2,pin())
  JK(q2,clr,"true","true",q3,pin())



# realizacja COUNTERa modulo 10
def COUNTER10(clk,clr,q0,q1,q2,q3):
  p = pin()
  nq3 = pin()
  JK(clk,clr,"true","true",q0,pin())
  JK(q0,clr,nq3,"true",q1,pin())
  JK(q1,clr,"true","true",q2,pin())
  JK(q0,clr,p,"true",q3,nq3)
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


# tworzenie punktu ��cz�cego wyj�cie bramki z innymi wej�ciami
def pin():
  global num
  num+=1
  v = f'p{num}'
  STAN[v] = 0
  return v
