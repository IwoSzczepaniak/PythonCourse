import string


# zad 1
def check(exp):
    var = string.ascii_lowercase
    opp = ['&', '|', '>']
    brackets = ['(', ')']
    state = True
    # True - waiting for var or opening bracket
    # False - waiting for operator or closing bracket

    i = 0
    for j in range(len(exp)):
        # brackets
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


def test_check():
    assert check("a&b>c|d") == True
    assert check("(a|b") == False
    assert check("a&b|>c") == False


# zad 2
def bracket(w):
    if not check(w): return ""
    while w[0] == '(' and w[-1] == ')' and check(w[1:-1]):
        w = w[1:-1]
    return w


def test_bracket():
    assert bracket("(a)") == "a"
    assert bracket("((a&b))") == "a&b"
    assert bracket("(a&b)|c") == "(a&b)|c"


# zad 3
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


def test_bal():
    assert bal("a&b>c", [">"]) == 3
    assert bal("(a&b)|c", ["&", "|"]) == 5
    assert bal("a&b", ["&"]) == 1


# zad 4
def onp(w):
    w = bracket(w)
    p = bal(w, '>')
    if p: return onp(w[:p]) + onp(w[p + 1:]) + w[p]
    p = bal(w, ['&', '|'])
    if p: return onp(w[:p]) + onp(w[p + 1:]) + w[p]
    return w


def test_onp():
    assert onp("a&b") == "ab&"
    assert onp("a>b>c") == "ab>c>"
    assert onp("(a>(b|c))") == "abc|>"
    assert onp("a>(b|c))") == ""


# zad 5
def map(exp, vec):
    var = string.ascii_lowercase
    res = ""

    i = 0
    val_dict = dict()
    for el in exp:
        if el in var:
            if el not in val_dict:
                if i == len(vec):
                    # print(f"Error in {exp} for args: '{vec}' - not enough arguments")
                    return False
                val_dict[el] = vec[i]
                i += 1
            res += val_dict[el]

        else:
            res += el
    if i < len(vec) and len(exp) > 0: print(f"Warning: to many arguments in {exp}")
    return res


def test_map():
    assert map('a&b', '11') == '1&1'
    assert map('a>b&c', '101') == '1>0&1'
    assert map('a>b&a', '10') == '1>0&1'
    assert map('a>b&c', '10') == False


# zad6
def gen(n):
    ret = []
    for i in range(1, 2 ** n):
        s = bin(i)[2:]
        s = '0' * (n - len(s)) + s
        ret.append(s)
    return ret


# zad 7
def val(expr):
    values = ['0', '1']
    stack = []
    while len(expr) > 0:
        el = expr[:1]
        expr = expr[1:]
        if el in values:
            stack.append(el)
        else:
            second = bool(int(stack.pop()))
            first = bool(int(stack.pop()))

            if el == '&':
                ret = first and second
            elif el == "|":
                ret = first or second
            elif el == ">":
                ret = (first and second) or (not first)
            else:
                return None

            if ret:
                if len(expr) == 0:
                    return '1'
                else:
                    expr = '1' + expr
            elif not ret:
                if len(expr) == 0:
                    return '0'
                else:
                    expr = '0' + expr
    return expr


def test_val():
    assert val('10>') == '0'
    assert val("101>&") == '1'


# zad 8
def tautology(expr):
    var = string.ascii_lowercase
    args = set()
    for el in expr:
        if el in var:
            args.add(el)
    # expr = bracket(expr)
    expr = onp(expr)
    possible = gen(len(args))
    for vec in possible:
        zero_one_expr = map(expr, vec)
        if val(zero_one_expr) == '0':
            return False
    return True


def test_tautology():
    assert tautology("a^b>a") == True
    assert tautology("a|a") == True
    assert tautology("((a>b)^(b>c))>(a>c)") == True


if __name__ == '__main__':
    test_check()
    test_bracket()
    test_bal()
    test_onp()
    test_map()
    # no gen_test - should be ok
    test_val()
    test_tautology()

    while True:
        w = input(">>")
        if w == "exit":
            break
        elif check(w):
            if tautology(w): print("TAK")
            else: print("NIE")
        else:
            print("error")
