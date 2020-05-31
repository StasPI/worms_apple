import socket
from queue import Queue
from threading import Thread, Lock

from colorama import init, Fore

q = Queue()
n_thread = 200
print_lock = Lock()

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
RED = Fore.RED
host = ''


def scan_port(port):
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{RED}{host:15}:{port:5} is closed {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open {RESET}")
    finally:
        s.close()


def scan_thread():
    while True:
        worker = q.get()
        scan_port(worker)
        q.task_done()


def main(host, ports):
    for t in range(n_thread):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()
    for worker in ports:
        q.put(worker)
    q.join()


if __name__ == '__main__':
    ports = [p for p in range(1, 65535)]
    main(host, ports)
