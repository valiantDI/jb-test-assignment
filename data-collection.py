import os
import pyautogui
import requests
from bs4 import BeautifulSoup
from typing import List, TypeVar

T = TypeVar("T")
HOST = 'https://github.com/'
URL = 'https://github.com/iisuslik43/2021-test-assignment'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/'
              '*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.90 Safari/537.36'
}


def get_html(url: str) -> str:
    if requests.get(url, headers=HEADERS).status_code == 200:
        return requests.get(url, headers=HEADERS).text


def get_title_and_links(html_doc: str, catalog: List[T]) -> List[dict]:
    """
    This function parses the names and links to python files from the repository
    """
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('div', class_='Box-row')
    for item in items:
        if item.find('a').get('title') == 'Go to parent directory':
            continue
        elif (HOST + item.find('a').get('href')).count('.') == 1:
            html_doc = get_html(HOST + item.find('a').get('href'))
            soup = BeautifulSoup(html_doc, 'html.parser')
            items = soup.find_all('div', class_='Box-row')
            get_title_and_links(html_doc, catalog)
        elif (HOST + item.find('a').get('href')).count('.py') == 1 and item.find('a').get('title') != '__init__.py':
            catalog.append(
                {
                    'title': item.find('a').get('title'),
                    'link': HOST + item.find('a').get('href')
                }
            )
    return catalog


def get_raw_links(html_py: str) -> str:
    """
    Function for getting links to raw python files from a repository
    """
    soup = BeautifulSoup(html_py, 'html.parser')
    for link in soup.find_all('div', class_='BtnGroup'):
        return HOST + link.find('a').get('href')


def get_code(link: str) -> str:
    return requests.get(link).text


def save_code(code_text: str, title: str):
    file_path = 'code-text/' + title + '.txt'
    with open(file_path, 'w') as file:
        file.write(code_text)
    return file


def screenshot(title: str):
    input_path = 'code-text\\' + title + '.txt'
    output_path = 'screenshots\\' + title + '.screenshot.png'
    os.startfile(input_path)
    pyautogui.sleep(0.5)
    x, y = pyautogui.locateCenterOnScreen(r'top_left.png')
    x1, y1 = pyautogui.locateCenterOnScreen(r'bottom_right.png')
    pyautogui.screenshot(output_path, region=(x - 25, y + 10, x1 - x, y1 - y - 20))
    x2, y2 = pyautogui.locateCenterOnScreen(r'close.png')
    pyautogui.moveTo(x2, y2)
    pyautogui.click(x2, y2)
    pyautogui.moveTo(x2 + 50, y2 + 50)


if __name__ == '__main__':
    python_files = []
    items = get_title_and_links(get_html(URL), python_files)
    for item in items:
        raw_link = get_raw_links(get_html(item['link']))
        code = get_code(raw_link)
        save_code(code, item['title'])
        screenshot(item['title'])
