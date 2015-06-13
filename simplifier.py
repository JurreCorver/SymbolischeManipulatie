from expression_template import *

#Give standard values
BinaryNode.comm = False
BinaryNode.hasUnit = False
BinaryNode.hasZero = False

#Define commutativity for additon node
AddNode.comm = True
MulNode.comm = True

#Define unit for several nodes
#hasUnit is necessary because the mod operator does not have a unit
AddNode.unit = Constant(0)
AddNode.hasUnit = True
MulNode.unit = Constant(1)
MulNode.hasUnit = True
SubNode.unit = Constant(0)
SubNode.hasUnit = True
PowNode.unit = Constant(1)
PowNode.hasUnit = True
DivNode.unit = Constant(1)
DivNode.hasUnit = True

#Define zero for multiplication and power
MulNode.hasZero = True
MulNode.zero = Constant(0)
MulNode.zeroOp = Constant(0) #a*0 = 0
PowNode.hasZero = True
PowNode.zero = Constant(0)
PowNode.zeroOp = Constant(1) #a**0 = 1     

def subtoadd(node):
    if not type(node)==SubNode: #Check if the supplied node really is a SubNode
        if issubclass(type(node),BinaryNode):
            return node.__class__(subtoadd(node.lhs),subtoadd(node.rhs))
        else: return node
    else:
        return AddNode(subtoadd(node.lhs),Constant(-1)*subtoadd(node.rhs))

def addtosub(node): #replace a+(-b)*c with a-b*c
    if type(node)!=AddNode:
        if issubclass(type(node),BinaryNode):
            return node.__class__(addtosub(node.lhs),addtosub(node.rhs))
        else: return node
    else:
        if type(node.rhs)==MulNode:
            rhs = node.rhs.rhs.evaluate()
            lhs = node.rhs.lhs.evaluate()
            if type(rhs)==float and rhs < 0:
                return SubNode(addtosub(node.lhs),Constant(-rhs)*addtosub(node.rhs.lhs))
            if type(lhs)==float and lhs<0:
                return SubNode(addtosub(node.lhs),Constant(-lhs)*addtosub(node.rhs.rhs))
        elif type(node.lhs)==MulNode:
            rhs = node.lhs.rhs.evaluate()
            lhs = node.lhs.lhs.evaluate()
            if type(rhs)==float and rhs < 0:
                return SubNode(addtosub(node.rhs),Constant(-rhs)*addtosub(node.rhs.lhs))
            elif type(lhs)==float and lhs < 0:
                return SubNode(addtosub(node.rhs),Constant(-lhs)*addtosub(node.rhs.rhs))
        return AddNode(addtosub(node.lhs),addtosub(node.rhs))

def removeUnits(node):
    if issubclass(type(node),BinaryNode):
        if node.hasUnit:
            rhs = node.rhs.evaluate()
            lhs = node.lhs.evaluate()
            if rhs==node.unit.evaluate():
                return removeUnits(node.lhs)
            if lhs==node.unit.evaluate():
                return removeUnits(node.rhs)
        return node.__class__(removeUnits(node.lhs),removeUnits(node.rhs))
    else:
        return node

def removeZero(node):
    if issubclass(type(node),BinaryNode):
        if node.hasZero:
            lhs = node.lhs.evaluate()
            rhs = node.rhs.evaluate()
            if lhs==node.zero.evaluate():
                return node.zeroOp
            if rhs==node.zero.evaluate():
                return node.zeroOp
        return node.__class__(removeZero(node.lhs),removeZero(node.rhs))
    else:
        return node      

def isMultiple(exp1,exp2):
    x = exp1
    y = exp2
    if type(x)==MulNode: #if x = a*s with s Constant, replace x with s*a
        lhs = x.lhs.evaluate()
        rhs = x.rhs.evaluate()
        if type(lhs)!=float and type(rhs)==float:
            x = MulNode(Constant(rhs),x.lhs)
    if type(y)==MulNode:
        lhs = y.lhs.evaluate()
        rhs = y.rhs.evaluate()
        if type(lhs)!=float and type(rhs)==float:
            y = MulNode(Constant(rhs),y.lhs)

    if type(x)!=MulNode: #force form x= s*a with s a Constant
        x = MulNode(Constant(1),x)
    if type(y)!=MulNode:
        y = MulNode(Constant(1),y)
    if x.rhs.evaluate() == y.rhs.evaluate():
        if type(x.lhs.evaluate())==float and type(y.lhs.evaluate())==float:
            return (True,(Constant(float(x.lhs+y.lhs))*x.rhs))
        # return (True,simplifyStep(x.lhs+y.lhs)*x.rhs) 
    return (False, None)

