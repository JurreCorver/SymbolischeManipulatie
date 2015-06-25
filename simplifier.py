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

def num(x): #short command to make numbers looks nicer than just float()
    if float(int(x))==float(x):
        return int(x)
    else: return float(x)

def subtoadd(node): #convert a-b to a+(-b) to process it as if it were addition
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
                return SubNode(addtosub(node.rhs),Constant(-num(rhs))*addtosub(node.lhs.lhs))
            elif type(lhs)==Constant and float(lhs) < 0:
                return SubNode(addtosub(node.rhs),Constant(-num(lhs))*addtosub(node.lhs.rhs))
        return AddNode(addtosub(node.lhs),addtosub(node.rhs))

def removeUnits(node): #remove unit operations, e.g. 1*a = 1 or a**1 = a
    if issubclass(type(node),BinaryNode):
        if node.hasLUnit:
            if node.lhs.evaluate()==node.unit:
                return removeUnits(node.rhs)
        if node.hasRUnit:
            if node.rhs.evaluate()==node.unit:
                return removeUnits(node.lhs)
        return node.__class__(removeUnits(node.lhs),removeUnits(node.rhs)) #iterate over tree
    else:
        return node

def removeZero(node): #remove zero-like expressions
    if type(node)==MulNode: #0*a = a*0 = 0
        if node.lhs == Constant(0) or node.rhs==Constant(0):
            return Constant(0)
    if type(node)==PowNode:
        if node.lhs == Constant(0): #0**a = 0
            return Constant(0)
        if node.rhs == Constant(0): #a**0 = 1
            return Constant(1)
        if node.lhs == Constant(1): #1**a = 1
            return Constant(1)
    if issubclass(type(node),BinaryNode):
        return node.__class__(removeZero(node.lhs),removeZero(node.rhs)) #iterate over tree
    return node

def simplifyPower(node):
    if type(node)==PowNode:
        if type(node.lhs)==PowNode: #turn (a**b)**c to a**(b*c)
            return simplifyPower(node.lhs.lhs)**(simplifyPower(node.lhs.rhs)*simplifyPower(node.rhs)).evaluate()
        if type(node.lhs)==MulNode: #turn (a*b)**c to a**c * b**c
            terms = getCommList(node.lhs)
            product = Constant(1)
            for term in terms:
                product = product* term**node.rhs
            return removeUnits(product)
    elif issubclass(type(node),BinaryNode):
        return node.__class__(simplifyPower(node.lhs),simplifyPower(node.rhs))
    return node

def isMultiple(exp1,exp2): #check if two expressions are multiples of each other. 
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
            return (True,((x.lhs+y.lhs).evaluate())*x.rhs) #return True and the sum of the two
        else:
            return (True, (x.lhs+y.lhs)*x.rhs)
    return (False, None) #return False

def isPower(exp1,exp2): #check if the two expression are the same up to exponent
    x = exp1
    y = exp2
    if type(x)!= PowNode:
        x = x**Constant(1)
    if type(y)!= PowNode:
        y = y**Constant(1)
    if x.lhs.evaluate() == y.lhs.evaluate():
        return (True,x.lhs**(x.rhs+y.rhs).evaluate()) #return True with exponents added
    else:
        return (False,None) #return False

