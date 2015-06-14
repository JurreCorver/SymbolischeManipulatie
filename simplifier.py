from expression_template import *

#Give standard values
BinaryNode.comm = False
BinaryNode.hasRUnit = False
BinaryNode.hasLUnit = False
BinaryNode.hasZero = False

#Define commutativity for additon node
AddNode.comm = True
MulNode.comm = True

#Define unit for several nodes
#hasUnit is necessary because the mod operator does not have a unit
AddNode.unit = Constant(0)
AddNode.hasLUnit = True
AddNode.hasRUnit = True
MulNode.unit = Constant(1)
MulNode.hasLUnit = True
MulNode.hasRUnit = True
SubNode.unit = Constant(0)
SubNode.hasLUnit = False
SubNode.hasRUnit = True
PowNode.unit = Constant(1)
PowNode.hasLUnit = False
PowNode.hasRUnit = True
DivNode.unit = Constant(1)
DivNode.hasRUnit = True
DivNode.hasLUnit = False

def num(x):
    if float(int(x))==float(x):
        return int(x)
    else: return float(x)

def subtoadd(node):
    if not type(node)==SubNode: #Check if the supplied node really is a SubNode
        if issubclass(type(node),BinaryNode):
            return node.__class__(subtoadd(node.lhs),subtoadd(node.rhs))
        else: return node
    else:
        return subtoadd(node.lhs)+Constant(-1)*subtoadd(node.rhs)

def addtosub(node): #replace a+(-b)*c with a-b*c
    if type(node)!=AddNode:
        if issubclass(type(node),BinaryNode):
            return node.__class__(addtosub(node.lhs),addtosub(node.rhs))
        else: return node
    else:
        if type(node.rhs)==MulNode:
            rhs = node.rhs.rhs.evaluate()
            lhs = node.rhs.lhs.evaluate()
            if type(rhs)==Constant and float(rhs) < 0:
                return SubNode(addtosub(node.lhs),Constant(-num(rhs))*addtosub(node.rhs.lhs))
            if type(lhs)==Constant and float(lhs)<0:
                return SubNode(addtosub(node.lhs),Constant(-num(lhs))*addtosub(node.rhs.rhs))
        elif type(node.lhs)==MulNode:
            rhs = node.lhs.rhs.evaluate()
            lhs = node.lhs.lhs.evaluate()
            if type(rhs)==Constant and float(rhs) < 0:
                return SubNode(addtosub(node.rhs),Constant(-num(rhs))*addtosub(node.rhs.lhs))
            elif type(lhs)==Constant and float(lhs) < 0:
                return SubNode(addtosub(node.rhs),Constant(-num(lhs))*addtosub(node.rhs.rhs))
        return AddNode(addtosub(node.lhs),addtosub(node.rhs))

def removeUnits(node):
    if issubclass(type(node),BinaryNode):
        if node.hasLUnit:
            if node.lhs.evaluate()==node.unit:
                return removeUnits(node.rhs)
        if node.hasRUnit:
            if node.rhs.evaluate()==node.unit:
                return removeUnits(node.lhs)
        return node.__class__(removeUnits(node.lhs),removeUnits(node.rhs))
    else:
        return node

def removeZero(node):
    if type(node)==MulNode:
        if node.lhs == Constant(0) or node.rhs==Constant(0):
            return Constant(0)
    if type(node)==PowNode:
        if node.lhs == Constant(0):
            return Constant(0)
        if node.rhs == Constant(0):
            return Constant(1)
        if node.rhs == Constant(0):
            return node.lhs
        if node.lhs == Constant(1):
            return Constant(1)
    if issubclass(type(node),BinaryNode):
        return node.__class__(removeZero(node.lhs),removeZero(node.rhs))
    return node

def isMultiple(exp1,exp2):
    x = exp1
    y = exp2
    if type(x)==MulNode: #if x = a*s with s Constant, replace x with s*a
        lhs = x.lhs.evaluate()
        rhs = x.rhs.evaluate()
        if type(lhs)!=Constant and type(rhs)==Constant:
            x = MulNode(rhs,x.lhs)
    if type(y)==MulNode:
        lhs = y.lhs.evaluate()
        rhs = y.rhs.evaluate()
        if type(lhs)!=Constant and type(rhs)==Constant:
            y = MulNode(rhs,y.lhs)

    if type(x)!=MulNode: #force form x= s*a with s a Constant
        x = MulNode(Constant(1),x)
    if type(y)!=MulNode:
        y = MulNode(Constant(1),y)
    if x.rhs.evaluate() == y.rhs.evaluate():
        if type(x.lhs.evaluate())==Constant and type(y.lhs.evaluate())==Constant:
            return (True,((x.lhs+y.lhs).evaluate())*x.rhs)
        # return (True,simplifyStep(x.lhs+y.lhs)*x.rhs) 
    return (False, None)

