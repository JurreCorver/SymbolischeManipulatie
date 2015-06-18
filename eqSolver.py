from expression_template import *

def solvePolynomial(eq):
    
    polyn = frost(str(eq))
    #for now, assum a x^2 + b x + c
    
    ''''print(binNodeList)
    
    cpownode = 0
    for i in range(0, len(binNodeList)):
        if binNodeList[i] == 'PowNode':
            cpownode += 1
        
    print(cpownode)'''
    
    
    print(polyn.degree('x'))
    
    
    
    
    