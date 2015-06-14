import math

class FuncNode(Expression):
    """A node in the expression tree representing a function."""
    
    def __init__(self, *args):
        self.args=args
        
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        return '%s(%s)' % (self.name, ", ".join(map(str,self.args)))
    
    #allow for evaluation
    def __float__(self): #let eval figure out what the op_symbol does on floats
        return self.func(*map(float,args))

    def __int__(self): #let eval figure out what the op_symbol does on ints
        return int(self.func(*map(float,args)))
    
    def evaluate(self,dic={}): #let eval figure out what the op_symbol means for evaluation
        return self.func(*[arg.evaluate(dic) for arg in self.args])
        
class SinNode(FuncNode):
    """Represents the sine function"""
    funcList.append("SinNode")
    name = 'sin'
    func = math.sin
    def __init__(self, arg):
        super(SinNode, self).__init__(arg)  
        
class ArcSinNode(FuncNode):
    """Represents the sine function"""
    funcList.append("ArcSinNode")
    name = 'arcsin'
    func = math.asin
    def __init__(self, arg):
        super(ArcSinNode, self).__init__(arg)         
       
class CosNode(FuncNode):
    """Represents the cosine function"""
    funcList.append("CosNode")
    name = 'cos'
    func = math.cos
    def __init__(self, arg):
        super(CosNode, self).__init__(arg)
        
class ArcCosNode(FuncNode):
    """Represents the arccosine function"""
    funcList.append("ArcSinNode")
    name ='arccos'
    func = math.acos
    def __init__(self, arg):
        super(ArcCosNode, self).__init__(arg)         

class TanNode(FuncNode):
    """Represents the tan function"""
    funcList.append("TanNode")
    name= 'tan'
    func = math.tan
    def __init__(self, arg):
        super(TanNode, self).__init__(arg)               
        
        
class LogNode(FuncNode):
    """Represents the logarithm"""
    funcList.append("LogNode")
    name = 'log'
    func = math.log
    def __init__(self, arg):
        super(LogNode, self).__init__(arg, base=math.e)
class ExpNode(FuncNode):
    """Represents the exponent function"""
    name = 'exp'
    func = math.exp
    funcList.append("ExpNode")
    def __init__(self, arg):
        super(ExpNode, self).__init__(arg)
