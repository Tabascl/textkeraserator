import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def clean_text(filename):
    text = open(filename, 'r').read()

    soup = BeautifulSoup(text)
    hum_text = soup.get_text()

    clean_text = ''.join([i if ord(i) < 128 else '' for i in text])

    with open('clean_posts.txt', 'w') as f:
        f.write(clean_text)
