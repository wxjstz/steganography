#! env python
import sys
import getopt
from Crypto.Hash import MD5, SHA256, SHA512
from Crypto.Cipher import ARC2, ARC4, DES3, CAST, AES, Blowfish

cryptors = {}
encrypt_methods = ''


def cryptor_register(cryptor):
    global cryptors
    global encrypt_methods
    cryptors[cryptor.name] = cryptor
    encrypt_methods += (', ' if encrypt_methods else '') + cryptor.name


class cipher_aes:
    name = 'AES-CBC'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        h = SHA256.new()
        h.update(self.key)
        self.key = h.digest()

    def __extend_plain(self, plain):
        i = 16 - len(plain) % 16 - 1
        return 'abcdefghijklmnop'[i] + plain + i * ' '

    def __extract_plain(self, plain):
        i = ord(plain[0]) - ord('a')
        if i == 0:
            return plain[1:]
        return plain[1: - i]

    def encrypt(self, plain):
        cryptor = AES.new(self.key, AES.MODE_CBC, 16 * ' ')
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = AES.new(self.key, AES.MODE_CBC, 16 * ' ')
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_aes)


class cipher_blowfish:
    name = 'Blowfish-CBC'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        h = SHA512.new()
        h.update(self.key)
        self.key = h.digest()[:56]

    def __extend_plain(self, plain):
        i = 8 - len(plain) % 8 - 1
        return '01234567'[i] + plain + i * ' '

    def __extract_plain(self, plain):
        i = ord(plain[0]) - ord('0')
        if i == 0:
            return plain[1:]
        return plain[1: - i]

    def encrypt(self, plain):
        cryptor = Blowfish.new(self.key, Blowfish.MODE_CBC, 8 * ' ')
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = Blowfish.new(self.key, Blowfish.MODE_CBC, 8 * ' ')
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_blowfish)


class cipher_cast:
    name = 'CAST-CBC'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        h = MD5.new()
        h.update(self.key)
        self.key = h.digest()

    def __extend_plain(self, plain):
        i = 8 - len(plain) % 8 - 1
        return '01234567'[i] + plain + i * ' '

    def __extract_plain(self, plain):
        i = ord(plain[0]) - ord('0')
        if i == 0:
            return plain[1:]
        return plain[1: - i]

    def encrypt(self, plain):
        cryptor = CAST.new(self.key, CAST.MODE_CBC, 8 * ' ')
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = CAST.new(self.key, CAST.MODE_CBC, 8 * ' ')
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_cast)


class cipher_des3:
    name = 'DES3-CBC'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        h = SHA256.new()
        h.update(self.key)
        self.key = h.digest()[:24]

    def __extend_plain(self, plain):
        i = 8 - len(plain) % 8 - 1
        return '01234567'[i] + plain + i * ' '

    def __extract_plain(self, plain):
        i = ord(plain[0]) - ord('0')
        if i == 0:
            return plain[1:]
        return plain[1: - i]

    def encrypt(self, plain):
        cryptor = DES3.new(self.key, DES3.MODE_CBC, 8 * ' ')
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = DES3.new(self.key, DES3.MODE_CBC, 8 * ' ')
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_des3)


class cipher_arc2:
    name = 'ARC2-CBC'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        h = MD5.new()
        h.update(self.key)
        self.key = h.digest()

    def __extend_plain(self, plain):
        i = 8 - len(plain) % 8 - 1
        return '01234567'[i] + plain + i * ' '

    def __extract_plain(self, plain):
        i = ord(plain[0]) - ord('0')
        if i == 0:
            return plain[1:]
        return plain[1: - i]

    def encrypt(self, plain):
        cryptor = ARC2.new(self.key, ARC2.MODE_CBC, 8 * ' ')
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = ARC2.new(self.key, ARC2.MODE_CBC, 8 * ' ')
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_arc2)


class cipher_arc4:
    name = 'ARC4'

    def __init__(self, key):
        self.key = key
        self.__extend_key()

    def __extend_key(self):
        key = ''
        h = SHA512.new()
        h.update(self.key)
        key += h.digest()
        h.update(self.key)
        key += h.digest()
        h.update(self.key)
        key += h.digest()
        h.update(self.key)
        key += h.digest()
        self.key = key

    def __extend_plain(self, plain):
        return plain

    def __extract_plain(self, plain):
        return plain

    def encrypt(self, plain):
        cryptor = ARC4.new(self.key)
        return cryptor.encrypt(self.__extend_plain(plain))

    def decrypt(self, cipher):
        cryptor = ARC4.new(self.key)
        return self.__extract_plain(cryptor.decrypt(cipher))


cryptor_register(cipher_arc4)


def usage():
    print 'usage:'
    print '    -h | --help      print this message'
    print '    -e | --encrypt   encrypt operate'
    print '    -d | --decrypt   decrypt operate'
    print '    -m <encrypt_method>'
    print '       | --method <encrypt_method>'
    print '                     Encrypt method: ' + encrypt_methods
    print '                     default method is AES-CBC'
    print '    -f <file>'
    print '       |--file <file>'
    print '                     source to encrypt/decrypt'
    print '                     source come from stdin, when <file> is \'--\''
    print '    -p <password>'
    print '       | --passwd <password>'
    print '                     key used to encrypt/decrypt'
    sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hedm:f:p:', ['help', 'encrypt', 'decrypt', 'method=', 'file=', 'passwd='])
    except getopt.GetoptError:
        usage()

    operate_help = False
    operate_encrypt = False
    operate_decrypt = False
    input_text = None
    password = None
    encrypt_method = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            operate_help = True
        elif opt in ('-e', '--encrypt'):
            operate_encrypt = True
        elif opt in ('-m', '--method'):
            encrypt_method = arg
        elif opt in ('-d', '--decrypt'):
            operate_decrypt = True
        elif opt in ('-f', '--file'):
            if arg == '--':
                input_text = sys.stdin.read()
            else:
                with open(arg, 'r') as fn: input_text = fn.read()
        elif opt in ('-p', '--passwd'):
            password = arg
        else:
            print 'unknow option'
            usage()

    if operate_help:
        usage()

    if operate_encrypt and operate_decrypt:
        print '--encrypt/--decrypt can not used together'
        sys.exit(1)

    if (operate_encrypt or operate_decrypt) and not input_text:
        print '--encrypt/--decrypt must used with --file'
        sys.exit(1)

    if (operate_encrypt or operate_decrypt) and not password:
        print '--encrypt/--decrypt must used with --passwd'
        sys.exit(1)

    if operate_decrypt and encrypt_method:
        print '--method should not be used with --decrypt,  it can be selected automatically'
        sys.exit(1)

    encrypt_method = encrypt_method if encrypt_method else 'AES-CBC'
    if encrypt_method not in cryptors:
        print 'encrypt method must be one of ' + encrypt_methods
        sys.exit(1)

    if operate_encrypt and input_text:
        cryptor = cryptors[encrypt_method](password)
        sys.stdout.write('CIPHER,' + encrypt_method + ':' + cryptor.encrypt(input_text).encode('hex'))
        return

    if operate_decrypt and input_text:
        if input_text[:7] != 'CIPHER,':
            print 'This is not encrypted by shield.py'
            sys.exit(1)
        input_text = input_text[7:]
        for key in cryptors:
            if input_text.startswith(key + ':'):
                cryptor = cryptors[key](password)
                input_text = input_text[len(key) + 1:]
                sys.stdout.write(cryptor.decrypt(input_text.decode('hex')))
                return
        print 'unknow encrypt method'
        sys.exit(1)

    usage()


if __name__ == '__main__':
    main()
