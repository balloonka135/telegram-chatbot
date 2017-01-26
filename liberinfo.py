import time
import telebot
from telebot import types
import gd
from gd import GoodreadsBook
from gd import GoodreadsClientException

greeting = """
    ✋ Welcome to LiberInfo bot 📚
We are a community of book lovers.
This is an inline bot, that make its easy to find a book you are interested in.
Also, we have some more cool features, type /help to find about them.
Enjoy!
"""

help_ = """
To find any kind of book, just type @LiberInfo_bot and a book title or author's name.
Inside a chat you can use /author command to get a brief info about the author 
you are interested in, for example:
/author J.K.Rowling
Also, if you want to explore the book world, you can type /random and get the 
random book from GoodReads repository
"""

_token = '298429549:AAHNxMxVkVI0Qv-8jDisG2Xzjw7QllQQL2g'
bot = telebot.TeleBot(_token)

books = GoodreadsBook()
books = books.authenticate()


# Handles all text messages that contains the commands '/start'
@bot.message_handler(commands=['start'])  # greeting
def send_welcome(message):
    bot.reply_to(message.chat.id, greeting)


@bot.message_handler(commands=['help'])  # command list
def send_welcome(message):
    bot.reply_to(message.chat.id, help_)


@bot.message_handler(commands=['random'])  # /random
def random(message):
    book = books.book()
    text = "Your result: {}".format(text(book['title'], book['author'], book['cover'],
                                  book['review'], book['rating'], book['link']))
    bot.send_message(message.chat.id, text, disable_web_page_preview=False)


@bot.message_handler(commands=['author'])
def author_info(message):
    auth = books.author_search(message)
    text = "{0} \nListopia: \n{1} \nShort bio\n {2}".format(str(auth['author_name']),
                                                            str(auth['author_books']), str(auth['author_bio']))
    bot.send_message(message.chat.id, text, disable_web_page_preview=False)


@bot.inline_handler(lambda query: query.query == 'text')  # inline session
def query_text(query):
    book_req = books.book_search(query)
    try:
        result = []
        for i, book in enumerate(book_req):
            if i > 20:  # not to overload
                break
            result.append(types.InlineQueryResultArticle(id=i,
                                                         title=book['title'],
                                                         hide_url=True,
                                                         thumb_url=book['cover'], thumb_width=48, thumb_height=48,
                                                         input_message_content=InputTextMessageContent(
                                                         message_text="Result for '{0}':\n{1}".format(query, gd.text(
                                                                 book['title'],
                                                                 book['author'], book['cover'], book['review'],
                                                                 book['rating'], book['link'])
                                                         )))
        bot.answer_inline_query(query.id, result)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


def main_loop():
    bot.polling()
    while 1:
        time.sleep(10)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)
