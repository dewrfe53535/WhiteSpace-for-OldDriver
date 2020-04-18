# Author: SuperFashi
import binascii
import getopt
import sys
import os

Formore = 0

def writeFile(message, path):
    file = open(path, 'w',encoding='utf-8')
    file.write(message)
    file.close()

def readFile(path,isdecrypt = False):
    if isdecrypt:
        file = open(path,'r',encoding='utf-8').read()
    else:
        file = open(path,'rb').read()
    return file

def readWS(white):
    ret = ''
    for char in white:
        if char == ' ':
            ret += '0'
        elif char == '	':
            ret += '1'
    return ret

def readWSAdvance(white):
    deco = white.split('+')[1:-1]
    ret = ''
    for char in deco:
        if char == '':
            ret += '0'
        elif char == ' ':
            ret += '1'
    return ret

def writeWS(bin):
    ret = ''
    for char in bin:
        if char == '0':
            ret += ' '
        elif char == '1':
            ret += '	'
    return ret

def writeWSAdvance(bin):
    ret = '+'
    for char in bin:
        if char == '1':
            ret += ' '
        ret += '+'
    return ret

def toBin(text):
    bits = bin(int(binascii.hexlify(text), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def toStr(bin):
    hex_string = '%x' % int(bin, 2)
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1))).decode('utf-8')

def usage():
    # print('Watch the code yourself please!')
    print('Usage:') 
    print('python whitespace.py -e|-d (-i input -o output)')
    print('-h, --help: View this manual')
    print('-e, --encrypt: Run encrypt mode')
    print('-d, --decrypt: Run decrypt mode')
    print('-a, --advanced: use \'+\' as a spliter in order to prevent some idiot escape methods, also needs to decrypt with this mode')
    print('-i, --input=: Read a file instead of typing it')
    print('-o, --output=: Write to a file instead of printing it')
    print('')
    print('Notice that when you running decrypt mode, everything besides spaces and tabs will be ignored, but at least contain one space or tab or the program will throw an error.')
    exit()

if __name__ == '__main__':
    encrypt = 0
    decrypt = 0
    inputPath = 0
    outputPath = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'haedi:o:', ['help', 'advanced', 'encrypt', 'decrypt', 'input=', 'output='])
    except:
        usage()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-e', '--encrypt'):
            encrypt = True
        elif opt in ('-d', '--decrypt'):
            decrypt = True
        elif opt in ('-i', '--input'):
            if os.path.exists(arg):
                inputPath = arg
            else:
                print('You have entered a wrong input path!')
                usage()
        elif opt in ('-o', '--output'):
            outputPath = arg
        elif opt in ('-a', '--advanced'):
            Formore = True
    if encrypt and decrypt:
        usage()
    if encrypt:
        if not inputPath:
            print('Please enter some secret code:')
            text = input()
            text = text.encode('utf-8')
        else:
            text = readFile(inputPath)
        try:
            if Formore:
                encryptedText = writeWSAdvance(toBin(text))
            else:
                encryptedText = writeWS(toBin(text))
        except Exception as e:
            print(e)
            print('Encrypt success...fully failed due to some reasons.')
            print('Try to check your input!')
            usage()
        print('Encrypt finished!')
        if not outputPath:
            if Formore:
                print('Please completely copy all the text down below:')
            else:
                print('Please completely copy all the *invisible* things down below:')
            print(encryptedText)
        else:
            writeFile(encryptedText, outputPath)
            print('Please check your file to get some *invisible* things')
    elif decrypt:
        if not inputPath:
            if Formore:
                print('Please enter some text here:')
            else:
                print('Please enter some *blanks* here:')
            white = input()
        else:
            white = readFile(inputPath,True)
        try:
            if Formore:
                text = toStr(readWSAdvance(white))
            else:
                text = toStr(readWS(white))
        except Exception as e:
            print(e)
            print('Decrypt success...fully failed due to some reasons.')
            print('Try to check your input!')
            usage()
        if not outputPath:
            print('Here\'re some messages:')
            print(text)
        else:
            writeFile(text, outputPath)
            print('You can now see the original texts.')
    else:
        usage()
            