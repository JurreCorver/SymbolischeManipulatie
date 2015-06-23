from expression_template import *

def leadingCoefficient(exp,var='x'):
    #simplify exp to the form a_n x^n + \ldots + a_0
    exp=simplify(exp)
    #if the expression consist of one term (e.g. 5x**7)
#    if isinstance(exp,)

    #split the expressions in its terms and search for the term with the degree of the expression
    terms=getCommList(exp)
    for term in terms:
        if term.deg(var)==exp.deg(var):
            #the leadingCoefficient of a constant is the constant, lhs of x**7 is x, while lhs of 5*x**7 is 5
            if isinstance(term,Constant):
                return term
            elif isinstance(term,Variable) or isinstance(term.lhs,Variable):
                return Constant(1)
            else:
                return term.lhs

def polDivMod(exp1,exp2, var='x'):
    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totdiv = Constant(0)
    while exp1.deg(var)>= exp2.deg(var):
        div = leadingCoefficient(exp1,var)/leadingCoefficient(exp2,var) * Variable(var)**(Constant(exp1.deg(var) - exp2.deg(var)))
        exp1 = simplify(exp1 - div * exp2)
        totdiv = totdiv + div
    return [simplify(totdiv), exp1]

def polDiv(exp1,exp2, var='x'):
    return polDivMod(exp1, exp2, var)[0]

def polMod(exp1, exp2, var='x'):
    return polDivMod(exp1, exp2, var)[1]