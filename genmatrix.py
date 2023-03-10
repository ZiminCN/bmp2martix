#!/usr/bin/python3

import sys
import getopt
from PIL import Image,ImageDraw,ImageFont

def mono_genmatrix(image, flip, scan_dir, endian, color_reverse, increase):
    width = image.size[0]
    height = image.size[1]

    if flip == 'X':
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    elif flip == 'Y':
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    if scan_dir == 'H':
        scan_direction = 'Horizontal'
    else:
        scan_direction = 'Vertical'

    if endian == 'B':
        byte_reverse = True
    else:
        byte_reverse = False

    if color_reverse == 'true':
        color_reverse = True
    else:
        color_reverse = False

    unalign = 0
    matrix = list()
    
    if scan_direction == 'Horizontal':
        if (width%8) != 0:
            unalign = 1
        if increase == 'X':
            for i in range(0, height):
                for j in range(0, (width//8)+unalign):
                    v = 0x00
                    rs = 8*j
                    re = 8*(j+1)
                    if re > width:
                        re = width
                    for k in range(rs, re):
                        if image.getpixel((k, i)) != 0:
                            if not byte_reverse:
                                v |= (0x01 << (k%8))
                            else:
                                v |= (0x01 << (7-(k%8)))
                    if color_reverse:
                        v ^= 0xff
                    matrix.append(v)
        if increase == 'Y':
            for i in range(0, (width//8)+unalign):
                for j in range(0, height):
                    v = 0x00
                    rs = 8*i
                    re = 8*(i+1)
                    if re > width:
                        re = width
                    for k in range(rs, re):
                        if image.getpixel((k, j)) != 0:
                            if not byte_reverse:
                                v |= (0x01 << (k%8))
                            else:
                                v |= (0x01 << (7-(k%8)))
                    if color_reverse:
                        v ^= 0xff
                    matrix.append(v)
    elif scan_direction == 'Vertical':
        if (height%8) != 0:
            unalign = 1
        if increase == 'X':
            for i in range(0, (height//8)+unalign):
                for j in range(0, width):
                    v = 0x00
                    rs = 8*i
                    re = 8*(i+1)
                    if re > height:
                        re = height
                    for k in range(rs, re):
                        if image.getpixel((j, k)) != 0:
                            if not byte_reverse:
                                v |= (0x01 << k%8)
                            else:
                                v |= (0x01 << (7-k%8))
                    if color_reverse:
                        v ^= 0xff
                    matrix.append(v)
        if increase == 'Y':
            for i in range(0, width):
                for j in range(0, (height//8)+unalign):
                    v = 0x00
                    rs = 8*j
                    re = 8*(j+1)
                    if re > height:
                        re = height
                    for k in range(rs, re):
                        if image.getpixel((i, k)) != 0:
                            if not byte_reverse:
                                v |= (0x01 << k%8)
                            else:
                                v |= (0x01 << (7-k%8))
                    if color_reverse:
                        v ^= 0xff
                    matrix.append(v)
    return matrix

def show_matrix(matrix):
    i = 0
    cnt_arr = 0
    for v in matrix:
        if i == 0:
            print("{", end='')
        print('0x%02x' % v, end='')
        if i != 7:
            print(',', end='')
        i += 1
        if i == 8:
            print("},", end='') 
            i = 0
            cnt_arr += 1
            print()
    print()
    print()
    print()
    print("cnt_arr is ", end='')
    print(cnt_arr)

def main():
    help = 'Usage: %s [option]' % sys.argv[0]
    help += '''\nOption:
    -h | --help                 ??????????????????

    -O | --operation            ??????????????????????????????str
                                str: ????????????, mono: ??????????????????

    -F | --flip                 ????????????
                                X: ????????????, Y: ????????????

    -S | --scan-dir             ????????????????????????????????????
                                H:????????????, V:????????????

    -I | --increase             ??????????????????????????????X
                                X:????????????, Y:????????????

    -E | --endian               ???????????????????????????????????????
                                L: ???????????????????????????????????????????????? pixel 0 -> bit0
                                B: ???????????????????????????????????????????????? pixel 0 -> bit7

    -H | --character-height     ????????????????????????16???str???????????????

    -R                          ??????????????????????????????
                                ???????????????: 1, ??????: 0
                                ??????: ??????: 0, ??????: 1

Example:

    (1) ????????????????????????????????? (????????????, ?????????, ????????????)
    ./genmatrix -O mono -R xxx.bmp

    (2) ???????????????????????????????????? (16x16, ????????????, ?????????, ????????????)
    ./genmatrix -O str -S V -E B '?????????????????????'
'''
    short_opts = 'hO:F:S:E:H:R:I:'
    opts = ['help', 'operation', 'flip' 'scan-dir', 'endian', 'character-height', 'increase']

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
    except getopt.GetoptError as err:
        print(err)
        print(help)
        sys.exit(1)

    operation       = 'str'
    flip            = 'false'
    scan_dir        = 'H'
    endian          = 'L'
    char_height     = '16'
    color_reverse   = 'false'
    increase        = 'X'

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help)
            sys.exit()
        elif opt in ('-O', '--operation'):
            if arg not in ('str', 'mono'):
                print('??????????????????: ' + opt + ' ' + arg)
                sys.exit(1)
            operation = arg
        elif opt in ('-F', '--flip'):
            if arg not in ('X', 'Y'):
                print('??????????????????: ' + opt + ' ' + arg)
                sys.exit(1)
            flip = arg
        elif opt in ('-S', '--scan-dir'):
            if arg not in ('H', 'V'):
                print('??????????????????: ' + opt + ' ' + arg)
                sys.exit(1)
            scan_dir = arg
        elif opt in ('-I', '--increase'):
            if arg not in ('X', 'Y'):
                print('??????????????????: ' + opt + ' ' + arg)
                sys.exit(1)
            increase = arg
        elif opt in ('-E', '--endian'):
            if arg not in ('L', 'B'):
                print('??????????????????: ' + opt + ' ' + arg)
                sys.exit(1)
            endian = arg
        elif opt in ('-H', '--character-height'):
            char_height = arg
        elif opt in ('-R'):
            color_reverse = 'true'
        else:
            print(help)
            sys.exit(1)

    if len(args) > 0:
        arg = args[0]
    else:
        print('??????????????????????????????')
        print(help)
        sys.exit(1)

    print('\n????????????: ' + operation)
    if operation == 'str':
        print('????????????: ' + char_height)
    print('????????????: ' + flip)
    print('????????????: ' + scan_dir)
    print('????????????: ' + endian)
    print('????????????: ' + color_reverse + '\n')

    if operation == 'mono':
        img = Image.open(arg)
        if img.mode != '1':
            img = img.convert('L')
            img = img.convert('1')
        matrix = mono_genmatrix(img, flip, scan_dir, endian, color_reverse, increase)
        show_matrix(matrix)
        img.close()
    else:
        # ??????unicode???????????????
        l = list()
        for c in arg:
            l.append(ord(c))
        l.sort()
        # ???????????????
        c = list()
        for i in l:
            print(hex(i) + ', /* ' + chr(i) + ' */')
            c.append(chr(i))
        print(c)
        arg = c
        for s in arg:
            print('/* ' + hex(ord(s)) + ' */')
            if ord(s) < 128:
                w = int(char_height)//2
            else:
                w = int(char_height)
            h = int(char_height)
            img = Image.new("1", (w,h), (1))
            ttfont = ImageFont.truetype("fonts/unifont-13.0.06.ttf", h)
            draw = ImageDraw.Draw(img)
            draw.text((0,0), u'%c' % s, (0), font=ttfont)
            matrix = mono_genmatrix(img, flip, scan_dir, endian, color_reverse, increase)
            show_matrix(matrix)
            img.show()
            img.close()

if __name__ == '__main__':
    main()

