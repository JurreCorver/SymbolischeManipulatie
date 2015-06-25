from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp2=sfrost('(x+1)*(x-2)')
exp1=sfrost('(x+1)*(x-3)')
var='x'

print(subtoadd(frost('5-(-2 - x + x ** 2)')))
print(type(frost('(-2 - x + x ** 2)')) == AddNode and type('1')!=AddNode)
print(expand(frost('-1')))