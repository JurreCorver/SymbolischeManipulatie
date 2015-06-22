#mijn klad, afblijven jongens
from expression_template import *
from functions import *
from simplifier import *
from numintegrate import *

name = 'UserNode1'

def addUserNode(classname,funcname,exp):
    def __init__(self,*args):
        if len(args)==1:
            self.args = [args[0]]
        else:
            self.args=list(args)
    def diff(self, var):
        return self.exp(*self.args).diff(var)
    def evaluate(self, dic={}):
        return self.exp(*self.args).evaluate(dic)
    globals()[classname] = \
        type(classname,(FuncNode,),dict())
    eval(classname).__init__ = __init__
    eval(classname).name = funcname
    eval(classname).exp= exp
    eval(classname).diff=diff
    eval(classname).evaluate=evaluate

sin = lambda x: SinNode(x)
addUserNode('NewClass','sin',sin)
x = NewClass(Constant(math.pi))
print(x.evaluate())
    
exit()
