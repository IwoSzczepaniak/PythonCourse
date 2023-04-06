import string

def gen(n):
    if n==0:
        yield ""
    else:
        for c in gen(n-1):
            yield c+'0'
            yield c+'1'

for s in gen(4):
    print(s)

def perm(s):
    '''Funkcja generuje permutacje liter w napisie s'''
    if len(s)==1:
        yield s
    else:
        for p in perm(s[:-1]):
            for i in range(len(s)):
                yield p[:i]+s[-1]+p[i:]

# for a in perm("abca"):
#     print(a)


def komb(s,k):
    if k==1:
        for x in s: yield x
    elif len(s)==k:
        yield s
    else:
        for x in komb(s[1:],k): yield x
        for x in komb(s[1:],k-1): yield s[0]+x

# for a in komb("ABAA", 2):
#     print(a)

def war(s,k):
    for ko in komb(s,k):
        for p in perm(ko):
            yield p

# for w in war('ABCDE',3):
#     print(w)


# !! DOCZYTAĆ O WYRAŻENIACH COEXPRESSION !!