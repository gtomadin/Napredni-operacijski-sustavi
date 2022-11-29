from Crypto.Cipher import AES
import base64
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad



class AES_Cipher():

    def init(self, key_size, cipher_mode):
        self.key = get_random_bytes(key_size)
        self.cipher_mode = cipher_mode

    def encrypt(self, data):
        data_bytes = data.encode()
        padded = pad(data_bytes, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = self.get_cipher(iv)
        encrypted_data = cipher.encrypt(padded)
        return base64.b64encode(iv + encrypted_data)

    def decrypt(self, encoded_data):
        iv_data = base64.b64decode(encoded_data)
        iv = iv_data[:AES.block_size]
        encrypted_data = iv_data[AES.block_size:]
        cipher = self.get_cipher(iv)
        data = cipher.decrypt(encrypted_data)
        return unpad(data, AES.block_size).decode('utf-8')

    def get_cipher(self, iv):
        if(self.cipher_mode == "ecb"):
            return AES.new(self.key, AES.MODE_ECB)

        if (self.cipher_mode == "cbc"):
            return AES.new(self.key, AES.MODE_CBC, iv)

        if (self.cipher_mode == "ofb"):
            return AES.new(self.key, AES.MODE_OFB, iv)

    def get_key(self):
        return self.key



#message = "jako bitna poruka"
#aes_cipher = AES_Cipher()
#es_cipher.init(32, "cbc") # 16, 24, 32 / ecb, cbc, ofb

#aes_encyrpted_message = aes_cipher.encrypt(message)
#print("Kriptirana poruka: {}".format(aes_encyrpted_message))
#aes_decrypted_message = aes_cipher.decrypt(aes_encyrpted_message)
#print("Dekriptirana poruka: {}".format(aes_decrypted_message))
