from expression_template import *
from functions import *



a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
d = a+b**c-x


#print(d)
#print(c)

print(Expression.fromString('5+2*3' )   )

print(LogNode(a).evaluate())

