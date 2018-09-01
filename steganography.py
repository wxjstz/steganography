#! env python
import sys
import getopt
from PIL import Image


def encode_bin(s):
    r = ''
    s = s.encode('hex')
    for c in s:
        r = r + {
            '0': '0000',
            '1': '0001',
            '2': '0010',
            '3': '0011',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'a': '1010',
            'b': '1011',
            'c': '1100',
            'd': '1101',
            'e': '1110',
            'f': '1111'
        }[c]
    return r


def decode_bin(s):
    r = ''
    i = 0
    while i + 4 <= len(s):
        c = s[i: i + 4]
        r = r + {
            '0000': '0',
            '0001': '1',
            '0010': '2',
            '0011': '3',
            '0100': '4',
            '0101': '5',
            '0110': '6',
            '0111': '7',
            '1000': '8',
            '1001': '9',
            '1010': 'a',
            '1011': 'b',
            '1100': 'c',
            '1101': 'd',
            '1110': 'e',
            '1111': 'f'
        }[c]
        i = i + 4
    return r.decode('hex')


class steganography:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.width = self.image.size[0]
        self.length = self.image.size[1]
        self.pixels = self.image.load()
        self.color_num = len(self.pixels[0, 0])
        self.op_width = 0
        self.op_length = 0
        self.op_color_idx = 0

    def __del__(self):
        self.image.save(self.path)

    def __reset(self):
        self.op_width = 0
        self.op_length = 0
        self.op_color_idx = 0

    def __next_bit(self):
        self.op_color_idx += 1
        if self.op_color_idx == self.color_num:
            self.op_color_idx = 0
            self.op_width += 1
            if self.op_width == self.width:
                self.op_width = 0
                self.op_length += 1

    def __write_bit(self, bit):
        pixel = list(self.pixels[self.op_width, self.op_length])
        if bit == '1':
            pixel[self.op_color_idx] = pixel[self.op_color_idx] | 1
        else:
            pixel[self.op_color_idx] = pixel[self.op_color_idx] & (~ 1)
        self.pixels[self.op_width, self.op_length] = tuple(pixel)
        self.__next_bit()

    def __read_bit(self):
        pixel = list(self.pixels[self.op_width, self.op_length])
        r = str(pixel[self.op_color_idx] & 1)
        self.__next_bit()
        return r

    def __write_length(self, length):
        for i in xrange(32):
            self.__write_bit(str(length & 1))
            length = length >> 1

    def __read_length(self):
        r = 0
        for i in xrange(32):
            r = r + (int(self.__read_bit()) << i)
        return r

    def write(self, s):
        self.__reset()
        s = encode_bin('STEGANOGRAPHY:' + s)
        if 32 + len(s) > self.width * self.length * self.color_num:
            print 'too big to write in this picture'
            sys.exit(1)
        self.__write_length(len(s))
        for c in s:
            self.__write_bit(c)

    def read(self):
        self.__reset()
        length = self.__read_length()
        if 32 + length > self.width * self.length * self.color_num:
            return None
        head_length = len(encode_bin('STEGANOGRAPHY:'))
        if length < head_length:
            return None
        s = ''
        for i in xrange(head_length):
            s = s + self.__read_bit()
        if decode_bin(s) != 'STEGANOGRAPHY:':
            return None
        s = ''
        for i in xrange(length - head_length):
            s = s + self.__read_bit()
        return decode_bin(s)


def usage():
    print 'uasge:'
    print '    -h | --help    print this message'
    print '    -r | --read    read text from picture'
    print '    -w | --write   write text to picture'
    print '    -p <picture file>'
    print '       | --picture <picture file>'
    print '                   picture file to be operate'
    print '    -f <input file>'
    print '       | --file <input file>'
    print '                   write file to picture.'
    print '                   file come from stdin, when <input file> is \'--\''
    sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrwp:f:', ['help', 'read', 'write', 'picture=', 'file='])
    except getopt.GetoptError:
        usage()

    write_text = None
    picture_file = None
    operate_help = False
    operate_read = False
    operate_write = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            operate_help = True
        elif opt in('-r', '--read'):
            operate_read = True
        elif opt in('-w', '--write'):
            operate_write = True
        elif opt in('-p', '--picture'):
            picture_file = arg
        elif opt in('-f', '--file'):
            if arg == '--':
                write_text = sys.stdin.read()
            else:
                with open(arg, 'r') as fn: write_text = fn.read()
        else:
            print 'unknown option'
            usage()

    if operate_help:
        usage()

    if operate_read and operate_write:
        print '--read/--write can not be used together'
        sys.exit(1)

    if (operate_read or operate_write) and not picture_file:
        print '--read/--write must used with --picture'
        sys.exit(1)

    if operate_write and not write_text:
        print '--write must used with --file'
        sys.exit(1)

    if operate_read and picture_file:
        sys.stdout.write(steganography(picture_file).read())
        return

    if operate_write and picture_file and write_text:
        steganography(picture_file).write(write_text)
        return
    
    usage()

if __name__ == '__main__':
    main()
