import random, binascii

test_string = random.randbytes(2048)

def parse(raw_data: bytes):
    ascii_data = binascii.b2a_hex(raw_data).decode()
    numbers = [int(byte, 16) for byte in ascii_data]
    print(numbers)
    final_data = []
    converted_byte = 1 << 9
    for index, data in enumerate(ascii_data):
        if index % 2 == 0:
            converted_byte = 0

if __name__ == "__main__":
    parse(test_string)