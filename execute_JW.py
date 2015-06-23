from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp2=sfrost('(x+1)*(x-2)')
exp1=sfrost('(x+1)*(x-3)')
var='x'

print(exp1,',', exp2)

totquot = Constant(0)

deg1 = exp1.deg(var)
deg2 = exp2.deg(var)
quot = coefficient(exp1,deg1, var)/coefficient(exp2,deg2,var) * Variable(var)**(Constant(exp1.deg(var) - exp2.deg(var)))
exp1 = simplify(exp1 - quot * exp2)
totquot = totquot + quot
print(simplify(frost('-3 - 2 * x - (-2 - x + x ** 2) + x ** 2')))