#mijn klad, afblijven jongens
from expression_template import *

x = Constant(2)
y = Constant(10)

expr = Expression.fromString('2**10-24%3')
print(expr)
print(float(expr))
