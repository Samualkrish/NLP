import sys
import struct
from bitstring import BitArray


def main():
    try:
        file = open(sys.argv[1], 'rb')
        output_file_name = "utf8encoder_out.txt"
        out = open(output_file_name, 'wb')
        data = file.read(2)
        while data:
            value = struct.unpack(">H", data)[0]
            hex_val = hex(value)
            print(hex_val)
            byte_value = ''
            if hex_val < hex(127):
                binary = bin(int(hex_val, 16))[2:].zfill(8)
                for i, bit in enumerate(reversed(list(binary))):
                    if i == 7:
                        byte_value = '0' + byte_value
                        break
                    byte_value = bit + byte_value
            elif hex_val >= hex(128) and hex_val < hex(2047):
                binary = bin(int(hex_val, 16))[2:].zfill(16)
                for i, bit in enumerate(reversed(list(binary))):
                    if i == 5:
                        byte_value = '10' + bit + byte_value
                        continue
                    elif i == 10:
                        byte_value = '110' + bit + byte_value
                        break
                    byte_value = bit + byte_value
            elif hex_val >= hex(2048) and hex_val < hex(65535):
                binary = bin(int(hex_val, 16))[2:].zfill(24)
                print(binary)
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
            s = BitArray(bin=byte_value).bytes
            out.write(s)
            data = file.read(2)
        file.close()
        out.close()
    except IOError as e:
        print("I/O Error")


if __name__ == '__main__':
    main()
