from bs4 import BeautifulSoup
from lxml import etree
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def parser_html(url):
    list_of_links = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}")

    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find('div', class_='search-registry-entrys-block')
    all_res = result.find_all('div', class_="w-space-nowrap ml-auto registry-entry__header-top__icon")
    for i in all_res:
        link = i.find('a', attrs={'data-modalup': None})
        red_link = link['href']
        if 'view.html' in red_link:
            red_link = red_link.replace('view.html', 'viewXml.html')
        list_of_links.append('https://zakupki.gov.ru'+red_link)
    return list_of_links


def parser_xml(url):
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}")

    xml = response.text
    soup = BeautifulSoup(xml, 'xml')
    result = soup.find('commonInfo').find('publishDTInEIS')
    if result:
        print(url, '-', result.text)
    else:
        print(url, '-', None)
