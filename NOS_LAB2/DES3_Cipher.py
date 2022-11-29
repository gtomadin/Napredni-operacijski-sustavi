from Crypto.Cipher import DES3
import base64
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class DES3_Cipher():

    def init(self, key_size, cipher_mode):
        self.key = DES3.adjust_key_parity(get_random_bytes(key_size))
        self.cipher_mode = cipher_mode

    def encrypt(self, data):
        data_bytes = data.encode()
        padded = pad(data_bytes, DES3.block_size)
        iv = Random.new().read(DES3.block_size)
        cipher = self.get_cipher(iv)
        encrypted_data = cipher.encrypt(padded)
        return base64.b64encode(iv + encrypted_data)

    def decrypt(self, encoded_data):
        iv_data = base64.b64decode(encoded_data)
        iv = iv_data[:DES3.block_size]
        encrypted_data = iv_data[DES3.block_size:]
        cipher = self.get_cipher(iv)
        data = cipher.decrypt(encrypted_data)
        return unpad(data, DES3.block_size).decode('utf-8')


    def get_cipher(self, iv):
        if(self.cipher_mode == "ecb"):
            return DES3.new(self.key, DES3.MODE_ECB)

        if (self.cipher_mode == "cbc"):
            return DES3.new(self.key, DES3.MODE_CBC, iv)

        if (self.cipher_mode == "ofb"):
            return DES3.new(self.key, DES3.MODE_OFB, iv)

    def get_key(self):
        return self.key


#message = "jako bitna poruka"
#des3_cipher = DES3_Cipher()
#des3_cipher.init(24, "cbc") # 16, 24 / ecb, cbc, ofb

#des3_encyrpted_message = des3_cipher.encrypt(message)
#print("Kriptirana poruka: {}".format(des3_encyrpted_message))
#des3_decrypted_message = des3_cipher.decrypt(des3_encyrpted_message)
#print("Dekriptirana poruka: {}".format(des3_decrypted_message))