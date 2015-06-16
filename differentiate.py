from expression_template import *
from functions import *

class DNode(Expression):
    """A node in the expression tree representing a derivative"""

    #TODO: differentieren definieren voor elke node

    #We can treat this DNode almost like a FuncNode (below)
    precedence = 15
    funcList.append('DNode') #add to the list of functions for the shunting-yard algoritm
    name = 'd'
    numargs = 2

    def __init__(self,exp, var):
        self.exp = exp
        self.var = var

    def __str__(self):
        if type(self.var)==Variable:
            return 'd(%s)/d%s' % (str(self.exp),str(self.var))
        else:
            #TODO: error message
            return 'd(%s)/d(%s)' % (str(self.exp),str(self.var))

    def evaluate(self,dic={}):
        #Standard differentiation formulas for ** + * / -, constants and variables
        #if the variable to which you differentiate is the same as the function, return 1

        #Rules for differentiating a variable.
        if type(self.exp)==Variable:
            if self.exp == self.var:
                return Constant(1)
            else: return Constant(0)

        #Rule for differentiating a power
        if type(self.exp)==PowNode:
            return (self.exp*(self.exp.rhs*DNode(self.exp.lhs,self.var)/self.exp.lhs+LnNode(self.exp.lhs)*DNode(self.exp.rhs,self.var))).evaluate(dic)

        #Rules for differentiating a constant, gives 0
        if type(self.exp)==Constant:
            return Constant(0)
        #Rules for differentiating a sum
        if type(self.exp)==AddNode:
            return (DNode(self.exp.lhs,self.var)+DNode(self.exp.rhs,self.var)).evaluate(dic)
        #Rules for differentiating a subtraction
        if type(self.exp)==SubNode:
            return (DNode(self.exp.lhs,self.var)-DNode(self.exp.rhs,self.var)).evaluate(dic)
        #Rules for differentiating a multiplication -> Product Rule
        if type(self.exp)==MulNode:
            return (DNode(self.exp.lhs,self.var)*self.exp.rhs+self.exp.lhs*DNode(self.exp.rhs,self.var)).evaluate(dic)
        #Rules for differentiating a division
        if type(self.exp)==DivNode:
            return (DNode(self.exp.lhs,self.var)/self.exp.rhs - (self.exp.lhs * DNode(self.exp.rhs,self.var))/(self.exp.rhs**Constant(2))).evaluate(dic)

        #Rules for differentiating functions. These functions often have their derivative pre defined.
        if issubclass(type(self.exp),FuncNode):
            if self.exp.hasDerivative:
                if self.exp.derivativeException: #make weird functions define their own derivative
                    return self.exp.derivative(self.var)
                if self.exp.numargs==1: #just use chain rule on regular functions
                    return (self.exp.derivative()*DNode(self.exp.args[0],self.var)).evaluate(dic)

        #Add functionality for the derivative of derivatives
        if type(self.exp)==DNode: #have to be careful here, if we first evaluate the child expression and then take the derivative we obiously get 0
            subDNode = self.exp.evaluate()
            if type(subDNode)==DNode: #avoid infinite loops
                return DNode(subDnode,self.var)
            else:
                return DNode(subDNode,self.var).evaluate(dic)

        return DNode(self.exp.evaluate(dic),self.var) #do nothing if it matches none of the cases

