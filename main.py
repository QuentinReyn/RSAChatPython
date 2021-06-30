import base64
import random
import helper
import makeFile
import argparse
import six
from primesieve import *


def generate_key_pair_manually(p, q):
    if not (helper.is_prime(p) and helper.is_prime(q)):
        raise ValueError('Les deux nombres doivent être premiers.')
    elif p == q:
        raise ValueError('p et q ne peuvent être égaux')
    # n = pq
    n = p * q

    phi = (p-1) * (q-1)

    # Choisis un nombre entier e tel que e et phi(n) sont co-premiers.
    e = random.randrange(1, phi)

    # Utiliser l'algorithme d'Euclide pour vérifier que e et phi(n) sont premiers.
    g = helper.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = helper.gcd(e, phi)

    # Utiliser l'algorithme d'Euclide étendu pour générer la clé privée.
    d = helper.multiplicative_inverse(e, phi)

    # Retour des pairs de clés publique et privée
    # La clé publique est (e, n) et la clé privée est (d, n)
    return ((e, n), (d, n))


def generate_key_pair_auto(size):
    p = helper.generate_random_prime(size)
    q = helper.generate_random_prime(size)
    while(p == q):
        q = helper.generate_random_prime(size)

    # n = pq
    n = p * q

    phi = (p-1) * (q-1)

    # Choisis un nombre entier e tel que e et phi(n) sont co-premiers.
    e = random.randrange(1, phi)

    # Utiliser l'algorithme d'Euclide pour vérifier que e et phi(n) sont premiers.
    g = helper.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = helper.gcd(e, phi)

    # Utiliser l'algorithme d'Euclide étendu pour générer la clé privée.
    d = helper.multiplicative_inverse(e, phi)

    # Retour des pairs de clés publique et privée
    # La clé publique est (e, n) et la clé privée est (d, n)
    return ((e, n), (d, n))


def encrypt(key, string):
    enc = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(string[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decrypt(key, string:str):
    dec = []
    enc = base64.urlsafe_b64decode(string).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)



def redirect_new_key_input():
    return input("\n La clé n'est pas définie ou inconnue, veuillez la renseigner : \n")


def redirect_new_text_input():
    return input("\n Le texte a chiffrer n'est pas définie ou inconnue, veuillez le renseigner : \n")


def main(args):
    print("===========================================================================================================")
    print("================================== RSA Encryptor / Decrypter ==============================================")
    print(" ")

    commande = args.commande
    cle = args.cle
    texte = args.texte
    switchs = args.switchs
    print(switchs)
    newCle = ""
    newText = ""
    encrypted_msg = ""
    public =""
    private = ""
    if(commande == 'keygen'):
        if(switchs is not None and "-s" in switchs):
            public, private = generate_key_pair_auto(10)
        else:
            public, private = generate_key_pair_auto(10)
        if(switchs is not None and "-f" in switchs):
            makeFile.create_file_rsa("mescles", private[1], public[1])
        else:
            makeFile.create_file_rsa("mescles", private[1], public[1])

    if(switchs is not None and "-m" in switchs):
        p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
        q = int(input(" - Enter another prime number (Not one you entered above): "))
        public, private = generate_key_pair_manually(p, q)
        if(switchs is not None and "-f" in switchs):
            makeFile.create_file_rsa("mescles", private[0], public[0])
        else:
            makeFile.create_file_rsa("mescles", private[0], public[0])

    print(" - Generating your public / private key-pairs now . . .")

    print(" - Your public key is ", public,
          " and your private key is ", private)

    if(commande == "crypt"):
        if(cle is not None or cle != ""):
            while(helper.read_public_rsa_file(cle) == ""):
                print(helper.read_public_rsa_file(cle))
                cle = redirect_new_key_input()
            else:
                while(texte is None):
                    texte = redirect_new_text_input()
                else:
                    encrypted_msg = encrypt(helper.read_public_rsa_file(cle), texte)
                    print(" - Your encrypted message is: ",
                          ''.join(map(lambda x: str(x), encrypted_msg)))
        else:
            cle = redirect_new_key_input()
            while(helper.read_public_rsa_file(cle) == ""):
                cle = redirect_new_key_input()
            else:
                while(texte is None):
                    texte = redirect_new_text_input()
                else:
                    encrypted_msg = encrypt(helper.read_public_rsa_file(cle), texte)
                    print(" - Your encrypted message is: ",
                          ''.join(map(lambda x: str(x), encrypted_msg)))

    if(commande == "decrypt"):
        if(cle is not None):
            while(helper.read_private_rsa_file(cle) == ""):
                cle = redirect_new_key_input()
            else:
                while(texte is None):
                    texte = redirect_new_text_input()
                else:
                    print(" - Decrypting message with private key ", cle, " . . .")
                    print(" - Your message is: ", decrypt(helper.read_private_rsa_file(cle), texte))
        else:
            cle = redirect_new_key_input()
            while(helper.read_private_rsa_file(cle) == ""):
                cle = redirect_new_key_input()
            else:
                while(texte is None):
                    texte = redirect_new_text_input()
                else:
                    print(" - Decrypting message with private key ", cle, " . . .")
                    print(" - Your message is: ", decrypt(helper.read_private_rsa_file(cle), texte))

    print(" ")
    print("============================================ END ==========================================================")
    print("===========================================================================================================")


def helpMsg(name=None):
    return '''program.py
        Syntaxe: monRSA <commande> [<clé>] [<texte>] [switchs]
        Commandes : 
        keygen: Génére une paire de clé 
        crytp: Chiffre <texte> pour le clé publique <clé> 
        decrytp: Déchiffre <texte> pour le clé privée <clé>
        help: Affiche ce manuel
        Clé:
                  Un fichier qui contient une clé publique monRSA ('crypt') ou une clé privée ('decrypt')
        Texte: 
                  Une phrase en clair ('crypt') ou une phrase chiffrée ('decrypt') 
        Switchs : 
                  -f <file> permet de choisir le nom des clé générés, monRSA.pub et monRSA.priv par défaut")
        '''


def menu():
    """
    This method is used to check the value specified by the user in command line
    By default values of parameters are :

    :return: ArgumentParser object which contains the parameters
    """
    args = argparse.ArgumentParser(add_help=False, usage=helpMsg())
    required = args.add_argument_group('required arguments')
    args.add_argument('-v', '--version', action='version',
                      version='%(prog)s 1.0', help="Show program's version number and exit.")

    args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS)
    required.add_argument("--commande", required=True)
    args.add_argument("--cle")
    args.add_argument("--texte")
    args.add_argument("--switchs", nargs=2, action='append')
    return args.parse_args()


main(menu())
