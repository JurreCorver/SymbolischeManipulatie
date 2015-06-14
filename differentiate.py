from expression_template import *
from simplifier import *

class DNode(Expression):
    precedence = 15
    funcList.append('DNode')
    name = 'd'
    numargs = 2
    
    def __init__(self,exp, var):
        self.exp = exp
        self.var = var

    def __str__(self):
        return 'd(%s)/d%s' % (str(self.exp),self.var)

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

        if type(self.exp)==AddNode or type(self.exp)==SubNode:
            return self.__class__(DNode(self.exp.lhs),DNode(self.exp.rhs)).evaluate(dic)
        if type(self.exp)==MulNode:
            return (DNode(self.exp.lhs,self.var)*self.exp.rhs+self.exp.lhs*DNode(self.exp.rhs,self.var)).evaluate(dic)

        if type(self.exp)==DivNode:
            return (DNode(self.exp.lhs,self.var)/self.exp.rhs - (self.exp.lhs * DNode(self.exp.rhs,self.var))/(self.exp.rhs**Constant(2))).evaluate(dic)

        if issubclass(type(self.exp),FuncNode):
            if self.exp.hasDerivative and self.exp.numargs==1: #currently only support one variable
                return (self.exp.derivative()*DNode(self.exp.args[0],self.var)).evaluate(dic)
        

        return DNode(self.exp,self.var) #do nothing if it matches none of the cases


#define derivatives for the various classes:
print(simplify(DNode(frost('sin(2*x)'),Variable('x'))))
print(simplify(DNode(frost('ln(2*x)'),Constant(2)*Variable('x'))))


print(simplify(DNode(frost('x**a'),Variable('x')).evaluate()))
print(simplify(DNode(frost('1/x'),Variable('x'))))
