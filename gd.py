import goodreads
from goodreads import client
import random
import re


# os.chdir("path") to change the path

def cleanhtml(raw_html):  # cleans from html tags and shorten
    cleanr = re.compile(r'<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    word_list = cleantext.split()
    word_list = word_list[:50]  # shortening the text
    cleantext = str(word_list)
    return cleantext


def text(title, author, cover, review, rating, link):
    info = "{0}\n{1}⭐️  GoodReads\nAuthor: {2}\n{3}\nLink {4}".format(str(title), str(rating), str(author),
                                                                      str(review), str(link))


class GoodreadsClientException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class GoodreadsBook:
    def __init__(self):
        self._client_key = "VAZLR9mDDHl4qgV59PFi1A"
        self._client_secret = "Y0jaiBfS0bVll4RSxMIt2CSa0yPgwjnarCwh0f6TA"

    def authenticate(self):
        self.auth_client = client.GoodreadsClient(self._client_key, self._client_secret)

    def parse_book(self, book):
        return {
            'title': book_data.title,
            'author': book_data.authors[0],
            'rating': book_data.rating,
            'review': cleanhtml(book_data.description),
            'cover': book_data.image_url,
            'link': book_data.link
        }

    def book(self):
        """ Get info about a random book """
        max_book_num = 10000000
        index = random.randint(1, max_book_num)
        book = self.auth_client.book(index)

        return parse_book(book)

    def book_search(self, q, page=1, search_field='all'):
        """ Get the most popular books for the given query. This will search all
        books in the title/author/ISBN fields and show matches, sorted by
        popularity on Goodreads.
        :param q: query text
        :param page: which page to return (default 1)
        :param search_fields: field to search, one of 'title', 'author' or
        'genre' (default is 'all')
        """
        if not q:
            raise GoodreadsClientException("book id or isbn required")
        books = self.auth_client.search_books(str(q), page, search_field)

        return map(parse_book, books)

    def author_search(self, author):
        author = self.auth_client.find_author(str(author))
        return {
            'author_name': author.name,
            'author_books': author.books,
            'author_bio': cleanhtml(author.about),
            'author_pic': author.image_url
        }
