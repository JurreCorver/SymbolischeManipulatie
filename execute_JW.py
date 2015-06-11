from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
d=a/b+c*b/a+x
print(Expression.fromString('(5+((2))*x/(3+2))'))