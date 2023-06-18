from bs4 import BeautifulSoup  # для парсинга старниц
import requests  # для запросов к сайту, получения содержимого веб-страницы
import csv

CSV = 'cards.csv'


HOST = 'https://ru.myfin.by/'
URL = 'https://ru.myfin.by/credit-cards'
HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='cards-list-item cards-list-item--requirements')
    cards = []
    for item in items:
        cards.append(
            {
                'Cards_Ttile': item.find('div', class_='cards-list-item__title').get_text(strip=True),
                'link' :  item.find('div', class_='cards-list-item__cell cards-list-item__cell--self-center cards-list-item__name tablet-hidden').find('a').get('href'),
                'Grace_period' : item.find('div', class_ = 'cards-list-item__rate f-bold').get_text(strip=True),
                'credit_limit' :  item.find('div', class_='cards-list-item__cell cards-list-item__cell--with-title cards-list-item__period').get_text(strip=True),
                'cards_img' :  item.find('div', class_='cards-list-item__logo-wrapper').find('img').get('src')
            }
        )
    return cards

def store(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Bank','Link','Grace_period','Credit_limit','img'])
        for item in items:
            writer.writerow([item['Cards_Ttile'], item['link'], item['Grace_period'], item['credit_limit'], item['cards_img']])

def parcer():
    PAGE = input('tell me the number of pages to parse: ')
    PAGE = int(PAGE.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards=[]
        for page in range(1,PAGE):
            print(f'Parse the {page} page')
            html = html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            store(cards,CSV )

        print(cards)
    else:
        print('Error')

parcer()



