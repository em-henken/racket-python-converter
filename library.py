def car(c):
    for e in c:
        return e

def cdr(c):
    c.pop(0)
    return c
        

def cons(x, l):
    if type(l)  == list:
        new = [x]
        for e in l:    
            new.append(e)
        return new
    else:
        return [x, l]
