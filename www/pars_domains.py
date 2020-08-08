from bs4 import BeautifulSoup
from connect import go_connect

dom_list = []
URL = r'https://www.iana.org/domains/root/db'

soup = BeautifulSoup(go_connect(URL), 'html.parser')

for td in soup.find_all('td'):
    for span in td.find_all('span'):
        for root_zone in span.find_all(string=True):
            dom_list.append(root_zone)
print(len(dom_list))