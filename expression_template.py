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
     - evaluate(dict={}): evaluate expression with a dictionary
     - deg(self, var): the degree of an expression (as a polynomial in var)
    """
    # TODO: when adding new methods that should be supported by all subclasses, add them to this list

    precedence = 0 #by default always add brackets

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
        
    def __eq__(self, other):
        return EqNode(self, other)
    

    
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

#macro for Expression.fromString(string)
def frost(string):
    return Expression.fromString(string)

def sfrost(exp,d='',n=1): #macro for simplifying and optionally differtiating frost(string)
    if d!='':
        expr = frost(exp)
        for i in range(n):
            expr=simplify(expr.diff(Variable(d)))
        return expr
    else:
        return simplify(frost(exp))

    
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

    def diff(self,var):
        return Constant(0)


    def deg(self, var = 'x'):
        #the degree of the zero polynomial is -infinity
        if self.value == 0:
            return -float("inf")
        #the degree of a constant non-zero polynomial is 0
        else:
            return 0
        
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

    def diff(self,var):
        if self == var:
            return Constant(1)
        else: return Constant(0)

    def deg(self, var = 'x'):
       #the degree of the polynomial x is 1 w.r.t. x
       if self.symbol == var:
           return 1
       #the degree of the polynomial x is 0 w.r.t. y
       else:
           return 0
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""

    #define standard values for BinaryNodes
    leftass = False
    rightass = False
    precedence = 0 #always add brackets
    
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

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

    def diff(self, var):
        return self.lhs.diff(var)+self.rhs.diff(var)

    def deg(self, var= 'x'):
        return max(self.lhs.deg(var),self.rhs.deg(var))
       
class SubNode(BinaryNode):
    """Represents the substraction operator"""
    leftass = True
    rightass = False
    precedence = 2
    op_symbol='-'

    binNodeList.append("SubNode")
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self.lhs.diff(var) - self.rhs.diff(var)

    def deg(self, var= 'x'):
        return max(self.lhs.deg(var),self.rhs.deg(var))
        
class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    leftass = True
    rightass = True
    precedence = 3
    op_symbol='*'

    binNodeList.append("MulNode")
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self.lhs.diff(var)*self.rhs + self.lhs*self.rhs.diff(var)

    def deg(self, var= 'x'):
        return self.lhs.deg(var)+self.rhs.deg(var)
        
class DivNode(BinaryNode):
    """Represents the division operator"""
    leftass = True
    rightass = False
    precedence =3
    op_symbol='/'

    binNodeList.append("DivNode")
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self.lhs.diff(var)/self.rhs - (self.lhs * self.rhs.diff(var))/(self.rhs*self.rhs)

    def deg(self, var= 'x'):
        return self.lhs.deg(var)-self.rhs.deg(var)
        
class PowNode(BinaryNode):
    """Represents the exponentiation (power) operator"""
    leftass = False
    rightass = True
    precedence = 3
    op_symbol='**'

    binNodeList.append("PowNode")
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self*(self.rhs*self.lhs.diff(var)/self.lhs+LnNode(self.lhs)*self.rhs.diff(var))

    def deg(self, var = 'x'):
        #x^0 heeft graad 0
        if self.rhs.deg(var)==-float('inf'):
            return 0
        #x^2 heeft graad 2
        elif self.rhs.deg(var)==0:
            return self.lhs.deg(var)*self.rhs.value
        #x^x heeft graad oneindig
        else:
            return float('inf')

class ModNode(BinaryNode):
    """Represents the modulo opertor"""
    leftass = True
    rightass = False
    precedence = 3
    op_symbol='%'

    binNodeList.append("ModNode")
    def __init__(self,lhs,rhs):
        super(ModNode, self).__init__(lhs,rhs)

class EqNode(BinaryNode): #egg node
    """Represents the equality operator"""
    leftass=True
    rightass=True
    precedence=15
    op_symbol = '=='

    binNodeList.append("EqNode")
    def __init__(self,lhs,rhs):
        super(EqNode,self).__init__(lhs,rhs)

    def evaluate(self,dic={}):
        return EqNode(self.lhs.evaluate(dic),self.rhs.evaluate(dic))

    def __float__(self):
        return float(self.lhs)-float(self.rhs)

    def __int__(self):
        return int(self.lhs)-int(self.rhs)
    
        
from functions import *
from simplifier import *
from numintegrate import *



