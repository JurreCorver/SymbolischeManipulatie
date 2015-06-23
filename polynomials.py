from expression_template import *

    #find the coefficient of a polynomial before x**deg
def coefficient(exp, deg, var='x'):
    #simplify exp to the form a_n x^n + \ldots + a_0
    exp=simplify(exp)
    #gebruik subtoadd om aftrekken te veranderen in optellen (van een negatief getal) en trek coefficienten bij dezelfde macht samen
    #e.g. 2 x**7 + a x**7 = (2+a) x**7
    exp=subtoadd(simplify(exp,False))
    #split the expressions in its terms and search for the term with the degree of the expression
    if isinstance(exp,AddNode):
        terms=getCommList(exp)
        for term in terms:
            if term.deg(var)==deg:
                return simplify(term/(Variable(var)**Constant(deg)))
        return Constant(0)
    else:
        if exp.deg(var)==deg:
            return simplify(exp/(Variable(var)**Constant(deg)))
        else:
            return Constant(0)

def polDivMod(exp1,exp2, var='x'):
    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totdiv = Constant(0)
    while exp1.deg(var)>= exp2.deg(var):
        deg1 = exp1.deg(var)
        deg2 = exp2.deg(var)
        div = coefficient(exp1,deg1, var)/coefficient(exp2,deg2,var) * Variable(var)**(Constant(exp1.deg(var) - exp2.deg(var)))
        exp1 = simplify(exp1 - div * exp2)
        totdiv = totdiv + div
    return [simplify(totdiv), exp1]

def polDiv(exp1,exp2, var='x'):
    return polDivMod(exp1, exp2, var)[0]

def polMod(exp1, exp2, var='x'):
    return polDivMod(exp1, exp2, var)[1]

methodList.append(['polDiv',polDiv,3])
methodList.append(['polMod',polMod,3])