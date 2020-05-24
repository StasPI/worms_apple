from cryptography.fernet import Fernet
import os


def write_key():
    # Generates a key and save it into a file
    key = Fernet.generate_key()
    return key


def encrypt_file(filename, key):
    # Given a filename (str) and key (bytes), it encrypts the file and write it
    f = Fernet(key)
    try:
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)
    except:
        pass


def decrypt_file(filename, key):
    # Given a filename (str) and key (bytes), it decrypts the file and write it
    f = Fernet(key)
    try:
        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)
    except:
        pass


def e_d_directory(path, key):
    key = key
    tree = os.walk(path)
    for folder in tree:
        for file in folder[2]:
            full_path = os.path.join(folder[0], file)
            # encrypt_file(filename=full_path, key=key)
            decrypt_file(filename=full_path, key=key)




# key = write_key()
# print(key)


def command_line():
    print('| Encrypt || Decrypt |')
    command = str(input('Enter command: '))
    if command.lower() == 'encrypt':
        print('| File || Directory |')
        command = str(input('Enter type: '))
        if command.lower() == 'file':
            filename = str(input('Enter file name: '))
            encrypt_file(filename, key)
        elif command.lower() == 'directory':
            path = str(input('Enter directory path: '))
            e_d_directory(path, key)
    elif command.lower() == 'decrypt':
        print('| File || Directory |')
        command = str(input('Enter type: '))
        if command.lower() == 'file':
            filename = str(input('Enter file name: '))
            key = input('Enter key: ')
            decrypt_file(filename, key)
        elif command.lower() == 'directory':
            path = str(input('Enter directory path: '))
            key = input('Enter key: ')
            e_d_directory(path, key)



# class EncryptDecrypt:
#     def encrypt_file(filename, key):
#         f = Fernet(key)
#         try:
#             with open(filename, "rb") as file:
#                 file_data = file.read()
#             encrypted_data = f.encrypt(file_data)
#             with open(filename, "wb") as file:
#                 file.write(encrypted_data)
#         except:
#             pass
#
#     def decrypt_file(filename, key):
#         f = Fernet(key)
#         try:
#             with open(filename, "rb") as file:
#                 encrypted_data = file.read()
#             decrypted_data = f.decrypt(encrypted_data)
#             with open(filename, "wb") as file:
#                 file.write(decrypted_data)
#         except:
#             pass
#
#     def encrypt_directory(path, key):
#         tree = os.walk(path)
#         for folder in tree:
#             for file in folder[2]:
#                 full_path = os.path.join(folder[0], file)
#                 EncryptDecrypt.encrypt_file(full_path, key)
#
#     def decrypt_directory(path, key):
#         tree = os.walk(path)
#         for folder in tree:
#             for file in folder[2]:
#                 full_path = os.path.join(folder[0], file)
#                 EncryptDecrypt.decrypt_file(full_path, key)
#
#
# def write_key():
#     # Generates a key and save it into a file
#     key = Fernet.generate_key()
#     return key
#
#
# # key = write_key()
# # print(key)
# file_name =
# key = input()
# ed = EncryptDecrypt
# # ed.encrypt_directory(file_name, key)
# ed.decrypt_directory(file_name, key)
#
#
#
# # file_name = str(input())
# # key = input()
# # key = key.encode()
# # ed = EncryptDecrypt
# # # ed.encrypt_directory(file_name, key
# # ed.decrypt_directory(file_name, key)