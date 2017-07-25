"""
For using this module, we should make sure that the necessary package as pycrypt has been installed.
Any question, please refer to : https://www.dlitz.net/software/pycrypto/
By ShaoMingwu on 2015/1/24
"""

import subprocess
import rsa
from base64 import b64encode, b64decode
# from Crypto.PublicKey import RSA
from public import constant

__author__ = 'Shaomingwu@inspur.com'


def launchcmd(cmdstr):
    """
    Launch a cmdstr, and get the result.
    6 June,2015 Edited by Shaomingwu@inspur.com : return the original output data.
    :param cmdstr: command string.
    :return: The result after launching the cmdstr.
    """
    # Check if the input cmdstr is valid?
    pp = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if pp:
        return pp.stdout


def unicorn_decrypt(message):
    """
    Decrypt the message.
    :param message:  The encrypted message.
    :return: The original message.
    Add one more step: b64decode. By ShaoMingwu@inspur.com
    """
    privatekey = rsa.PrivateKey.load_pkcs1(constant.PRIVATE_KEY_UNICORN)
    try:
        return rsa.decrypt(b64decode(message), privatekey)
    except Exception:
        return ''


if __name__ == "__main__":
    # Test the functions.
    print(launchcmd("ls -l"))

    print("Len of publick key is [%d]" % len(constant.PUBLIC_KEY_UNICORN))
    print("Len of private key is [%d]" % len(constant.PRIVATE_KEY_UNICORN))

    publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(constant.PUBLIC_KEY_UNICORN)
    privateKey = rsa.PrivateKey.load_pkcs1(constant.PRIVATE_KEY_UNICORN)

    msgOri = "I want to play football with you."
    enTuple = rsa.encrypt(msgOri, publicKey)

    enBase64 = b64encode(enTuple)
    print("%s\n%d" % (enTuple, len(enTuple)))
    print("%s\n%d" % (enBase64, len(enBase64)))
    msgGet = unicorn_decrypt(enBase64)
    print(msgGet)
