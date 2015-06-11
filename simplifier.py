from expression_template import *

#Give standard values for commutativity
BinaryNode.comm = False

#Define commutativity for additon node
AddNode.comm = True

#Define unit for several nodes
AddNode.unit = Constant(0)
MulNode.unit = Constant(1)
SubNode.unit = Constant(0)
PowNode.unit = Constant(1)
ModNode.unit = Constant(1) #can't really define a unit?
DivNode.unit = Constant(1)

def simplify(exp):
    exp = exp.evaluate() #try to simplify using the evaluate method. If this returns a float, stop
    if type(exp)==float:
        return Constant(exp)
    newExp = exp

    if issubclass(type(exp),BinaryNode):
        if exp.comm: #try to use commutativity

            #find all children expression of the same type
            #e.g. turn 5+3+2+x+y into a list [5,3,2,x,y]
            global commList
            commList = []
            findSameChildren(exp)

            #evaluate the operator applied to all the constants, and leave the compound expressions as-is
            consts = []
            compounds = []
            for node in commList:
                if type(node)==Constant:
                    consts.append(node)
                else:
                    compounds.append(node)

            newExp = exp.unit
            for node in consts:
                newExp = Constant(float(exp.__class__(node,newExp)))
            for node in compounds:
                newExp = exp.__class__(newExp,node).evaluate()

    #if the expression didn't change, but it is a BinaryNode, try to simplify its children
    if newExp==exp and issubclass(type(exp),BinaryNode):
        return exp.__class__(simplify(exp.lhs),simplify(exp.rhs))
    else:
        return newExp

def findSameChildren(exp):
    global commList
    if issubclass(type(exp),BinaryNode):
        if type(exp)==type(exp.lhs):
                findSameChildren(exp.lhs)
        else:
            commList.append(exp.lhs)
        if type(exp)==type(exp.rhs):
                findSameChildren(exp.rhs)
        else:
            commList.append(exp.rhs)
    else:
         commList.append(exp)

#TODO: turn expressions like x+x into 2*x
#TODO: sort variables into alphabetic order
#TODO: try to use distributive properties, e.g. 2+x-2 -> x
#TODO: fix bug where '1+(2-3)+4' does not have a bracket removed when printed

#example computations         
expr = Expression.fromString('5+x+5+4+5+7+x-5*7+12-8')
findSameChildren(expr)
for i in range(100):
    newExpr = simplify(expr)
    if expr == newExpr:
        break
    else: expr = newExpr
print(expr.evaluate())
print(simplify(expr))
print(Expression.fromString('1+(2-3)+4'))