def simplifyByComm(exp): #try to use commutativity to simplify the expression
    if issubclass(type(exp),BinaryNode):
        if exp.comm: #only evaluate code if the operator is commutative (i.e. multiplication and addition only

            #find all children expression of the same type
            commList = getCommList(exp)

            #split the list into constants and compound expressions
            consts = []
            compounds = []

            for node in commList:
                if type(node.evaluate())==Constant:
                    consts.append(node.evaluate())
                else:
                    compounds.append(node)
                    
            #deprecated by code that comes after this
            # if type(exp)==MulNode: #turn expressions like x*x*x into x**3
            #     for node in variables:
            #         i = variables.index(node)
            #         j = 1
            #         while i+1<len(variables) and variables[i]==variables[i+1]:
            #             j+=1
            #             del variables[i+1]
            #         if j!=1:
            #             variables[i]=node**Constant(j)

            if type(exp)==MulNode:
                for node in compounds:
                    mults = node
                    compounds.remove(node) #remove the node
                    for x in compounds:
                        check = isPower(mults,x) #if the two are a power of each other multiply them together
                        if check[0]:
                            mults = check[1]
                            compounds.remove(x) #remove the node you just multiplied by
                    compounds.insert(0,mults) #put the product back in

            compounds.sort(key=variableKey) #sort the list of compounds

                
            newExp = exp.unit #factor out constants, start with the unit operand (e.g. 0 for addition)
            for node in consts:
                newExp = exp.__class__(node,newExp).evaluate()
            for node in compounds:
                newExp = exp.__class__(newExp,node)
            return newExp
    return exp

def factorTerms(exp): #factorize terms multiples of each other, e.g. x+x = 2*x
    if type(exp)==AddNode:
        commList = getCommList(exp) #get all the children that are also sums, i.e. get all the terms in the sum exp is part of

        #split terms in sum into constants and compound expressions
        consts = []
        compounds = []
        for node in commList:
            if type(node.evaluate())==Constant:
                consts.append(node.evaluate())
            else:
                compounds.append(node)

        for node in compounds: #simplify all the compound expressions by commutativity first
            compounds[compounds.index(node)]=simplifyByComm(node)

        for node in compounds:
            mults = node
            compounds.remove(node) #remove the current node from the queue
            for x in compounds:
                check = isMultiple(mults,x)  #for each node check if each other node is a multiple of it
                if check[0]:
                    mults = check[1] #add them together if they are
                    compounds.remove(x)
            compounds.insert(0,mults) #insert the joint term at the beginning of the queue

        compounds.sort(key=variableKey) #sort the compounds    
            
        newExp = Constant(0)
        for node in consts: #add all the constants together
            newExp = AddNode(node,newExp).evaluate()
        for node in compounds: #add the compounds back
            newExp = AddNode(newExp,node)

        return newExp
    return exp

    
def variableKey(exp): #sort key used to sort varibales and powers of variables
    if type(exp)==Variable:
        return exp.symbol
    if type(exp)==PowNode:
        if type(exp.lhs)==Variable:
            if type(exp.rhs)==Constant and float(exp.rhs)<0: #sort negative powers to the right of positive ones
                return "~" + exp.lhs.symbol # '~' is the last normal character in the ASCII table
            return exp.lhs.symbol
    return "" #return empty string to sort compound expressions to the right

def divtomul(exp): # convert a/b to a*b**-1 to be able to process the expression as if it were multiplication
    if type(exp)==DivNode:
        return divtomul(exp.lhs)*(simplifyPower(divtomul(exp.rhs)**Constant(-1)))
    elif issubclass(type(exp),BinaryNode):
        return exp.__class__(divtomul(exp.lhs),divtomul(exp.rhs))
    return exp

def multodiv(exp):
    if type(exp)==MulNode: #convert expressions like -5 * x**-1 to -5/x
        terms = getCommList(exp)
        posProd = Constant(1)
        negProd = Constant(1)
        for term in terms:
            if type(term)==PowNode and type(term.rhs)==Constant and float(term.rhs)<0:
                negProd*=term.lhs**Constant(-num(term.rhs))
            else:
                posProd*=term
        return removeUnits(posProd/negProd)
                
        # if type(exp.rhs)==PowNode and type(exp.rhs.rhs)==Constant and float(exp.rhs.rhs)<0:
        #     return exp.lhs/(multodiv(exp.rhs.lhs)**Constant(-num(exp.rhs.rhs)))
        
    if type(exp)==PowNode: #convert x**-n to 1/x**n
        if type(exp.rhs)==Constant and float(exp.rhs)<0:
            return Constant(1)/(multodiv(exp.lhs)**Constant(-num(exp.rhs)))
        
    if issubclass(type(exp),BinaryNode):#iterate over tree
        return exp.__class__(multodiv(exp.lhs),multodiv(exp.rhs))
    return exp

