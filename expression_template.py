import math
import cmath
from scipy import special

# split a string into mathematical tokens
# returns a list of numbers, operators, parantheses and commas
# output will not contain spaces
def tokenize(string):
    splitchars = list("+-*/(),%=")
    
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
    
    #special casing for ** and ==:
    ans = []
    for t in tokens:
        if len(ans) > 0 and t == ans[-1] == '=':
            ans[-1] = '=='
        elif len(ans) > 0 and t == ans[-1] == '*':
            ans[-1] = '**'
        else:
            ans.append(t)
    return ans
    
# check if a string represents a real number
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def num(y): #short command to make numbers looks nicer than just float() or complex()
    x=complex(y)
    if type(x)==complex and complex(x.imag)!=0:
        return x
    x = float(complex(x).real)
    if float(int(x))==float(x):
        return int(x)
    else: return float(x)
    
#create empty lists of binary nodes and functions. They will be filled later
binNodeList=[] #list of binary nodes
funcList=[] #list of functions
methodList =[] #list of methods
userVarDict = {} #dictionary for user defined variables

class InputError(Exception): #define the InputError exception to be raised in the fromString method
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


class Expression():
    """A mathematical expression, represented as an expression tree"""
    
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
     - evaluate(dict={}): evaluate expression with a dictionary
     - deg(self, var='x'): the degree of an expression (as a polynomial in var)
     - mindeg(self, var = 'x'): the lowest power of variable in self
     - diff(self, var): the derivative of the expression
    """

    precedence = 0 #by default always add brackets

    # operator overloading:
    # this allows us to perform 'arithmetic' with expressions, and obtain another expression
    def __add__(self, other):
        return AddNode(self, other)

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
    
    def tex(self): #standard conversion to TeX code is simply taking a string
        return str(self)
    
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

        #list of global methods
        metnamelist = [met[0] for met in methodList]
        metdic = {met[0]:(met[1],met[2]) for met in methodList}

        index = 0
        for token in tokens:
            if isnumber(token):
                # numbers go directly to the output
                output.append(Constant(num(token)))

            elif token == ',':
                while not stack[-1] == '(':
                    output.append(stack.pop())
                    
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator

                #add neg to the stack when encountering a - if the preceding token is a bracket or operator
                if token == '-' and (index==0 or tokens[index-1] in (['(']+oplist)):
                    stack.append('neg')
                else:
                    while True:
                        while len(stack)>0 and stack[-1]=='neg': #the previous token was a negation so add it to the output
                            output.append(stack.pop())

                        #stop if the stack is empty or the top is not an operator
                        if len(stack) == 0 or stack[-1] not in oplist:
                            break

                        #use associativity and precedence to get correct order of operations
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
                if len(output)>0 and str(output[-1]) in funcnamelist+metnamelist: #check if last item on the output is a function/method, if it is pop it from the output to the stack
                    stack.append(str(output.pop()))
                # left parantheses go to the stack
                stack.append(token)
            elif token == ')':
                # right paranthesis: pop everything upto the last left paranthesis to the output
                while not stack[-1] == '(':
                    output.append(stack.pop())
                # pop the left paranthesis from the stack (but not to the output)
                stack.pop()
                if len(stack)>0 and stack[-1] in funcnamelist+metnamelist: #if after popping the top of the stack is a function/method add it to the output
                    output.append(stack.pop())
            elif token in userVarDict: #add the value of user defined variables to the output
                output.append(userVarDict[token])
            else:
                # unknown token
                output.append(Variable(token))
            index+=1
        # pop any tokens still on the stack to the output
        while len(stack) > 0:
            output.append(stack.pop())

        # convert RPN to an actual expression tree
        for t in output:
            if t in metnamelist+funcnamelist: #check whether the token is a method/function and pop the right amount of arguments from the stack
                args = []
                if t in metnamelist: 
                    numargs = metdic[t][1]
                else:
                    numargs = funcdic[t].numargs
                while len(args)<numargs:
                    if len(stack)==0: #if the stack is empty the function has not been supplied enough arguments
                        raise InputError('%s arguments excpected of function %s' % (numargs, t))
                    args.append(stack.pop())
                if t in metnamelist: #append the function/method to the stack
                    stack.append(metdic[t][0](*args[::-1]))
                else:
                    stack.append(funcdic[t](*args[::-1]))

            #exception for neg and ==
            elif t == 'neg':
                stack.append(NegNode(stack.pop()))
            elif t == '==':
                y = stack.pop()
                x = stack.pop()
                stack.append(EqNode(x,y))
                
            elif t in oplist:
                # let eval and operator overloading take care of figuring out what to do
                y = stack.pop()
                x = stack.pop()
                stack.append(eval('x %s y' % t))
            else:
                # a constant, push it to the stack
                stack.append(t)
        # the resulting expression tree is what's left on the stack, therefore we raise an error if the stack is greater than length 1
        if len(stack)>1:
            raise InputError('Syntax error! You probably tried to use an undefined function.')
        return stack[0]


def diff(exp,var): #add diff to the list of understood methods by fromstring so that frost('d(x,y)') works
    return exp.diff(var)
methodList.append(['d',diff,2])

methodList.append(['exit',exit,0])#make it possible for the user to exit

def frost(string):
    if ':=' in string: #handle user vars/functions differently
        stringSplit = string.split(':=')
        if '(' in stringSplit[0]: #if the expression on the left of := contains a left bracket, it must be a function
            userNodes.stringToNode(*stringSplit) #add a user defined FuncNode
        else:
            userVarDict.update({stringSplit[0]:frost(stringSplit[1])}) #it's not a function so add the variable to a global dictionary
        return frost(stringSplit[1]) #return the string on the right hand side for display
    return Expression.fromString(string) #if there was ':=' just parse the string normally

def sfrost(exp): #macro for simplifying and optionally differtiating frost(string)
    return simplify(frost(exp))

    
class Constant(Expression):
    """Represents a constant value"""
    def __init__(self, value):
        self.value = value
        self.precedence = 8 #never add brackets for constants
        
    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        else:
            return False
        
    def __str__(self): #convert to strings for display
        val = num(self.value)
        if complex(val).imag == 0:
            return str(val)
        else:
            if complex(val).real!=0:
                return str(num(val.real))+' + '+str(num(val.imag))+'i'
            else:
                return str(num(val.imag))+'i'
        
    # allow conversion to numerical values
    def __int__(self):
        return int(num(self.value))
        
    def __float__(self):
        return float(num(self.value))

    def __complex__(self):
        return complex(self.value)

    def evaluate(self,dic={}):
        return self

    def diff(self,var):
        return Constant(0)


    def deg(self, var):
        #the degree of the zero polynomial is -infinity
        if self.value == 0:
            return -float("inf")
        #the degree of a constant non-zero polynomial is 0
        else:
            return 0
            
    def mindeg(self, var):
        return 0

#make it easy to type in common mathematical constants
userVarDict.update({'i':Constant(1j)}) 
userVarDict.update({'pi':Constant(math.pi)})
userVarDict.update({'e':Constant(math.e)})
userVarDict.update({'phi':Constant(0.5*(1+5**0.5))})
        
class Variable(Expression):
    """Represents a variable"""
    def __init__(self, symbol):
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
            return dic[self.symbol]
        else:
            return self

    def diff(self,var):
        if self == var:
            return Constant(1)
        else: return Constant(0)

    def deg(self, var):
       #the degree of the polynomial x is 1 w.r.t. x
       if self.symbol == var.symbol:
           return 1
       #the degree of the polynomial x is 0 w.r.t. y
       else:
           return 0
    def mindeg(self, var):
        #the degree of the polynomial x is 1 w.r.t. x
        if self.symbol == var.symbol:
            return 1
        #the degree of the polynomial x is 0 w.r.t. y
        else:
            return 0
           
class NegNode(Expression):
    """Represents the negation function"""
    precedence = 3

    def __init__(self,arg):
       self.arg = arg

    def __eq__(self, other):
        if type(self)== type(other):
            return self.arg == other.arg
        return False

    def __str__(self):
        return '-%s' % str(self.arg)

    def tex(self):
        return '-%s' % self.arg.tex()

    def __float__(self):
        return -float(self.arg)

    def __int__(self):
        return -int(self.arg)

    def __complex__(self):
        return -complex(self.arg)

    def evaluate(self,dic={}):
        arg =self.arg.evaluate(dic)
        if type(arg)==Constant:
            return Constant(-num(arg))
        return Constant(-1)*arg

    def deg(self, var):
        return self.arg.deg(var)

    def mindeg(self, var):
        return self.arg.mindeg(var)

    def diff(self,var):
        return Constant(-1)*self.arg.diff(var)

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

    def tex(self):
        lstring = self.lhs.tex()
        if self.lhs.precedence<self.precedence: #add brackets if the lhs has higher precedence
            lstring = r'\left('+lstring+r'\right)'
        elif not self.leftass and self.lhs.precedence==self.precedence: #consider associativity
            lstring = r'\left('+lstring+r'\right)'

        rstring = self.rhs.tex()
        if self.rhs.precedence<self.precedence: #add brackets if the rhs has higher precedence
            rstring = r'\left('+rstring+r'\right)'
        elif not self.rightass and self.rhs.precedence==self.precedence: #consider associativity
            rstring = r'\left('+rstring+r'\right)'

        lstring = '{%s}' % lstring
        rstring = '{%s}' % rstring

        if type(self)==MulNode and not type(self.lhs)==type(self.rhs)==Constant:
            return lstring + r'\,'+ rstring
        return "%s%s%s" % (lstring, self.tex_symbol, rstring)


    #allow for evaluation
    def __float__(self): #let eval figure out what the op_symbol does on floats
        return eval('float(self.lhs) %s float(self.rhs)' % self.op_symbol)

    def __int__(self): #let eval figure out what the op_symbol does on ints
        return eval('int(self.lhs) %s int(self.rhs)' % self.op_symbol)

    def __complex__(self): #let eval figure out what the op_symbol does on complex numbers
        return eval('complex(self.lhs) %s complex(self.rhs)' % self.op_symbol)

    def evaluate(self,dic={}): #let eval figure out what the op_symbol means for evaluation
        l = self.lhs.evaluate(dic)
        r = self.rhs.evaluate(dic)

        if type(l)==Constant and type(r)==Constant:
            val =  eval('(%s) %s (%s)' % (num(l),self.op_symbol,num(r)))
            return(Constant(num(val)))
        else:
            return self.__class__(l,r)

class AddNode(BinaryNode):
    """Represents the addition operator"""
    leftass = True
    rightass = False
    precedence = 2
    op_symbol='+'
    tex_symbol='+'

    binNodeList.append("AddNode")
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs)

    def diff(self, var='x'):
        return self.lhs.diff(var)+self.rhs.diff(var)

    def deg(self, var):
        #x**2+(-x**2) has degree -infinity
        if simplify(self.lhs+self.rhs)==Constant(0):
            return -float('inf')
        return max(self.lhs.deg(var),self.rhs.deg(var))

    def mindeg(self, var):
        if simplify(self.lhs+self.rhs)==Constant(0):
            return 0
        return min(self.lhs.mindeg(var),self.rhs.mindeg(var))



class SubNode(BinaryNode):
    """Represents the substraction operator"""
    leftass = True
    rightass = False
    precedence = 2
    op_symbol='-'
    tex_symbol='-'

    binNodeList.append("SubNode")
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self.lhs.diff(var) - self.rhs.diff(var)

    def deg(self, var):
        #x**2-x**2 has degree -infinity
        if simplify(self.lhs-self.rhs)==Constant(0):
            return -float('inf')
        return max(self.lhs.deg(var),self.rhs.deg(var))

    def mindeg(self, var):
        if simplify(self.lhs-self.rhs)==Constant(0):
            return 0
        return min(self.lhs.mindeg(var),self.rhs.mindeg(var))

class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    leftass = True
    rightass = True
    precedence = 3
    op_symbol='*'
    tex_symbol= r'\cdot'

    binNodeList.append("MulNode")
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self.lhs.diff(var)*self.rhs + self.lhs*self.rhs.diff(var)

    def deg(self, var):
        return self.lhs.deg(var)+self.rhs.deg(var)

    def mindeg(self, var):
        return self.lhs.mindeg(var)+self.rhs.mindeg(var)

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

    def deg(self, var):
        return self.lhs.deg(var)-self.rhs.deg(var)

    def mindeg(self, var):
        return self.lhs.mindeg(var)-self.rhs.mindeg(var)

    def tex(self):
        return r'\frac{'+self.lhs.tex()+ r'}{'+self.rhs.tex()+r'}'

class PowNode(BinaryNode):
    """Represents the exponentiation (power) operator"""
    leftass = False
    rightass = True
    precedence = 3
    op_symbol='**'
    tex_symbol = '^'

    binNodeList.append("PowNode")
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs)

    def diff(self, var):
        return self*(self.rhs*self.lhs.diff(var)/self.lhs+LnNode(self.lhs)*self.rhs.diff(var))

    def deg(self, var):
        #x^0 heeft graad 0
        if self.rhs.deg(var)==-float('inf'):
            return 0
        #x^2 heeft graad 2
        elif type(self.rhs.evaluate())==Constant:
            return self.lhs.deg(var)*num(self.rhs.evaluate())
        #x^x heeft geen gedefinieerde graad
        else:
            raise TypeError('%s is not a polynomial' % (self.lhs**self.rhs))

    def mindeg(self, var):
        #x^n heeft graad n als n een constant is
        if type(self.rhs.evaluate())==Constant:
            return self.lhs.mindeg(var)*num(self.rhs.evaluate())
        #x^x heeft geen goed gedefineerde graad
        else:
            raise TypeError('%s is not a polynomial' % (self.lhs**self.rhs))

class ModNode(BinaryNode):
    """Represents the modulo opertor"""
    leftass = True
    rightass = False
    precedence = 3
    op_symbol='%'
    tex_symbol = r'\,\mathrm{mod}\,'

    binNodeList.append("ModNode")
    def __init__(self,lhs,rhs):
        super(ModNode, self).__init__(lhs,rhs)

class EqNode(BinaryNode): #egg node
    """Represents the equality operator"""
    leftass=True
    rightass=True
    precedence=-1
    op_symbol = '=='
    tex_symbol = '='

    binNodeList.append("EqNode")
    def __init__(self,lhs,rhs):
        super(EqNode,self).__init__(lhs,rhs)

    def evaluate(self,dic={}): #while EqNode is a binary node, some of its methods are irregular
        return EqNode(self.lhs.evaluate(dic),self.rhs.evaluate(dic))

    def __float__(self):
        return float(self.lhs)-float(self.rhs)

    def __int__(self):
        return int(self.lhs)-int(self.rhs)

    def __complex__(self):
        return complex(self.lhs)-complex(self.rhs)

from functions import *
from simplifier import *
from numintegrate import *
from polynomials import *
from polynomialSolver import *
import userNodes #need to do a regular import to be able to refer to the global variables of userNodes.py



