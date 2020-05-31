from datetime import datetime
from queue import Queue
from threading import Thread

import requests

start_time = datetime.now()
q = Queue()
n_threads = 5
domain = 'google.com'
content = ''

with open(r'subdomains.txt', 'r') as inf:
    content = inf.read()

subdomains = content.splitlines()


def scan_subdomains():
    while True:
        url = q.get()
        try:
            requests.get(url, stream=True)
        except requests.ConnectionError:
            pass
        else:
            print('[+] ', url)
        q.task_done()


if __name__ == '__main__':
    for subdomain in subdomains:
        url = f'http://{subdomain}.{domain}'
        q.put(url)

    for t in range(n_threads):
        worker = Thread(target=scan_subdomains)
        worker.daemon = True
        worker.start()

    q.join()

finish_time = datetime.now()
print(finish_time - start_time)