def simplifyByComm(exp):    
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
            variables = []
            for node in commList:
                
                if type(node.evaluate())==float:
                    consts.append(Constant(node.evaluate()))
                elif type(node)==Variable:
                    variables.append(node)
                else:
                    compounds.append(node)

            variables.sort(key=lambda x: x.symbol)

            if type(exp)==MulNode:
                for node in variables:
                    i = variables.index(node)
                    j = 1
                    while i+1<len(variables) and variables[i]==variables[i+1]:
                        j+=1
                        del variables[i+1]
                    variables[i]=node**Constant(j)

            compounds = compounds+variables
            compounds.sort(key=variableKey)
                
            newExp = exp.unit
            for node in consts:
                newExp = Constant(float(exp.__class__(node,newExp)))
            for node in compounds:
                newExp = exp.__class__(newExp,node)
            return newExp
    return exp

def variableKey(exp):
    if type(exp)==Variable:
        return exp.symbol
    if type(exp)==PowNode:
        if type(exp.lhs)==Variable:
            return exp.lhs.symbol
    return ""
            

def simplifyStep(exp):
    exp = exp.evaluate() #try to simplify using the evaluate method. If this returns a float, stop
    if type(exp)==float:
        return Constant(exp)
    oldExp = exp
    exp = subtoadd(exp) #turn a-b into a+(-1)*b to more easily use commutativity of addition operator
    exp = removeUnits(exp) #remove unit operations
    exp = removeZero(exp) #remove zero elements
    exp = simplifyByComm(exp)
    
    if type(exp)==AddNode:
        global commList
        commList = []
        findSameChildren(exp)

        consts = []
        compounds = []
        for node in commList:
            if type(node.evaluate())==float:
                consts.append(Constant(node.evaluate()))
            else:
                compounds.append(node)

        for node in compounds:
            compounds[compounds.index(node)]=simplifyByComm(node)

        for node in compounds:
            mults = node
            compounds.remove(node)
            for exp in compounds:
                check = isMultiple(mults,exp)
                if check[0]:
                    mults = check[1]
                    compounds.remove(exp)
            compounds.insert(0,mults)
        newExp = 0
        for node in consts:
            newExp = Constant(float(AddNode(node,newExp)))
        for node in compounds:
            newExp = AddNode(newExp,node)

        exp = newExp
    exp = simplifyByComm(exp)            
    #if the expression didn't change, but it is a BinaryNode, try to simplify its children
    exp = addtosub(exp) #first remove the intentionally added minusses
    exp = removeUnits(exp) #remove accidentally added unit operations
    if exp==oldExp and issubclass(type(exp),BinaryNode):
        return exp.__class__(simplifyStep(exp.lhs),simplifyStep(exp.rhs))
    else:
        return exp

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

def simplify(exp,n=20):
    for i in range(n):
        newExp = simplifyStep(exp)
        if exp == newExp:
            break
        exp = newExp
    return exp
         
#DONE: use commutative properties, e.g. 2+x+4+2+y to 8+x+y
#DONE: support subtraction, e.g. 2+x-2+4 = 4+x
#DONE: remove units, e.g. 2+0 = 2, 2*1 = 1, 3**1 = 3
#DONE: add zeros, e.g. 2*0 = 0 and 3**0 = 1
#DONE: turn expressions like x+x into 2*x and 2+x-x into 2
#DONE: sort variables into alphabetic order
#DONE: Turn multiplications of variables into powers, e.g. x*x to x**2

#TODO: fix bug where '1+(2-3)+4', also '1+(2+-1*3)+4' does not have a bracket removed when printed
#TODO: Print integers when the values are actually integers
#TODO: Add an expand method taking e.g. (x+2)*(x-3) to x**2-x-6

def frost(str):
    return Expression.fromString(str)

#example computations         
expr = frost('5+x+5+4+5+7-1*x-5*7+12-8+0+x*(2*x+7)+y**1+0*x+y**0')
print(simplify(expr))

expr = frost('x*x+x*x+x*x*x+x*y*x+x*(a/k)*x')
print(simplify(expr))
print(simplify(frost('x*x*x+x*x')))
