import math
from expression_template import *

class FuncNode(Expression):
    """A node in the expression tree representing a function."""
    
    def __init__(self, func, name, *args):
        self.func=func
        self.name=name
        self.args=args
        
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        return '%s(%s)' % (self.name, str(self.arg))
    
    #allow for evaluation
    def __float__(self): #let eval figure out what the op_symbol does on floats
        return self.func(*map(float,args))

    def __int__(self): #let eval figure out what the op_symbol does on ints
        return int(self.func(*map(float,args)))
    
    def evaluate(self,dic={}): #let eval figure out what the op_symbol means for evaluation
        return self.func(*[arg.evaluate(dic) for arg in self.args])
        
class SinNode(FuncNode):
    """Represents the sine function"""
    def __init__(self, arg):
        super(SinNode, self).__init__(math.sin, 'sin', arg)  
        
class ArcSinNode(FuncNode):
    """Represents the sine function"""
    def __init__(self, arg):
        super(ArcSinNode, self).__init__(math.asin, 'sin', arg)         
       
class CosNode(FuncNode):
    """Represents the cosine function"""
    def __init__(self, arg):
        super(CosNode, self).__init__(math.cos, 'cos', arg)
        
class ArcCosNode(FuncNode):
    """Represents the arccosine function"""
    def __init__(self, arg):
        super(ArcCosNode, self).__init__(math.acos, 'arccos', arg)         

class TanNode(FuncNode):
    """Represents the tan function"""
    def __init__(self, arg):
        super(TanNode, self).__init__(math.tan, 'tan', arg)               
        
        
class LogNode(FuncNode):
    """Represents the logarithm"""
    def __init__(self, arg):
        super(LogNode, self).__init__(math.log, 'log', arg, base=math.e)
class ExpNode(FuncNode):
    """Represents the exponent function"""
    def __init__(self, arg):
        super(ExpNode, self).__init__(math.exp, 'exp', arg)
        
 




