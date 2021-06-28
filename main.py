import random,helper,makeFile


def generate_key_pair(p, q):
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


def encrypt(pk, plaintext):
    key, n = pk
    # Convertis chaque lettre du texte en clair en nombres basés sur le caractère utilisant B^e mod n
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Retour d'un tableau de bytes
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    # Génére le texte en clair basé sur le texte chiffré et la clé privée en utilisant C^d mod n
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Retour d'un tableau de bytes sous une chaine
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("===========================================================================================================")
    print("================================== RSA Encryptor / Decrypter ==============================================")
    print(" ")

    p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
    q = int(input(" - Enter another prime number (Not one you entered above): "))

    print(" - Generating your public / private key-pairs now . . .")

    public, private = generate_key_pair(p, q)

    print(" - Your public key is ", public, " and your private key is ", private)
    makeFile.create_file_rsa("mescles",private[0],public[0])
    message = input(" - Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)

    print(" - Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    print(" - Decrypting message with private key ", private, " . . .")
    print(" - Your message is: ", decrypt(private, encrypted_msg))

    print(" ")
    print("============================================ END ==========================================================")
    print("===========================================================================================================")