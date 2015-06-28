from expression_template import *

class FuncNode(Expression):
    """A node in the expression tree representing a function."""
    numargs = 1
    precedence = 15

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

    def tex(self):
        return r'\mathrm{'+self.name+r'}\!\left('+", ".join([arg.tex() for arg in self.args])+r'\right)'

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
            argVals = [str(num(arg)) for arg in newArgs]
            return Constant(eval(self.func+'('+','.join(argVals)+')')) #polygamma was behaving weird, so I decided to do it this way
        return self.__class__(*newArgs)

class SinNode(FuncNode):
    """Represents the sine function"""
    funcList.append("SinNode")
    name = 'sin'
    func = 'cmath.sin'

    def __init__(self, arg):
        super(SinNode, self).__init__(arg)

    def diff(self,var):
        return CosNode(self.args[0])*self.args[0].diff(var)

class ArcSinNode(FuncNode):
    """Represents the arcsine function"""
    funcList.append("ArcSinNode")
    name = 'arcsin'
    func = 'cmath.asin'
    def __init__(self, arg):
        super(ArcSinNode, self).__init__(arg)

    def diff(self, var):
        return ((Constant(1)-self.args[0]*self.args[0])**Constant(-0.5))*self.args[0].diff(var)

class CosNode(FuncNode):
    """Represents the cosine function"""
    funcList.append("CosNode")
    name = 'cos'
    func = 'cmath.cos'
    def __init__(self, arg):
        super(CosNode, self).__init__(arg)

    def diff(self, var):
        return Constant(-1)*SinNode(self.args[0])*self.args[0].diff(var)

class ArcCosNode(FuncNode):
    """Represents the arccosine function"""
    funcList.append("ArcCosNode")
    name ='arccos'
    func = 'cmath.acos'
    def __init__(self, arg):
        super(ArcCosNode, self).__init__(arg)

    def diff(self,var):
        return (Constant(-1)*(Constant(1)-self.args[0]*self.args[0])**Constant(-0.5))*self.args[0].diff(var)

class TanNode(FuncNode):
    """Represents the tan function"""
    funcList.append("TanNode")
    name= 'tan'
    func = 'cmath.tan'
    def __init__(self, arg):
        super(TanNode, self).__init__(arg)

    def diff(self,var):
        return CosNode(self.args[0])**Constant(-2)*self.args[0].diff(var)

class ArcTanNode(FuncNode):
    """Represents the arctan function"""
    funcList.append("ArcTanNode")
    name ='arctan'
    func = 'cmath.atan'
    def __init__(self, arg):
        super(ArcTanNode, self).__init__(arg)

    def diff(self,var):
        return self.args[0].diff(var)/(self.args[0]**2+1)

class LogNode(FuncNode):
    """Represents the logarithm"""
    funcList.append("LogNode")
    name = 'log'
    func = 'cmath.log'
    numargs = 2
    def __init__(self, arg1, arg2):
        super(LogNode, self).__init__(arg1, arg2)

    def diff(self,var):
        return (LnNode(args[0])/LnNode(args[1])).diff(var)

class LnNode(FuncNode):
    """Represents the natural logarithm"""
    funcList.append("LnNode")
    name = 'ln'
    func = 'cmath.log'
    def __init__(self, arg):
        super(LnNode, self).__init__(arg)

    def diff(self,var):
        return self.args[0].diff(var)/self.args[0]

class ExpNode(FuncNode):
    """Represents the exponent function"""
    name = 'exp'
    func = 'cmath.exp'
    funcList.append("ExpNode")
    def __init__(self, arg):
        super(ExpNode, self).__init__(arg)

    def diff(self, var):
        return self*self.args[0].diff(var)

class FloorNode(FuncNode):
    """Represents the floor function"""
    funcList.append("FloorNode")
    name = 'floor'
    func = 'math.floor'

    def __init__(self, arg):
        super(FloorNode, self).__init__(arg)

class GammaNode(FuncNode): #feature request from Aldo
    """Represents the gamma function"""
    name = 'gamma'
    func = 'math.gamma'
    funcList.append("GammaNode")
    def __init__(self,arg):
        super(GammaNode,self).__init__(arg)

    def diff(self,var):
        return GammaNode(self.args[0])*PolyGammaNode(Constant(0),self.args[0])*self.args[0].diff(var)

class PolyGammaNode(FuncNode):
    """Represents the polygamma function"""
    name = 'polygamma'
    func = 'special.polygamma'
    numargs=2
    funcList.append("PolyGammaNode")

    def __init__(self,arg1,arg2):
        super(PolyGammaNode,self).__init__(arg1, arg2)

    def diff(self,var):
        return PolyGammaNode(self.args[0]+Constant(1),self.args[1])*self.args[1].diff(var)

