import AES_Cipher, DES3_Cipher, RSA_Cipher, SHA2_Hasher
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad

class Digital_Signature():

    def init(self, asymmetric_key_size, hash_variant):

        self.asymmetric_cihper = RSA_Cipher.RSA_Cipher()
        self.asymmetric_cihper.init(asymmetric_key_size)

        self.sha2_hasher_signer = SHA2_Hasher.SHA2_Hasher()
        self.sha2_hasher_signer.init(hash_variant)

        self.sha2_hasher_verifier = SHA2_Hasher.SHA2_Hasher()
        self.sha2_hasher_verifier.init(hash_variant)

    def sign(self, data):
        self.sha2_hasher_signer.hash(data)
        key = self.asymmetric_cihper.get_keyPair()
        h = self.sha2_hasher_signer.hasher
        signature = pkcs1_15.new(key).sign(h)
        padded = pad(signature, 128)
        return padded

    def verify(self, signature, data):
        signature = unpad(signature, 128)
        key = self.asymmetric_cihper.get_keyPair().public_key()
        if (isinstance(data, str)):
            data = data.encode()

        self.sha2_hasher_verifier.hash(data)
        h = self.sha2_hasher_verifier.hasher

        try:
            pkcs1_15.new(key).verify(h, signature)
            return "The signature is valid."
        except (ValueError, TypeError):
            return "The signature is not valid."


#message = "jako bitna poruka"
#dig_sig = Digital_Signature()
#dig_sig.init(1024, "sha256") # 1024, 2048, 3072 / sha256, sha512

#signature = dig_sig.sign(message)
#print("Digitalni potpis: {}".format(signature))
#check_signature = dig_sig.verify(signature, message)
#print("Jeli potpis valjan: {}".format(check_signature))