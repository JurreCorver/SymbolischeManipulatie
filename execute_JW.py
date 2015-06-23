from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp=frost('3*x**7-1-5*x**8')
exp2=simplify(exp)

print(exp)
print(exp2)
print(isinstance(exp,AddNode))
print(isinstance(exp2,AddNode))
g=getCommList(exp2)
for i in g:
    print(i)
#print(leadingCoefficient(frost('3*x')))
#print(polMod(frost('x+x**5+1+x**3'),frost('3*x')))
#print(polDiv(frost('x+x**5+1+x**3'),frost('3*x')))