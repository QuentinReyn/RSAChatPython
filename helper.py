import random,base64

'''
Algorithme d'Euclide pour déterminer le plus grand diviseur commun
source : https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Algorithme étendu d'Euclide pour trouver l'inverse multiplicatif de deux nombres
source : https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
'''
def multiplicative_inverse(e, p):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = p

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + p


'''
Fonction pour vérifier si le nombre est premier.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

'''
Convertir un texte en base64
'''
def convert_to_base64(decimal):
    y=str(decimal).encode('ascii')
    return base64.b64encode(y).decode('ascii')