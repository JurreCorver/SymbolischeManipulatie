from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp=frost('5*x**7-1-5*x**8')
exp1=simplify(exp, False)
exp2=frost('x**2')

print(exp1)
print(exp2)
print(coefficient(exp2,1,'x'))
print(polMod(exp1,exp2,'x'))
print(polDiv(exp1,exp2,'x'))