def multoneg(exp): #replaces expressions such as -1*x with -x
    if type(exp)==MulNode:
        if exp.lhs==Constant(-1):
            return NegNode(multoneg(exp.rhs))
    if issubclass(type(exp), BinaryNode):
        return exp.__class__(multoneg(exp.lhs),multoneg(exp.rhs))
    return exp

def simplifyStep(exp,expandEachStep=True):
    exp = exp.evaluate() #try to simplify using the evaluate method. If this returns a constant, stop
    if type(exp)==Constant:
        return exp
    if issubclass(type(exp),FuncNode): #if the node is a function, simplify its arguments
        return exp.__class__(*[simplifyStep(arg) for arg in exp.args])
    exp = subtoadd(exp) #turn a-b into a+(-1)*b to more easily use commutativity of addition operator
    exp = divtomul(exp) #turn a/b to a*b**-1
    exp = removeUnits(exp) #remove unit operations
    exp = removeZero(exp) #remove zero elements
    exp = simplifyByComm(exp) #try to use commutativity to simplify
    exp = removeUnits(exp) #remove unit operations
    exp = removeZero(exp) #remove zero elements
    exp = factorTerms(exp) #factor terms in a sum, e.g. x+x to 2*x
    exp = simplifyPower(exp) #(a**b)**c to a**(b*c)
    exp = simplifyByComm(exp) #try to use commutativity again
    if expandEachStep:
        exp = expand(exp)
        exp = removeZero(exp) #remove zeros added by the simplifier
        exp = removeUnits(exp) #remove unit operators added by the simplifier
    exp = addtosub(exp) #first remove the intentionally added minusses
    exp = multodiv(exp) #turn expressions of form b**-1 back to 1/b
    exp = removeZero(exp) #remove zeros added by the simplifier
    exp = removeUnits(exp) #remove unit operators added by the simplifier
    exp = multoneg(exp)#replace -1*a with -a
    
    if issubclass(type(exp),BinaryNode): #try to simplify its children as well
        return exp.__class__(simplifyStep(exp.lhs,expandEachStep),simplifyStep(exp.rhs,expandEachStep))
    else:
        return exp

def findSameChildren(exp): #return all the children of the tree that are of the same type of BinaryNode
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
            
def getCommList(exp): #return result of findSameChildren as a list
    global commList #a bit ugly doing it like this, but it works
    commList = []
    findSameChildren(exp)
    return commList

def simplify(exp,expandEachStep=True,n=20):#iterate simplifyStep until there is no change or maximum is exceeded
    for i in range(n):
        newExp = simplifyStep(exp,expandEachStep)
        if exp == newExp:
            break
        exp = newExp
    return exp

def expand(exp): #expand expressions of form (sum a_i)*(sum b_j)
    if type(exp) == MulNode:
        if type(exp.lhs) == AddNode and type(exp.rhs)!=AddNode: #(a+b)*c = ac+bc
            rhs = expand(exp.rhs)
            terms = getCommList(exp.lhs)
            newExp = Constant(0)
            for term in terms:
                newExp += term*rhs
            return newExp
        if type(exp.rhs) == AddNode and type(exp.lhs)!=AddNode: #a*(b+c) = ab+ac
            lhs = expand(exp.lhs)
            terms = getCommList(exp.rhs)
            newExp = Constant(0)
            for term in terms:
                newExp += term*lhs
            return newExp
        if type(exp.rhs) == AddNode and type(exp.lhs)==AddNode: #(a+b)*(c+d) = ac+ad+bc+bd
            lterms = getCommList(exp.lhs)
            rterms = getCommList(exp.rhs)
            newExp = Constant(0)
            for lterm in lterms:
                for rterm in rterms:
                    newExp+=lterm*rterm
            return newExp
    if issubclass(type(exp),BinaryNode):
        return exp.__class__(expand(exp.lhs),expand(exp.rhs)) #iterate over tree
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

#TODO: support trigoniometric properties