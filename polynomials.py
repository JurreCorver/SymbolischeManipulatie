from expression_template import *

    #find the coefficient of a polynomial before x**deg
def coefficient(exp, deg, var):
    #simplify exp to the form a_n x^n + \ldots + a_0
    #gebruik subtoadd om aftrekken te veranderen in optellen (van een negatief getal) en trek coefficienten bij dezelfde macht samen
    exp=subtoadd(simplify(exp))

    #split the expressions in its terms and search for the term with the degree of the expression
    if isinstance(exp,AddNode):
        terms=getCommList(exp)
        ans = Constant(0)
        for term in terms:
            if term.deg(var)==deg:
                ans += term/(var**Constant(deg))
        return simplify(ans)
    #if there is only one term
    else:
        if exp.deg(var)==deg:
            return simplify(exp/(var**Constant(deg)))
        else:
            return Constant(0)

def polQuotRem(exp1,exp2, var):
    '''calculate the remainder and the quotient of exp1/exp2 over the reals'''

    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totquot = Constant(0)
    while exp1.deg(var)>= exp2.deg(var):
        deg1 = exp1.deg(var)
        deg2 = exp2.deg(var)
        quot = coefficient(exp1,deg1, var)/coefficient(exp2,deg2,var) * var**(Constant(deg1 - deg2))
        exp1 = simplify(exp1 - quot * exp2)
        totquot = totquot + quot
    return [simplify(totquot), exp1]

def polQuotRemInt(exp1, exp2, var):
    '''calculate the remainder and the quotient of exp1/exp2 over the integers'''
    #modulo 0 nothing happens
    if exp2 == Constant(0):
        return [Constant(0),exp1]

    totquot = Constant(0)
    for d in range(exp1.deg(var),exp2.deg(var)-1,-1):
        deg2 = exp2.deg(var)
        leadingcoef2=coefficient(exp2,deg2,var)
        quot = FloorNode(coefficient(exp1,d, var)/leadingcoef2) * var**(Constant(d - deg2))
        exp1 = simplify(exp1 - quot * exp2)
        totquot = totquot + quot
    return [simplify(totquot), exp1]

def polQuot(exp1,exp2, var):
    return polQuotRem(exp1, exp2, var)[0]

def polRem(exp1, exp2, var):
    return polQuotRem(exp1, exp2, var)[1]

def polQuotInt(exp1,exp2, var):
    return polQuotRemInt(exp1, exp2, var)[0]

def polRemInt(exp1, exp2, var):
    return polQuotRemInt(exp1, exp2, var)[1]

methodList.append(['polQuotient',polQuot,3])
methodList.append(['polRemainder',polRem,3])
methodList.append(['polIntQuotient',polQuotInt,3])
methodList.append(['polIntRemainder',polRemInt,3])
methodList.append(['polIntRemainder',polRemInt,3])

def gcd(exp1, exp2):
    '''calculate the gcd of two integers'''

    #check whether both exp1 and exp2 are integers
    if int(exp1) != float(exp1):
        raise ValueError('%s is not an integer' % str(exp1))
    if int(exp2) != float(exp2):
        raise ValueError('%s is not an integer' % str(exp2))

    #we can assume both integers are positive
    if int(exp1)<0:
        exp1=NegNode(exp1).evaluate()
    if int(exp2)<0:
        exp2=NegNode(exp2).evaluate()

    #during our calculations we always want exp1 > exp2
    if int(exp1)<int(exp2):
        (exp1,exp2) = (exp2, exp1)

    #subtract exp2 as much as possible from exp1
    #then it follows that the new value of exp1 is smaller than exp2, hence interchange them
    #by continuing until exp2 = 0 we find the gcd
    while int(exp2) !=0:
        newexp1 = (exp1-FloorNode(exp1/exp2)*exp2).evaluate()
        (exp1, exp2) = (exp2, newexp1)
    return exp1

def polContent(exp1,var):
    '''makes a polynomial primitive'''

    exp1=simplify(exp1)
    #content of the zero polynomial is 0
    if exp1==Constant(0):
        return Constant(0)

    #calculate the gcd of all the terms
    content = Constant(0)
    for i in range(0,exp1.deg(var)+1):
        coef=coefficient(exp1,i,var)
        content = gcd(content, coef)
    return content

def polGcd(exp1, exp2, var):
    '''calculate the gcd of two possibly constant polynomials'''

    #first calculate the gcd of the contents of the polynomials
    gcdcontents=gcd(polContent(exp1, var),polContent(exp2, var))

    if exp1.deg(var)<exp2.deg(var):
        (exp1,exp2)=(exp2,exp1)

    #calcultate the gcd of the polynomials self (over the reals)
    while exp1 != Constant(0):
        (exp1, exp2) = (exp2, polRem(exp1, exp2, var))

    #the content of the polGcd should be the gcd of the contents of the two initial polynomials
    content2=polContent(exp2,var)
    exp2=simplify(exp2/content2*gcdcontents)

    #the leading coefficient should be positive
    if int(coefficient(exp2, exp2.deg(var),var))<0:
        exp2=simplify(NegNode(exp2))
    return exp2

methodList.append(['gcd',gcd,2])
methodList.append(['polContent',polContent,2])
methodList.append(['polGcd',gcd,3])
