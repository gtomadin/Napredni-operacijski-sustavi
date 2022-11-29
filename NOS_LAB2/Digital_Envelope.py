import AES_Cipher, DES3_Cipher, RSA_Cipher

class Digital_Envelope():

    def init(self, symmetric_alg, symmetric_key_size, symmetric_cipher_mode, asymmetric_key_size):

        if(symmetric_alg == "aes"):
            self.symmetric_cihper = AES_Cipher.AES_Cipher()
        if (symmetric_alg == "des3"):
            self.symmetric_cihper = DES3_Cipher.DES3_Cipher()

        self.symmetric_cihper.init(symmetric_key_size, symmetric_cipher_mode)

        self.asymmetric_cihper = RSA_Cipher.RSA_Cipher()
        self.asymmetric_cihper.init(asymmetric_key_size)

    def envelope(self, data):
        encrypted_data = self.symmetric_cihper.encrypt(data)
        encrypted_sym_key = self.asymmetric_cihper.encrypt(self.symmetric_cihper.get_key())
        return encrypted_data, encrypted_sym_key

    def open_envelope(self, digital_envelope):
        encrypted_data, encrypted_sym_key = digital_envelope
        sym_key = self.asymmetric_cihper.decrypt(encrypted_sym_key)
        data = self.symmetric_cihper.decrypt(encrypted_data)
        return data


#message = "jako bitna poruka"
#dig_env = Digital_Envelope()
#dig_env.init("aes", 16, "cbc", 1024) # aes, des3 / 16, 24, 32(samo aes) / ebc, cbc, ofb / 1024 2048, 3072

#envelope = dig_env.envelope(message)
#print("Digitalna omotnica: {}".format(envelope))
#opened_envelope = dig_env.open_envelope(envelope)
#print("Dekriptirana poruka: {}".format(opened_envelope))
