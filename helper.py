import random,base64
import re
from primesieve import *


def read_private_rsa_file(fileName):
   rsa = ""
   with open(fileName+'.priv') as f:
    lines = f.readlines()    
    if(str(lines[0]).lower().strip() == '---begin monrsa private key---'):
        rsa = str(lines[1])
    f.close()
   return rsa

def read_public_rsa_file(fileName):
   rsa = ""
   
   with open(fileName+'.pub') as f:
    lines = f.readlines()
    if(str(lines[0]).lower().strip() == '---begin monrsa public key---'):
        rsa = str(lines[1])
    f.close()
   return rsa

def generate_random_prime(size:int):
    return n_primes(1, random.randint(10**size, 10**(size+1)-1))[0]



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

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)