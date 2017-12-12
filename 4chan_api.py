import json
import itertools
from multiprocessing import Pool
from urllib.error import HTTPError
from urllib.request import urlopen

boards_url = "https://a.4cdn.org/boards.json"
threads_url = "https://a.4cdn.org/{0}/threads.json"
posts_url = "https://a.4cdn.org/{0}/thread/{1}.json"


def _get_boards():
    '''Returns a list of boards as their abbrevations'''
    board_json = json.loads(urlopen(boards_url).read())

    boards = []
    for entry in board_json['boards']:
        boards.append(entry['board'])

    return boards


def _get_threads(boards):
    '''Return a list of tuples with `(board, threadnumber)`'''
    threads = []

    for board in boards:
        threads_json = json.loads(urlopen(threads_url.format(board)).read())
        for page in threads_json:
            for thread in page['threads']:
                threads.append((board, thread['no']))

    return threads


def _get_posts(board, thread):
    '''Return a list of posts'''
    print("Getting thread {0} from board {1}".format(thread, board))
    posts = []

    try:
        posts_json = json.loads(
            urlopen(posts_url.format(board, thread)).read())
    except HTTPError:
        return []

    for post in posts_json['posts']:
        try:
            posts.append(post['com'])
        except KeyError:
            continue

    return posts


boards = _get_boards()
threads = _get_threads(boards)

with Pool(8) as p:
    posts = p.starmap(_get_posts, threads)

posts = itertools.chain.from_iterable(posts)

print("Successfully fetched {0} posts. Saving to file...".format(len(posts)))

with open("raw_posts.txt", "w") as f:
    for post in posts:
        f.write(post + '\n')

print("Done!")
