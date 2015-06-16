import math
from scipy import special

# split a string into mathematical tokens
# returns a list of numbers, operators, parantheses and commas
# output will not contain spaces
def tokenize(string):
    splitchars = list("+-*/(),%")
    
    # surround any splitchar by spaces
    tokenstring = []
    for c in string:
        if c in splitchars:
            tokenstring.append(' %s ' % c)
        else:
            tokenstring.append(c)
    tokenstring = ''.join(tokenstring)
    #split on spaces - this gives us our tokens
    tokens = tokenstring.split()
    
    #special casing for **:
    ans = []
    for t in tokens:
        if len(ans) > 0 and t == ans[-1] == '*':
            ans[-1] = '**'
        else:
            ans.append(t)
    return ans
    
# check if a string represents a numeric value
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# check if a string represents an integer value        
def isint(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
#create empty lists of binary nodes and functions. They will be filled later
binNodeList=[]
funcList=[]
    
class Expression():
    """A mathematical expression, represented as an expression tree"""
    
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
    """
    # TODO: when adding new methods that should be supported by all subclasses, add them to this list
    
    # operator overloading:
    # this allows us to perform 'arithmetic' with expressions, and obtain another expression
    def __add__(self, other):
        return AddNode(self, other)
        
    # DONE: other overloads, such as __sub__, __mul__, etc.

    def __sub__(self, other):
        return SubNode(self, other)
        
    def __mul__(self, other):
        return MulNode(self, other)
    #truediv implemented instead of div. Unsure why this works
    def __truediv__(self, other):
        return DivNode(self, other)        
        
    def __pow__(self, other):
        return PowNode(self, other)

    def __mod__(self, other):
        return ModNode(self, other)

    
    # basic Shunting-yard algorithm
    # Translates a string into an expression-tree
    def fromString(string):
        # split into tokens
        tokens = tokenize(string)
        
        # stack used by the Shunting-Yard algorithm
        stack = []
        # output of the algorithm: a list representing the formula in RPN
        # this will contain Constant's and '+'s
        output = []
        
        # list of operators
        oplist = [eval(op).op_symbol for op in binNodeList]
        preclist = [eval(op).precedence for op in binNodeList]
        asslist = [eval(op).leftass for op in binNodeList]

        #list of functions
        funcdic = {eval(func).name:eval(func) for func in funcList}
        funcnamelist = [eval(func).name for func in funcList]
        
        for token in tokens:
            if isnumber(token):
                # numbers go directly to the output
                if isint(token):
                    output.append(Constant(int(token)))
                else:
                    output.append(Constant(float(token)))
                
            elif token in funcnamelist:
                stack.append(token)

            elif token == ',':
                while not stack[-1] == '(':
                    output.append(stack.pop())
                    
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator
                while True:
                    # DONE: when there are more operators, the rules are more complicated
                    # DONE: look up the shunting yard-algorithm
                    if len(stack) == 0 or stack[-1] not in oplist:
                        break
                    tokenindex=oplist.index(token)
                    token2=stack[-1]
                    tokenindex2=oplist.index(token2)
                    if (
                        (asslist[tokenindex] and preclist[tokenindex]<=preclist[tokenindex2]) or
                        (not asslist[tokenindex] and preclist[tokenindex]< preclist[tokenindex2])
                        ):
                        output.append(stack.pop())
                    else:
                        break
                # push the new operator onto the stack
                stack.append(token)
            elif token == '(':
                # left parantheses go to the stack
                stack.append(token)
            elif token == ')':
                # right paranthesis: pop everything upto the last left paranthesis to the output
                while not stack[-1] == '(':
                    output.append(stack.pop())
                # pop the left paranthesis from the stack (but not to the output)
                stack.pop()
                if len(stack)>0 and stack[-1] in funcnamelist:
                    output.append(stack.pop())
            # TODO: do we need more kinds of tokens?
            else:
                # unknown token
                output.append(Variable(token))
            
        # pop any tokens still on the stack to the output
        while len(stack) > 0:
            output.append(stack.pop())
        
        # convert RPN to an actual expression tree
        for t in output:
            if t in funcnamelist:
                args = []
                while len(args)<funcdic[t].numargs:
                    args.append(stack.pop())
                stack.append(funcdic[t](*args[::-1])) #args seems to be in reverse order, so we have to reverse the list
            elif t in oplist:
                # let eval and operator overloading take care of figuring out what to do
                y = stack.pop()
                x = stack.pop()
                stack.append(eval('x %s y' % t))
            else:
                # a constant, push it to the stack
                stack.append(t)
        # the resulting expression tree is what's left on the stack
        return stack[0]

class DNode(Expression):
    """A node in the expression tree representing a derivative""" #Rik
    precedence = 15
    funcList.append('DNode') #works like a function, but slightly differently
    name = 'd'
    numargs = 2
    
    def __init__(self,exp, var):
        self.exp = exp
        self.var = var

    def __str__(self):
        if type(self.var)==Variable:
            return 'd(%s)/d%s' % (str(self.exp),str(self.var))
        else:
            return 'd(%s)/d(%s)' % (str(self.exp),str(self.var))

    def evaluate(self,dic={}):
        #Standard differentiation formulas for ** + * / -, constants and variables
        if self.exp == self.var:
            return Constant(1)
        
        if type(self.exp)==Variable:
            if self.exp == self.var:
                return Constant(1)
            else: return Constant(0)

        if type(self.exp)==PowNode:
            return (self.exp*(self.exp.rhs*DNode(self.exp.lhs,self.var)/self.exp.lhs+LnNode(self.exp.lhs)*DNode(self.exp.rhs,self.var))).evaluate(dic)

        if type(self.exp)==Constant:
            return Constant(0)

        if type(self.exp)==AddNode:
            return (DNode(self.exp.lhs,self.var)+DNode(self.exp.rhs,self.var)).evaluate(dic)

        if type(self.exp)==SubNode:
            return (DNode(self.exp.lhs,self.var)-DNode(self.exp.rhs,self.var)).evaluate(dic)
        
        if type(self.exp)==MulNode:
            return (DNode(self.exp.lhs,self.var)*self.exp.rhs+self.exp.lhs*DNode(self.exp.rhs,self.var)).evaluate(dic)

        if type(self.exp)==DivNode:
            return (DNode(self.exp.lhs,self.var)/self.exp.rhs - (self.exp.lhs * DNode(self.exp.rhs,self.var))/(self.exp.rhs**Constant(2))).evaluate(dic)

        if issubclass(type(self.exp),FuncNode):
            if self.exp.hasDerivative:
                if self.exp.derivativeException: #make weird functions define their own derivative
                    return self.exp.derivative(self.var)
                if self.exp.numargs==1: #just use chain rule on regular functions
                    return (self.exp.derivative()*DNode(self.exp.args[0],self.var)).evaluate(dic)

        if type(self.exp)==DNode: #have to be careful here, if we first evaluate the child expression and then take the derivative we obiously get 0
            subDNode = self.exp.evaluate()
            if type(subDNode)==DNode: #avoid infinite loops
                return DNode(subDnode,self.var)
            else:
                return DNode(subDNode,self.var).evaluate(dic)
        
        return DNode(self.exp.evaluate(dic),self.var) #do nothing if it matches none of the cases


class FuncNode(Expression):
    """A node in the expression tree representing a function."""
    numargs = 1
    precedence = 15
    hasDerivative=False
    derivativeException=False
    
    def __init__(self, *args):
        self.args=args
        
    def __eq__(self, other):
        if type(self) == type(other):
            for i in range(self.numargs):
                if self.args[i]!=other.args[i]:
                    return False
            return True
        else:
            return False
            
    def __str__(self):
        return '%s(%s)' % (self.name, ", ".join(map(str,self.args)))
    
    #allow for evaluation
    def __float__(self): #let eval figure out what the function means
        argVals = [str(float(arg)) for arg in self.args]
        return float(eval(self.func+'('+','.join(argVals)+')'))

    def __int__(self): #let eval figure out what the function means
        argVals = [str(float(arg)) for arg in self.args]
        return int(eval(self.func+'('+','.join(argVals)+')'))
    
    def evaluate(self,dic={}): #let eval figure out what the op_symbol means for evaluation
        onlyConstants = True
        newArgs = [arg.evaluate(dic) for arg in self.args]
        for arg in newArgs:
            if type(arg)!=Constant:
                onlyConstants = False
                break
        if onlyConstants:
            argVals = [str(float(arg)) for arg in newArgs]
            return Constant(eval(self.func+'('+','.join(argVals)+')')) #polygamma was behaving weird, so I decided to do it this way
        return self.__class__(*newArgs)
        
class SinNode(FuncNode):
    """Represents the sine function"""
    funcList.append("SinNode")
    name = 'sin'
    func = 'math.sin'

    def __init__(self, arg):
        super(SinNode, self).__init__(arg)

    hasDerivative = True
    def derivative(self):
        return CosNode(self.args[0])
        
class ArcSinNode(FuncNode):
    """Represents the sine function"""
    funcList.append("ArcSinNode")
    name = 'arcsin'
    func = 'math.asin'
    def __init__(self, arg):
        super(ArcSinNode, self).__init__(arg)

    hasDerivative = True
    def derivative(self):
        return (Constant(1)-self.args[0]*self.args[0])**Constant(-0.5)
       
class CosNode(FuncNode):
    """Represents the cosine function"""
    funcList.append("CosNode")
    name = 'cos'
    func = 'math.cos'
    def __init__(self, arg):
        super(CosNode, self).__init__(arg)
        
    hasDerivative = True
    def derivative(self):
        return Constant(-1)*SinNode(self.args[0])
        
class ArcCosNode(FuncNode):
    """Represents the arccosine function"""
    funcList.append("ArcSinNode")
    name ='arccos'
    func = 'math.acos'
    def __init__(self, arg):
        super(ArcCosNode, self).__init__(arg)
        
    hasDerivative = True
    def derivative(self):
        return Constant(-1)*(Constant(1)-self.args[0]*self.args[0])**Constant(-0.5)

class TanNode(FuncNode):
    """Represents the tan function"""
    funcList.append("TanNode")
    name= 'tan'
    func = 'math.tan'
    def __init__(self, arg):
        super(TanNode, self).__init__(arg)               
            
    hasDerivative = True
    def derivative(self):
        return CosNode(self.args[0])**Constant(-2) 
        
class LogNode(FuncNode):
    """Represents the logarithm"""
    funcList.append("LogNode")
    name = 'log'
    func = 'math.log'
    numargs = 2
    def __init__(self, arg1, arg2):
        super(LogNode, self).__init__(arg1, arg2)
    #need to define derivatives for two arguments first

class LnNode(FuncNode):
    """Represents the natural logarithm"""
    funcList.append("LnNode")
    name = 'ln'
    func = 'math.log'
    def __init__(self, arg):
        super(LnNode, self).__init__(arg)
            
    hasDerivative = True
    def derivative(self):
        return self.args[0]**Constant(-1)
        
class ExpNode(FuncNode):
    """Represents the exponent function"""
    name = 'exp'
    func = 'math.exp'
    funcList.append("ExpNode")
    def __init__(self, arg):
        super(ExpNode, self).__init__(arg)
            
    hasDerivative = True
    def derivative(self):
        return self

class GammaNode(FuncNode): #feature request from Aldo
    """Represents the gamma function"""
    name = 'gamma'
    func = 'math.gamma'
    funcList.append("GammaNode")
    def __init__(self,arg):
        super(GammaNode,self).__init__(arg)

    hasDerivative = True
    def derivative(self):
        return GammaNode(self.args[0])*PolyGammaNode(Constant(0),self.args[0])

class PolyGammaNode(FuncNode):
    """Represents the polygamma function"""
    name = 'polygamma'
    func = 'special.polygamma'
    numargs=2
    funcList.append("PolyGammaNode")
    
    def __init__(self,nnn,arg):
        super(PolyGammaNode,self).__init__(nnn, arg)

    hasDerivative = True
    derivativeException = True
    def derivative(self,var,dic={}):
        return PolyGammaNode(self.args[0]+Constant(1),self.args[1])*DNode(self.args[1],var).evaluate(dic)
    
def frost(string):
    return Expression.fromString(string)
    
class Constant(Expression):
    """Represents a constant value"""
    def __init__(self, value):
        self.value = value
        self.precedence = 15 #never add brackets for constants
        
    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        else:
            return False
        
    def __str__(self):
        return str(self.value)
        
    # allow conversion to numerical values
    def __int__(self):
        return int(self.value)
        
    def __float__(self):
        return float(self.value)

    def evaluate(self,dic={}):
        return self
        
class Variable(Expression):
    """Represents a variable"""
    def __init__(self, symbol):
        #TODO: check whether the value is a string
        self.symbol = symbol
        self.precedence = 15 #never add brackets for variables
        
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.symbol == other.symbol
        else:
            return False        
        
    def __str__(self):
        return self.symbol

    def evaluate(self,dic={}):
        if self.symbol in dic:
            return Constant(dic[self.symbol])
        else:
            return self
            
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""

    #define standard values for BinaryNodes
    leftass = False
    rightass = False
    precedence = 0 #always add brackets
    
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    # TODO: what other properties could you need? Precedence, associativity, identity, etc.
    # Done: precedence and associativity
            
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        lstring = str(self.lhs)
        if self.lhs.precedence<self.precedence: #add brackets if the lhs has higher precedence
            lstring = '(%s)' % lstring
        elif not self.leftass and self.lhs.precedence==self.precedence: #consider associativity
            lstring = '(%s)' % lstring
            
        rstring = str(self.rhs)
        if self.rhs.precedence<self.precedence: #add brackets if the rhs has higher precedence
            rstring = '(%s)' % rstring
        elif not self.rightass and self.rhs.precedence==self.precedence: #consider associativity
            rstring = '(%s)' % rstring
            
        return "%s %s %s" % (lstring, self.op_symbol, rstring)
    
    #allow for evaluation
    def __float__(self): #let eval figure out what the op_symbol does on floats
        return eval('float(self.lhs) %s float(self.rhs)' % self.op_symbol)

    def __int__(self): #let eval figure out what the op_symbol does on ints
        return eval('int(self.lhs) %s int(self.rhs)' % self.op_symbol)
    
    def evaluate(self,dic={}): #let eval figure out what the op_symbol means for evaluation
        l = self.lhs.evaluate(dic)
        r = self.rhs.evaluate(dic)

        if type(l)==Constant and type(r)==Constant:
            val =  eval('%s %s %s' % (float(l),self.op_symbol,float(r)))
            if float(int(val)) == val:
                return Constant(int(val))
            else:
                return Constant(val)
        else:
            return self.__class__(l,r)
        
class AddNode(BinaryNode):
    """Represents the addition operator"""
    leftass = True
    rightass = False
    precedence = 2
    op_symbol='+'
    
    binNodeList.append("AddNode")
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs) 
       
class SubNode(BinaryNode):
    """Represents the substraction operator"""
    leftass = True
    rightass = False
    precedence = 2
    op_symbol='-'

    binNodeList.append("SubNode")
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs)
        
class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    leftass = True
    rightass = True
    precedence = 3
    op_symbol='*'

    binNodeList.append("MulNode")
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs)
        
class DivNode(BinaryNode):
    """Represents the division operator"""
    leftass = True
    rightass = False
    precedence =3
    op_symbol='/'

    binNodeList.append("DivNode")
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs)
        
        
class PowNode(BinaryNode):
    """Represents the exponentiation (power) operator"""
    leftass = False
    rightass = True
    precedence = 3
    op_symbol='**'

    binNodeList.append("PowNode")
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs)

class ModNode(BinaryNode):
    """Represents the modulo opertor"""
    leftass = True
    rightass = False
    precedence = 3
    op_symbol='%'

    binNodeList.append("ModNode")
    def __init__(self,lhs,rhs):
        super(ModNode, self).__init__(lhs,rhs)
