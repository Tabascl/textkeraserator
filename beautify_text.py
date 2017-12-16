import warnings
import re

from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def clean_text(filename):
    text = open(filename, 'r', encoding='utf-8').read()

    text = re.sub('<br>', '\n', text)
    text = re.sub('\n+', '\n', text)
    text = ''.join([i if ord(i) < 128 else '' for i in text])

    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()

    clean_text = re.sub('>>[0-9]+', '', text)


    with open('clean_posts.txt', 'w') as f:
        f.write(clean_text)


if __name__ == '__main__':
    clean_text('raw_posts.txt')
