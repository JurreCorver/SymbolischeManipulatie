from simplifier import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
d=a/b+c*b/a+x
print(simplify(DNode(SinNode(x)**a,x).evaluate()))