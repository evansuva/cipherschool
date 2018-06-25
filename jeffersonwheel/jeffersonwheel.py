#
# Jefferson Wheel Cipher
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

from substitution import generate_key

def generate_wheels(num):
    """
    Returns an array of wheels for a Jefferson Cipher Wheel. Each wheel
    is just a random permutation of the alphabet.
    """
    wheels = []
    for i in range(num):
        wheels.append(generate_key())
    return wheels
    
def wheel_encrypt(wheels, msg, offset=None):
    """
    Returns the encryption of one block of a message using the input wheels.
    The optional parameter offest gives the row to select; if not provided,
    a random row is used.
    """

    if offset is None:
        offset = random.choice(range(1, len(wheels[0])))
        print ("Offset: " + str(offset))

    assert len(msg) <= len(wheels) # can only encrypt one block with this
    ciphertext = []
    for mindex in range(len(msg)):
        wheel = wheels[mindex]
        ciphertext.append(wheel[(wheel.index(msg[mindex]) + offset) % len(wheel)])
    return ''.join(ciphertext)

def wheel_decrypt(wheels, ciphertext):
    """
    Returns the possible decryptions of one block of a message using the input wheels.
    """

    assert len(ciphertext) <= len(wheels) # can only encrypt one block with this

    msgs = []
    for offset in range(1, len(wheels[0])):
        msgs.append(wheel_encrypt(wheels, ciphertext, -offset))
    return msgs

if __name__ == "__main__":    
    wheels = generate_wheels(20)
    # this prints vertically
    for wheel in wheels:
        print (','.join([c for c in wheel]))

    msg = "TOOMANYSECRETS"
    assert wheel_encrypt(wheels, msg, offset=0) == msg
    # encrypting with the inverse offset decrypts
    assert wheel_encrypt(wheels, wheel_encrypt(wheels, msg, offset=3), offset = -3) == msg

    ciphertext = wheel_encrypt(wheels, msg)
    msgs = wheel_decrypt(wheels, ciphertext)
    print ('\n'.join(msgs))
