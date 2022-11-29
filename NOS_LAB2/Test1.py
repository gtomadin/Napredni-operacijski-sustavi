import AES_Cipher, DES3_Cipher, RSA_Cipher, SHA2_Hasher, Digital_Envelope, Digital_Signature, Digital_Seal

message = "jako bitna poruka"

# AES Test
print("AES")
aes_cipher = AES_Cipher.AES_Cipher()
aes_cipher.init(32, "cbc") # 16, 24, 32 / ecb, cbc, ofb

aes_encyrpted_message = aes_cipher.encrypt(message)
print("Kriptirana poruka: {}".format(aes_encyrpted_message))
aes_decrypted_message = aes_cipher.decrypt(aes_encyrpted_message)
print("Dekriptirana poruka: {}".format(aes_decrypted_message))
print()


# DES3 Test
print("DES3")
des3_cipher = DES3_Cipher.DES3_Cipher()
des3_cipher.init(24, "cbc") # 16, 24 / ecb, cbc, ofb

des3_encyrpted_message = des3_cipher.encrypt(message)
print("Kriptirana poruka: {}".format(des3_encyrpted_message))
des3_decrypted_message = des3_cipher.decrypt(des3_encyrpted_message)
print("Dekriptirana poruka: {}".format(des3_decrypted_message))
print()


# RSA Test
print("RSA")
rsa_cipher = RSA_Cipher.RSA_Cipher()
rsa_cipher.init(1024) # 1024, 2048, 3072

rsa_encyrpted_message = rsa_cipher.encrypt(message)
print("Kriptirana poruka: {}".format(rsa_encyrpted_message))
rsa_decrypted_message = rsa_cipher.decrypt(rsa_encyrpted_message)
print("Dekriptirana poruka: {}".format(rsa_decrypted_message))
print()


# SHA2 Test
print("SHA2")
sha2 = SHA2_Hasher.SHA2_Hasher()
sha2.init("sha256") #sha256, sha512
print("Hashirana poruka: {}".format(sha2.get_hexdigest()))
print()


# Digital_Envelope Test
print("Digitalna omotnica")
dig_env = Digital_Envelope.Digital_Envelope()
dig_env.init("aes", 16, "cbc", 1024) # aes, des3 / 16, 24, 32(samo aes) / ebc, cbc, ofb / 1024 2048, 3072

envelope = dig_env.envelope(message)
print("Digitalna omotnica: {}".format(envelope))
opened_envelope = dig_env.open_envelope(envelope)
print("Dekriptirana poruka: {}".format(opened_envelope))
print()


# Digital_Signature Test
print("Digitalni potpis")
dig_sig = Digital_Signature.Digital_Signature()
dig_sig.init(1024, "sha256") # 1024, 2048, 3072 / sha256, sha512

signature = dig_sig.sign(message)
print("Digitalni potpis: {}".format(signature))
check_signature = dig_sig.verify(signature, message)
print("Jeli potpis valjan: {}".format(check_signature))
print()


# Digital_Seal Test
print("Digitalni pečat")
dig_seal = Digital_Seal.Digital_Seal()
dig_seal.init("aes", 16, "cbc", 1024, "sha256") # aes, des3 / 16, 24, 32(samo aes) / ebc, cbc, ofb / 1024 2048, 3072 / sha256, sha512

envelope_and_sign = dig_seal.create_envelope_and_signed(message)
print("Digitalni pečat: {}".format(envelope_and_sign))
opened_envelope = dig_seal.verify_and_open_envelope(envelope_and_sign)
print("Dekriptirana poruka: {}".format(opened_envelope))