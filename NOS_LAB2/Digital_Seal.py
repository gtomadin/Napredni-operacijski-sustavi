import Digital_Envelope, Digital_Signature

class Digital_Seal():

    def init(self, symmetric_alg, symmetric_key_size, symmetric_cipher_mode, asymmetric_key_size, hash_variant):

        self.digital_envelope = Digital_Envelope.Digital_Envelope()
        self.digital_envelope.init(symmetric_alg, symmetric_key_size, symmetric_cipher_mode, asymmetric_key_size)


        self.digital_signature = Digital_Signature.Digital_Signature()
        self.digital_signature.init(asymmetric_key_size, hash_variant)

    def create_envelope_and_signed(self, data):
        envelope = self.digital_envelope.envelope(data)
        #print("envelope: {}".format(envelope))
        signature = self.digital_signature.sign(envelope[0]), self.digital_signature.sign(envelope[1])
        #print("signature: {}".format(signature))
        return envelope, signature

    def verify_and_open_envelope(self, envelope_and_sign):
        envelope, signature = envelope_and_sign
        #print(envelope_and_sign)
        #print("envelope: {}".format(envelope))
        #print("signature: {}".format(signature))

        ver1 = self.digital_signature.verify(signature[0], envelope[0])
        ver2 = self.digital_signature.verify(signature[1], envelope[1])

        if(ver1 == "The signature is valid." and ver2 == "The signature is valid."):

            return self.digital_envelope.open_envelope(envelope)


#message = "jako bitna poruka"
#dig_seal = Digital_Seal()
#dig_seal.init("aes", 16, "cbc", 1024, "sha256") # aes, des3 / 16, 24, 32(samo aes) / ebc, cbc, ofb / 1024 2048, 3072 / sha256, sha512

#envelope_and_sign = dig_seal.create_envelope_and_signed(message)
#print("Digitalni pečat: {}".format(envelope_and_sign))
#opened_envelope = dig_seal.verify_and_open_envelope(envelope_and_sign)
#print("Dekriptirana poruka: {}".format(opened_envelope))