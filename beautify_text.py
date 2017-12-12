import warnings
import re

from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def clean_text(filename):
    text = open(filename, 'r').read()

    text = re.sub('<br>', '\n', text)
    text = re.sub('\n+', '\n', text)

    soup = BeautifulSoup(text)
    text = soup.get_text()

    text = re.sub('>>[0-9]+', '', text)

    clean_text = ''.join([i if ord(i) < 128 else '' for i in text])

    with open('clean_posts.txt', 'w') as f:
        f.write(clean_text)


if __name__ == '__main__':
    clean_text('raw_posts.txt')
