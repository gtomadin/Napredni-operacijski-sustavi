import Digital_Seal


def readFromFile(path):
    readfile = open(path, "r")
    return readfile


def writeInFile(path, data):
    writefile = open(path, "a", encoding="utf-8")
    writefile.write(data)

def toTuple(data):
    chucks = data.split('||,||')
    print(len(chucks))

if __name__ == "__main__":
    readfile = readFromFile("C:\\Code\\Pycharm\\NOS_lab2\\0036496597.txt")

    dig_seal = Digital_Seal.Digital_Seal()
    dig_seal.init("aes", 16, "cbc", 1024, "sha256")  # aes, des3 / 16, 24, 32(samo aes) / ebc, cbc, ofb / 1024 2048, 3072 / sha256, sha512

    envelope_and_sign = dig_seal.create_envelope_and_signed(readfile.read())
    print("Digitalni pečat: {}".format(envelope_and_sign))

    opened_envelope = dig_seal.verify_and_open_envelope(envelope_and_sign)

    print("Dekriptirana poruka: {}".format(opened_envelope))