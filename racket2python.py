from lark import Lark

my_grammar = """
?start: exp+

?exp: s_exp | atom | func 
?s_exp: "(" exp+ ")" | exp

?atom: var | num
num: NUMBER
var: /[A-Za-z]+/

?func: math
        | library 
        | definition 
        | bool 
        | map 
        | cond 
        | if_then

?library: car | cdr | list | cons | lambda
?arg: atom | func

math: "+" (atom | s_exp)+ -> add
    | "-" (atom | s_exp)+ -> sub
    | "*" (atom | s_exp)+ -> mul
    | "/" (atom | s_exp)+ -> div

bool: "<" exp exp -> lt
    | "<=" exp exp  -> lte
    | ">" exp exp -> gt
    | ">=" exp exp -> gte
    | "==" exp exp -> eq
    | "eq?" exp exp-> eq
    | "null?" exp  -> nl


car: "car" list
cdr: "cdr" list
list: "'(" atom* ")" | "(list " atom+ ")"
cons: "cons " atom (atom|list)

definition: "define (" def_init ")" exp 
def_init : var arg*

lambda: "lambda (" var+ ") (" exp ")"

if_then: "if (" bool ")" exp exp

map: "map (" func list ")"

cond: "cond" s_exp+

%import common.NUMBER
%import common.WS
%ignore WS
"""

function_dict = {}

def translate(t, indlev = 0):
    ind = '    ' * indlev
    if t.data == 's_exp' or t.data == 'start':
        #user defined funcs
        if translate(t.children[0]) in function_dict:
            params = [translate(child) for child in t.children]
            return ind + params[0] + '(' + ', '.join(params[1:]) + ')'
        
        answer = ''
        for c in t.children:
            trans = translate(c,indlev)
            answer += trans + '\n'
        return answer

    #atom
    elif t.data == 'num' or t.data == 'var':
        return ''.join(t.children[0])
    
    #boolean
    elif t.data == 'nl':
        return ind + translate(t.children[0], indlev) + " is None"
    elif t.data == 'lt':
        return ind + translate(t.children[0], indlev) + " < " + translate(t.children[1]) 
    elif t.data == 'lte':
        return ind + translate(t.children[0], indlev) + " <= " + translate(t.children[1]) 
    elif t.data == 'gt':
        return ind + translate(t.children[0], indlev) + " > " + translate(t.children[1]) 
    elif t.data == 'gte':
        return ind + translate(t.children[0], indlev) + " >= " + translate(t.children[1]) 
    elif t.data == 'eq':
        return ind + translate(t.children[0], indlev) + " == " + translate(t.children[1])
    
    #math
    elif t.data == 'add':
        return ind + '(' + translate(t.children[0]) + ' + ' + translate(t.children[1]) + ')'
    elif t.data == 'sub':
        return ind + '(' + translate(t.children[0]) + ' - ' + translate(t.children[1]) + ')'
    elif t.data == 'mul':
        return ind + '(' + translate(t.children[0]) + ' * ' + translate(t.children[1]) + ')'
    elif t.data == 'div':
        return ind + '(' + translate(t.children[0]) + ' / ' + translate(t.children[1]) + ')'
    
    #list, car, cdr
    elif t.data == 'list':
        new = []
        ret = map(translate, t.children)
        for i in ret:
            new.append(i)
        return ind + "[" + ', '.join(new) + "]"
    elif t.data == 'car':
        ls = t.children[0]
        return ''.join(ind + "car(" + translate(t.children[0], 0) + ")")
    elif t.data == 'cdr':
        ls = t.children[0]
        return ''.join(ind + "cdr(" + translate(t.children[0], 0) + ")")
    
    #lambda
    elif t.data == 'lambda':
        length = len(t.children)
        params = ', '.join(translate(c) for c in t.children[:length-1])
        return ind + 'lambda ' + params + ' : ' + translate(t.children[length-1], 0)
    
    #cond
    elif t.data == 'cond':
        code = ''    
        for i, child in enumerate(t.children):
            if i == 0:
                ret = ''.join(ind + '    return ' + (translate(child.children[1], indlev+1)).lstrip())
                code += '    ' + 'if ' + translate(child.children[0], 0) + ':\n' + ret + '\n' 
            else:
                ret = ''.join(ind + '    return ' + (translate(child.children[1], indlev+1)).lstrip())   
                code += ind + 'elif ' + translate(child.children[0], 0) + ':\n' + ret + '\n'
        return code
    
    #if then else
    elif t.data == 'if_then':
        condition, true_clause, false_clause = t.children
        if true_clause.data == 's_exp' and len(true_clause.children) > 1:
            t_ret =  ('\n').join(translate(c, indlev+1) for c in true_clause.children)
        elif len(true_clause.children) > 1:
            t_ret = translate(true_clause, indlev+1)
        else:
            t_ret = ''.join(ind + '    return ' + translate(true_clause, indlev+1).lstrip())

        if false_clause.data == 's_exp' and len(false_clause.children) > 1:
            f_ret =  ('\n').join(translate(c, indlev+1) for c in false_clause.children)
        elif len(false_clause.children) > 1:
            f_ret = translate(false_clause, indlev+1)
        else:
            f_ret = ''.join(ind + '    return ' + translate(false_clause, indlev+1).lstrip())
        return ''.join(ind + 'if' + ' (' + translate(condition, 0) + '):\n' +  t_ret + '\n' + ind + 'else:\n'  + f_ret)

    #define
    elif t.data == 'definition':
        if len(t.children[1].children) > 1:
            ret = ''.join(ind + translate(t.children[1], indlev+1))
        else:
            ret = ''.join(ind  + '    return ' + (translate(t.children[1], indlev+1)).lstrip())

        function_dict[translate(t.children[0])[0]] = [translate(t.children[0]), translate(t.children[1])] #save into function library

        return ''.join(ind + 'def ' + translate(t.children[0], 0) + ret)
    
    elif t.data == 'def_init':
        params = [translate(child) for child in t.children]
        return ''.join(ind + params[0] + '(' + ', '.join(params[1:]) + '):\n' )

    else:
        raise SyntaxError('translate: unknown function')


parser = Lark(my_grammar)

user_input = input("Enter racket program: ")
parse_tree = parser.parse(user_input)

print("\npython:\n\n")
print(translate(parse_tree))

