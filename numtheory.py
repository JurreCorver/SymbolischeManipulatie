from expression_template import *

def leadingCoefficient(exp,var='x'):
    terms=getCommList(simplify(exp))
    for term in terms:
        if term.deg(var)==exp.deg(var):
            return term


#def polModulo(exp1,exp2, var):
#    while exp1.deg(var)>exp2.deg(var):
