from bs4 import BeautifulSoup
from pars_data.connect_requests import go_connect

def parser_domains_zone():
    dom_list = []
    URL = r'https://www.iana.org/domains/root/db'

    soup = BeautifulSoup(go_connect(URL), 'html.parser')

    for td in soup.find_all('td'):
        for span in td.find_all('span'):
            for root_zone in span.find_all(string=True):
                dom_list.append(root_zone)
    return dom_list

class Xyi():
    pass