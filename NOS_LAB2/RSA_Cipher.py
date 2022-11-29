from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSA_Cipher():

    def init(self, key_size):
        self.key_size = key_size
        self.keyPair = RSA.generate(key_size)

    def encrypt(self, data):
        if(isinstance(data, str)):
            data_bytes = data.encode()
        else:
            data_bytes = data
        pubKey = self.keyPair.publickey()

        encryptor = PKCS1_OAEP.new(pubKey)
        encrypted = encryptor.encrypt(data_bytes)
        return encrypted

    def decrypt(self, encrypted):

        decryptor = PKCS1_OAEP.new(self.keyPair)
        decrypted = decryptor.decrypt(encrypted)

        return decrypted

    def get_keyPair(self):
        return self.keyPair


#message = "jako bitna poruka"
#rsa_cipher = RSA_Cipher()
#rsa_cipher.init(1024) # 1024, 2048, 3072

#rsa_encyrpted_message = rsa_cipher.encrypt(message)
#print("Kriptirana poruka: {}".format(rsa_encyrpted_message))
#rsa_decrypted_message = rsa_cipher.decrypt(rsa_encyrpted_message)
#print("Dekriptirana poruka: {}".format(rsa_decrypted_message))