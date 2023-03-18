import string


def check(exp):
    var = string.ascii_lowercase
    opp = ['&', '|', '>']
    brackets = ['(', ')']
    state = True
    # True - oczekiwanie na zmienną lub nawias otwierający
    # False - oczekiwanie na operator lub nawias domykający

    i = 0
    for j in range(len(exp)):
        # nawiasy
        if exp[j] in brackets:
            if i < 0:
                return False
            if exp[j] == '(':
                state = True
                i += 1
            elif exp[j] == ')':
                state = False
                i -= 1
        else:
            # pozostałe zasady
            if state:
                if exp[j] in var:
                    state = False
                else:
                    return False
            else:
                if exp[j] in opp:
                    state = True
                else:
                    return False

    if i == 0: return True
    return False


def bracket(w):
    while w[0] == '(' and w[-1] == ')' and check(w[1:-1]):
        w = w[1:-1]
    return w


def bal(w, op):
    j = 0
    # for el,i in enumerate (w[:-1]):
    #     if el == ')': j+=1
    #     elif el == '(': j-=1
    #     elif el in op and j == 0:
    #         return i
    for i in range(len(w) - 1, -1, -1):
        if w[i] == ')':
            j += 1
        elif w[i] == '(':
            j -= 1
        elif w[i] in op and j == 0:
            return i
    return False


def onp(w):
    w = bracket(w)
    p = bal(w, '>')
    if p: return onp(w[:p]) + onp(w[p + 1:]) + w[p]
    p = bal(w, ['&','|'])
    if p: return onp(w[:p]) + onp(w[p + 1:]) + w[p]
    return w


if __name__ == '__main__':
    while True:
        w = input(">>")
        if check(w):
            print(onp(w))
        else:
            print("error")
