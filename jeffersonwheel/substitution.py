#
# Monoalphabetic Substitution Cipher
# for UVA GenCyber 2018
#
# David Evans
# 20 June 2018
#

# We'll use standard Python random, even though it is not cryptographically secure! 
# If you were planning to use any of these ciphers to protect nuclear secrets (please
# don't!), you should replace this with a cryptographic random nubmer generator,
# like the one provided by PyCrypto. After version 3.6, Python will provide the
# secrets module, with a cryptographic random number generator.
import random 

# We use the uppercase English letters, ABC...Z, as our alphabet.
ALPHABET = [chr(ch + ord('A')) for ch in range(26)] 

def generate_key(alphabet = ALPHABET): 
    """
    Generates a key for a monoalphabetic substitution cipher, which is a
    random permutation of the letters in the alphabet.
    """
    unused = list(alphabet)
    key = [] 
    while unused:
        letter = random.choice(tuple(unused))
        unused.remove(letter)
        key.append(letter)

    return key

def monoalphabetic_encrypt(key, msg, alphabet=ALPHABET):
    """
    Returns the encryption of message msg using the key. Encrypting with
    a monoalphabetic substitution cipher is just replacing each letter
    in the message with its substitution.  Only alphabet letters are
    encrypted, leaving punctuation and numbers unchanged (obviously this
    is very damanging to security, but, of course, the monoalphabetic
    cipher provides very little security anyway.
    """
    return ''.join([key[alphabet.index(c)] if c.isalpha() else c
                    for c in msg])

def monoalphabetic_decrypt(key, msg, alphabet=ALPHABET):
    return ''.join([alphabet[key.index(c)] if c.isalpha() else c
                    for c in msg])

def monoalphabetic_demo(msg):
    key = generate_key()
    msg = msg.upper()
    ctx = monoalphabetic_encrypt(key, msg)
    assert monoalphabetic_decrypt(key, ctx) == msg
    print ("Key:        " + ''.join(key))
    print ("Message:    " + msg)
    print ("Ciphertext: " + ctx)

if __name__ == "__main__":    
    msg = "Three can keep a secret, if two of them are dead. - Benjamin Franklin"
    monoalphabetic_demo(msg)

    # for a harder encryption, strip out all the non-alpha
    msg = "In mathematics you don't understand things, you just get used to them. John Von Neumann"
    msg = ''.join(c for c in msg if c.isalpha())
    monoalphabetic_demo(msg)

    
