from expression_template import *
from functions import *

def addUserNode(classname,funcname,exp,numargs): #add a new FuncNode with given name and function
    def __init__(self,*args): #initialization function (wonder if this is even necessary)
        if len(args)==1:
            self.args = [args[0]]
        else:
            self.args=list(args)
    def diff(self, var): #just differentiate the resultant expression after applying the function
        return eval(self.func+'(*self.args)').diff(var)
    def evaluate(self,dic={}): #first apply the function to its arguments and then evaluate normally
        return eval(self.func+'(*self.args)').evaluate(dic)

    #add a new class to the global variables
    globals()[classname] = \
        type(classname,(FuncNode,),dict())
    userClass = eval(classname) #eval(classname) gives an object representing the class
    userClass.__init__ = __init__ #overload __init__
    userClass.name = funcname #define name
    userClass.func = exp #define func (note this is always a string!)
    userClass.diff=diff #overload differentiation
    userClass.evaluate = evaluate #overload evaluate
    userClass.numargs = numargs #define the number of arguments
    funcList.append('userNodes.'+classname) #apply the function to funcList so that fromString can use it

def stringToNode(func, exp):
    funcSplit=func.split('(') #split the string into the function name and its arguments
    funcname = funcSplit[0]
    funcSplit= funcSplit[1].split(')')
    args = funcSplit[0].split(',') #put strings of the arguments in a list
    lambdaArgString = '' #create a string of arguments, e.g. 'x0,x1,x2'
    for i in range(len(args)):
        lambdaArgString+='x'+str(i)+','
    lambdaArgString=lambdaArgString[:-1] #last character is a comma, so remove it
    lambdaDicString = '{' #create a string containing a dictionary, e.g "{'x':x0,'y':x1,'z':x2}"
    for i in range(len(args)):
        lambdaDicString+='\''+args[i]+'\':x'+str(i)+','
    lambdaDicString=lambdaDicString[:-1]+'}' #last character is a comma, so remove it

    #we define the function as a lambda. this code will for example for stringToNode('f(x)','sin(x)') return:
    #(lambda x0: frost('sin(x)').evaluate({'x':x0})
    #this lambda then takes an expression object evaluates the expression above to SinNode(Variable('x')),
    #and then it uses evaluate() to replace Variable('x') with the expression given in the argument
    function = '(lambda %s: frost(\'%s\').evaluate(%s))' % (lambdaArgString, exp,lambdaDicString)

    #e.g. let our function be f(x) then we define a new FuncNode with classname UserNodef with the function
    #and expression as defined in the earlier parts of this code
    classname= 'UserNode'+funcname
    addUserNode(classname,funcname,function,len(args))

