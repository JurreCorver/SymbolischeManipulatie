from expression_template import *

    #find the coefficient of a polynomial before x**deg
def coefficient(exp, deg, var='x'):
    #simplify exp to the form a_n x^n + \ldots + a_0
    exp=subtoadd(simplify(exp))
    #gebruik subtoadd om aftrekken te veranderen in optellen (van een negatief getal) en trek coefficienten bij dezelfde macht samen
    #e.g. 2 x**7 + a x**7 = (2+a) x**7
    #exp=subtoadd(simplify(exp,False))
    #split the expressions in its terms and search for the term with the degree of the expression
    if isinstance(exp,AddNode):
        terms=getCommList(exp)
        ans = Constant(0)
        for term in terms:
            if term.deg(var)==deg:
                ans += term/(Variable(var)**Constant(deg))
        return simplify(ans)
    else:
        if exp.deg(var)==deg:
            return simplify(exp/(Variable(var)**Constant(deg)))
        else:
            return Constant(0)

def polQuotRem(exp1,exp2, var='x'):
    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totquot = Constant(0)
    while exp1.deg(var)>= exp2.deg(var):
        deg1 = exp1.deg(var)
        deg2 = exp2.deg(var)
        quot = coefficient(exp1,deg1, var)/coefficient(exp2,deg2,var) * Variable(var)**(Constant(deg1 - deg2))
        exp1 = simplify(exp1 - quot * exp2)
        totquot = totquot + quot
    return [simplify(totquot), exp1]

def polQuotRemInt(exp1, exp2, var='x'):
    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totquot = Constant(0)
    for d in range(exp1.deg(var),exp2.deg(var)-1,-1):
        deg2 = exp2.deg(var)
        leadingcoef2=coefficient(exp2,deg2,var)
        quot = FloorNode(coefficient(exp1,d, var)/leadingcoef2) * Variable(var)**(Constant(d - deg2))
        exp1 = simplify(exp1 - quot * exp2)
        totquot = totquot + quot
    return [simplify(totquot), exp1]

def polQuot(exp1,exp2, var='x'):
    return polQuotRem(exp1, exp2, var)[0]

def polRem(exp1, exp2, var='x'):
    return polQuotRem(exp1, exp2, var)[1]

def polQuotInt(exp1,exp2, var='x'):
    return polQuotRemInt(exp1, exp2, var)[0]

def polRemInt(exp1, exp2, var='x'):
    return polQuotRemInt(exp1, exp2, var)[1]

methodList.append(['polQuot',polQuot,3])
methodList.append(['polRem',polRem,3])
methodList.append(['polQuotInt',polQuot,3])
methodList.append(['polRemInt',polRem,3])

def polGcd(exp1, exp2, var='x'):
    while exp1 != Constant(0):
        if exp1.deg(var)<exp2.deg(var):
            (exp1,exp2)=(exp2,exp1)
        (exp1, exp2) = (exp2, polRemInt(exp1, exp2, var))
    #the leading coefficient of the polGcd should be positive
#    if coefficient(exp2, exp2.deg(var),var)
    return exp2

