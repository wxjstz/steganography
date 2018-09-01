# depend

Dependent on pillow/pycrypto. Install with follow command.

`pip install pillow pycrypto`

# usage
```
➜  ~ ./steganography.py -h
uasge:
    -h | --help    print this message
    -r | --read    read text from picture
    -w | --write   write text to picture
    -p <picture file>
       | --picture <picture file>
                   picture file to be operate
    -f <input file>
       | --file <input file>
                   write file to picture.
                   file come from stdin, when <input file> is '--'

➜  ~ ./cipher.py -h
usage:
    -h | --help      print this message
    -e | --encrypt   encrypt operate
    -d | --decrypt   decrypt operate
    -m <encrypt_method>
       | --method <encrypt_method>
                     Encrypt method: ARC4, ARC2-CBC, Blowfish-CBC, DES3-CBC, AES-CBC, CAST-CBC
                     default method is AES-CBC
    -f <file>
       |--file <file>
                     source to encrypt/decrypt
                     source come from stdin, when <file> is '--'
    -p <password>
       | --passwd <password>
                     key used to encrypt/decrypt
```

# example

1. plain text write to picture

`./steganography.py -w -p test.png -f plain.txt`

2. read plain text from picture

`./steganography.py -r -p test.png`

3. ciphertext write to picture

`./cipher.py -e -p password -f plain.txt | ./steganography.py -w -p test.png -f --`

4. read ciphertext from picture

`./steganography.py -r -p test.png | ./cipher.py -d -p password -f --`

