import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://www.litres.ru'
FILE = 'books.csv'
URL = 'https://www.litres.ru/knigi-fentezi/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='mgrid')
    books = []
    for item in items:
        books.append(
            {
                'title': item.find('a', class_='art__name__href').get_text(strip=True),
                'link_product': HOST + item.find('a', class_='art__name__href').get('href'),
                'author': item.find('div', class_='art__author').get_text(strip=True),
                'rating': item.find('div', class_='bottomline-rating').get_text()
            }
        )
    return books


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Link on the book', 'Rating of users'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['link_product'], item['rating']])


def parser():
    pagenation = input('Колличество сртаниц лдя парсинга: ')
    pagenation = int(pagenation.strip())
    html = get_html(URL)
    if html.status_code == 200:
        books = []
        for page in range(1, pagenation + 1):
            print(f'Производится парсинг страницы: {page} из {pagenation}')
            html = get_html(URL, params={'page': page})
            books.extend(get_content(html.text))
        save_file(books, FILE)
        print('Парсинг страниц завершён')
    else:
        print('Error')


parser()