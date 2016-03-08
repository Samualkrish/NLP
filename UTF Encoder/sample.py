import sys
import struct
import os.path

def convertToBinary(hex_val):
    total_binary = ''
    for hex_char in list(hex_val):
        bin_val = "{0:b}".format((int(hex_char,16)))
        while len(bin_val) < 4:
            bin_val = '0' + bin_val
        total_binary = total_binary + bin_val
    return total_binary

def main():
    try:
        file = open(sys.argv[1], 'rb')

        output_file_name = (os.path.splitext(os.path.basename(file.name))[0]).split('_')[0] + "_out.txt"

        data = file.read(2)
        while data:
            value = struct.unpack(">H", data)[0]
            binary = ''
            if value < 128:
                binary = bin(int(hex(value), 16))[2:].zfill(8)
                byte_value = ''
                for i, bit in enumerate(reversed(list(binary))):
                    if i == 7:
                        byte_value = '0' + byte_value
                        break
                    byte_value = bit + byte_value
                out = open(output_file_name, 'w+')
                out.write(chr(int(byte_value,2)))
            elif value >= 128 and value < 2048:
                binary = bin(int(hex(value), 16))[2:].zfill(16)
                byte_value = ''
                for i, bit in enumerate(reversed(list(binary))):
                    if i == 5:
                        byte_value = '10' + bit + byte_value
                        continue
                    elif i == 10:
                        byte_value = '110' + bit + byte_value
                        break
                    byte_value = bit + byte_value
                p = struct.pack('>P', byte_value)
                out = open(output_file_name, 'wb+')
                print(p)
            elif value >= 2048 and value < 65535:
                binary = bin(int(hex(value), 16))[2:].zfill(24)
                byte_value = ''
                for i, bit in enumerate(reversed(list(binary))):
                    if i == 5:
                        byte_value = '10' + bit + byte_value
                        continue
                    elif i == 11:
                        byte_value = '10' + bit + byte_value
                        continue
                    elif i == 15:
                        byte_value = '1110' + bit + byte_value
                        break
                    byte_value = bit + byte_value
                p = struct.pack('>p', byte_value)
                print(p)
                out = open(output_file_name, 'wb+')
                #out.write(p)
            elif value >= 65535 and value < 1112064:
                print('4 byte')


            # Determine the hex value from the length
            # hex_len = len(hex(value)[2:])
            # binary = "{0:b}".format(value)
            # binary = '0' + binary
            # val = ''
            # for i, value in enumerate(reversed(list(binary))):
            #     if hex_len <= 2:
            #         if i == 7:
            #             val = '0' + val
            #             break
            #     elif hex_len == 3:
            #         if i == 6:
            #             val = '10' + val
            #         elif i == 11:
            #             val = '110' + val
            #             break
            #     elif hex_len == 4:
            #         if i == 6:
            #             val = '10' + val
            #         elif i == 11:
            #             val = '10' + val
            #             break
            #         elif i == 15:
            #             val = '110' + val
            #     val = value + val
            #
            # if hex_len <= 2:
            #     while len(val) < 8:
            #         val = '0' + val
            #
            # print(val)
            # character = chr(BitArray(bin=val).int)
            # out.write(character)
            # print(val)
            # print(hex(int(val, 2)))
            # print(int(bits, 2))
            # print(int(bits[::-1], 2).to_bytes(8, 'big'))
            # out.write(int(bits[::-1], 2).to_bytes(8, 'big'))
            # char_int_val = int(hex(int(val, 2)), 0)
            # character = chr(BitArray(bin=val).int)
            # print(character)
            # unicode_val = u'' + hex_data
            # print(unicode_val)
            # print(ord(unicode_val))
            # out.write(chr(ord(unicode_val)))
            # out.write(bytearray(int(i, 16) for i in hex_data))
            #out.write(val)
            # print(chr(int('0x' + hex(int(val, 2))[3:], 16)) + "\n")
            # out.write(chr(int(val, 2)))
            # if hex_len <= 2:
            #     val = ''
            #     for i, value in enumerate(reversed(list(binary))):
            #         if i == 7:
            #             val = '0' + val
            #             break
            #         val = value + val
            #
            #     # Just making sure that the binary are 1 byte long
            #     while len(val) < 8:
            #         val = '0' + val
            #     out.write(chr(BitArray(bin=val).int))
            # elif hex_len == 3:
            #     val = ''
            #     for i, value in enumerate(reversed(list(binary))):
            #         if i == 6:
            #             val = '10' + val
            #         if i == 11:
            #             val = '110' + val
            #             break
            #         val = value + val
            #     print(int(val, 2))
            #     # out.write(chr(int(val,2)))
            # elif hex_len == 4:
            #     val = ''
            #     for i, value in enumerate(reversed(list(binary))):
            #         if i == 6:
            #             val = '10' + val
            #         if i == 11:
            #             val = '10' + val
            #         if i == 15:
            #             val = '1110' + val
            #             break
            #         val = value + val
            #     int_val = int(val, 2)
            #     print(int_val)
            #     print(chr(int_val))

            data = file.read(2)
        file.close()
        out.close()
    except IOError as e:
        print("I/O Error")


if __name__ == '__main__':
    main()