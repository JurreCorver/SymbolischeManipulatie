import math

# split a string into mathematical tokens
# returns a list of numbers, operators, parantheses and commas
# output will not contain spaces
def tokenize(string):
    splitchars = list("+-*/(),")
    
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
        

    
    # basic Shunting-yard algorithm
    def fromString(self, string):
        # split into tokens
        tokens = tokenize(string)
        
        # stack used by the Shunting-Yard algorithm
        stack = []
        # output of the algorithm: a list representing the formula in RPN
        # this will contain Constant's and '+'s
        output = []
        
        # list of operators
        oplist = ['+']
        
        for token in tokens:
            if isnumber(token):
                # numbers go directly to the output
                if isint(token):
                    output.append(Constant(int(token)))
                else:
                    output.append(Constant(float(token)))
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator
                while True:
                    # TODO: when there are more operators, the rules are more complicated
                    # look up the shunting yard-algorithm
                    if len(stack) == 0 or stack[-1] not in oplist:
                        break
                    output.append(stack.pop())
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
            # TODO: do we need more kinds of tokens?
            else:
                # unknown token
                raise ValueError('Unknown token: %s' % token)
            
        # pop any tokens still on the stack to the output
        while len(stack) > 0:
            output.append(stack.pop())
        
        # convert RPN to an actual expression tree
        for t in output:
            if t in oplist:
                # let eval and operator overloading take care of figuring out what to do
                y = stack.pop()
                x = stack.pop()
                stack.append(eval('x %s y' % t))
            else:
                # a constant, push it to the stack
                stack.append(t)
        # the resulting expression tree is what's left on the stack
        return stack[0]
    
class Constant(Expression):
    """Represents a constant value"""
    def __init__(self, value):
        self.value = value
        self.precedence = 0 #never add brackets for constants
        
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
        
class Variable(Expression):
    """Represents a variable"""
    def __init__(self, value):
        #TODO: check whether the value is a string
        self.value = value
        self.precedence = 0 #never add brackets for variables
        
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.value == other.value
        else:
            return False        
        
    def __str__(self):
        return self.value     
        
        
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""
    
    def __init__(self, lhs, rhs, op_symbol,precedence=15,leftass=False,rightass=False):
        self.lhs = lhs
        self.rhs = rhs
        self.op_symbol = op_symbol
        
        self.precedence = precedence #the higher the precedence, the lower the 'priority' of the operator.
        self.leftass = leftass #left associativity, e.g. a/b/c = (a/b)/c != a/(b/c)
        self.rightass = rightass #right associativity, e.g. a**b**c = a**(b**c) != (a**b)**c
    
    # TODO: what other properties could you need? Precedence, associativity, identity, etc.
    # Done: precedence and associativity
            
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        lstring = str(self.lhs)
        if self.lhs.precedence>self.precedence: #add brackets if the lhs has higher precedence
            lstring = '(%s)' % lstring
        elif not self.leftass and self.lhs.precedence==self.precedence: #consider associativity
            lstring = '(%s)' % lstring
            
        rstring = str(self.rhs)
        if self.rhs.precedence>self.precedence: #add brackets if the rhs has higher precedence
            rstring = '(%s)' % rstring
        elif not self.rightass and self.rhs.precedence==self.precedence: #consider associativity
            rstring = '(%s)' % rstring
            
        return "%s %s %s" % (lstring, self.op_symbol, rstring)
        
class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+',4,True,True)
       
class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-',4,True,False)
        
class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*',3,True,False)
        
class DivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/',3,True,False)
        
class PowNode(BinaryNode):
    """Represents the exponentiation (power) operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**',2,False,True)
        
# TODO: add more subclasses of Expression to represent operators, variables, functions, etc.
