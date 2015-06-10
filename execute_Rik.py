#mijn klad, afblijven jongens
from expression_template import *

x = Constant(2)
y = Constant(10)
z = Constant(1)
c = Variable('c')

print((c+x*y).evaluate({'c':2}))
