from Crypto.Hash import SHA256, SHA512

class SHA2_Hasher():

    def init(self, hash_variant):

        if(hash_variant == "sha256"):
            self.hasher = SHA256.new()

        if(hash_variant == "sha512"):
            self.hasher = SHA512.new()

    def hash(self, data):

        if(isinstance(data, str)):
            data = data.encode()

        self.hasher.update(data)

    def get_hexdigest(self):
        return self.hasher.hexdigest()

#message = "jako bitna poruka"
#sha2 = SHA2_Hasher()
#sha2.init("sha256") #sha256, sha512
#print("Hashirana poruka: {}".format(sha2.get_hexdigest()))