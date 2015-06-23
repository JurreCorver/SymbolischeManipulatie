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

def stringToNode(func, exp):
    funcSplit=func.split('(')
    funcname = funcSplit[0]
    funcSplit= funcSplit[1].split(')')
    args = funcSplit[0].split(',')
    print(funcname)
    print(args)
    argDic={}
    for arg in args:
        argDic.update((Variable(arg):arg)) 
# 'f(x,y,z):=sin(x)*y*z'
# lambda x,y,z: SinNode(x)*y*z
stringToNode('f(x,y,z)','x*y*z')
sin = lambda self,x,y: SinNode(x)*SinNode(y)
addUserNode('NewClass','sin',sin)
x = NewClass(Constant(math.pi),Constant(math.pi))

