import cv2
import numpy as np


def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode_image(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)

    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    print('Completed!')
    return image


def decode_image(image_name):
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    # split by 8-bits
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    print('Completed!')
    return decoded_data[:-5]


def encoded_start():
    file_imag_name = str(input('Image for modification: '))
    file_text_name = str(input('Data for image modification: '))
    secret_data = ''
    with open(file_text_name) as inf:
        for line in inf:
            secret_data += line

    encoded_image = encode_image(image_name=file_imag_name, secret_data=secret_data)
    cv2.imwrite("encoded_image.png", encoded_image)


def decoded_start():
    file_imag_name = str(input('Modified image: '))
    file_text_name = str(input('Extract data to: '))
    decoded_data = decode_image(file_imag_name)
    with open(file_text_name, 'w') as ouf:
        ouf.write(decoded_data)


def command_line():
    while True:
        print('| Encode || Decode || Exit |')
        command = str(input('Enter command: '))
        if command.lower() == 'encode':
            encoded_start()
        elif command.lower() == 'decode':
            decoded_start()
        elif command.lower() == 'exit':
            break
        else:
            print('There is no such command...')


command_line()