def isPower(exp1,exp2):
    x = exp1
    y = exp2
    if type(x)!= PowNode:
        x = x**Constant(1)
    if type(y)!= PowNode:
        y = y**Constant(1)
    if x.lhs.evaluate() == y.lhs.evaluate():
        return (True,x.lhs**(x.rhs+y.rhs).evaluate())
    else:
        return (False,None)

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
                
                if type(node.evaluate())==Constant:
                    consts.append(node.evaluate())
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
                    if j!=1:
                        variables[i]=node**Constant(j)

            compounds = compounds+variables
            if type(exp)==MulNode:
                for node in compounds:
                    mults = node
                    compounds.remove(node)
                    for x in compounds:
                        check = isPower(mults,x)
                        if check[0]:
                            mults = check[1]
                            compounds.remove(x)
                    compounds.insert(0,mults)

            compounds.sort(key=variableKey)

                
            newExp = exp.unit
            for node in consts:
                newExp = exp.__class__(node,newExp).evaluate()
            for node in compounds:
                newExp = exp.__class__(newExp,node)
            return newExp
    return exp

def factorTerms(exp):
    if type(exp)==AddNode:
        global commList
        commList = []
        findSameChildren(exp)

        consts = []
        compounds = []
        for node in commList:
            if type(node.evaluate())==Constant:
                consts.append(node.evaluate())
            else:
                compounds.append(node)

        for node in compounds:
            compounds[compounds.index(node)]=simplifyByComm(node)

        for node in compounds:
            mults = node
            compounds.remove(node)
            for x in compounds:
                check = isMultiple(mults,x)
                if check[0]:
                    mults = check[1]
                    compounds.remove(x)
            compounds.insert(0,mults)
        newExp = Constant(0)
        for node in consts:
            newExp = AddNode(node,newExp).evaluate()
        for node in compounds:
            newExp = AddNode(newExp,node)

        return newExp
    return exp

    
def variableKey(exp):
    if type(exp)==Variable:
        return exp.symbol
    if type(exp)==PowNode:
        if type(exp.lhs)==Variable:
            return exp.lhs.symbol
    return ""
            
def getCommList(exp):
    global commList
    commList = []
    findSameChildren(exp)
    return commList

def divtomul(exp):
    if type(exp)==DivNode:
        return divtomul(exp.lhs)*(divtomul(exp.rhs)**Constant(-1))
    elif issubclass(type(exp),BinaryNode):
        return exp.__class__(divtomul(exp.lhs),divtomul(exp.rhs))
    return exp

def multodiv(exp):
    if type(exp)==PowNode:
        if type(exp.rhs)==Constant and float(exp.rhs)<0:
            return Constant(1)/(exp.lhs**Constant(-num(exp.rhs)))
    if issubclass(type(exp),BinaryNode):
        return exp.__class__(multodiv(exp.lhs),multodiv(exp.rhs))
    return exp

def simplifyStep(exp):
    exp = exp.evaluate() #try to simplify using the evaluate method. If this returns a float, stop
    if type(exp)==Constant:
        return exp
    if issubclass(type(exp),FuncNode): #if the node is a function, simplify its arguments
        return exp.__class__(*[simplifyStep(arg) for arg in exp.args])
    oldExp = exp
    exp = subtoadd(exp) #turn a-b into a+(-1)*b to more easily use commutativity of addition operator
    exp = divtomul(exp)
    exp = removeUnits(exp) #remove unit operations
    exp = removeZero(exp) #remove zero elements
    exp = simplifyByComm(exp)
    exp = factorTerms(exp)
    exp = simplifyByComm(exp)            
    #if the expression didn't change, but it is a BinaryNode, try to simplify its children
    exp = addtosub(exp) #first remove the intentionally added minusses
    exp = multodiv(exp)
    exp = removeZero(exp)
    exp = removeUnits(exp) #remove accidentally added unit operations
    if exp==oldExp and  issubclass(type(exp),BinaryNode):
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

def simplify(exp,n=100):
    for i in range(n):
        newExp = simplifyStep(exp)
        if exp == newExp:
            break
        exp = newExp
    return exp

def expand(exp):
    if type(exp) == MulNode:
        if type(exp.lhs) == AddNode and type(exp.rhs)!=AddNode:
            rhs = expand(exp.rhs)
            terms = getCommList(exp.lhs)
            newExp = Constant(0)
            for term in terms:
                newExp += term*rhs
            return newExp
        if type(exp.rhs) == AddNode and type(exp.lhs)!=AddNode:
            lhs = expand(exp.lhs)
            terms = getCommList(exp.rhs)
            newExp = Constant(0)
            for term in terms:
                newExp += term*lhs
            return newExp
        if type(exp.rhs) == AddNode and type(exp.lhs)==AddNOde:
            lterms = getCommList(exp.lhs)
            rterms = getCommList(exp.rhs)
            newExp = Constant(0)
            for lterm in lterms:
                for rterm in rterms:
                    newExp+=lterm*rterm
            return newExp
    if issubclass(type(exp),BinaryNode):
        return exp.__class__(expand(exp.lhs),expand(exp.rhs))
    return exp
            
            
            
         
#DONE: use commutative properties, e.g. 2+x+4+2+y to 8+x+y
#DONE: support subtraction, e.g. 2+x-2+4 = 4+x
#DONE: remove units, e.g. 2+0 = 2, 2*1 = 1, 3**1 = 3
#DONE: add zeros, e.g. 2*0 = 0 and 3**0 = 1
#DONE: turn expressions like x+x into 2*x and 2+x-x into 2
#DONE: sort variables into alphabetic order
#DONE: Turn multiplications of variables into powers, e.g. x*x to x**2
#DONE: factorize x**a * x**b into x**(a+b)
#DONE: Add an expand method taking e.g. (x+2)*(x-3) to x**2-x-6
#DONE: Support division
#DONE: Support for functions

