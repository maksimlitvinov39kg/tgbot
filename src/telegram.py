
import importlib

from database.dapi import DatabaseConnector
import datetime
import telebot

def start_bot():
    token = "6117175686:AAE7Iq2TNjWIcuGfNxuUlB1Y_jwIK4V7Rgo"
    bot = telebot.TeleBot(token)
    epic_connector = DatabaseConnector()

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "Hey boss!")

    @bot.message_handler(commands=['add'])
    def add(message):
        bot.send_message(message.chat.id,'Введите название книги:')
        bot.register_next_step_handler(message, add2)

    def add2(message):
        title = message.text
        bot.send_message(message.chat.id, 'Введите автора:')
        bot.register_next_step_handler(message, lambda message: add3(message, title))

    def add3(message, title):
        author = message.text
        bot.send_message(message.chat.id, 'Введите год издания:')
        bot.register_next_step_handler(message, lambda message: save_book(message, title, author))

    def save_book(message, title, author):
        new_book = DatabaseConnector()
        s = new_book.add(title, author, message.text)
        if s != False:
            bot.send_message(message.chat.id, f'Добавление успешно. ID: {s}')
        else:
            bot.send_message(message.chat.id, 'Ошбибка при добавлении книги')


    @bot.message_handler(commands=['delete'])
    def delete(message):
        bot.send_message(message.chat.id,'Введите название книги:')
        bot.register_next_step_handler(message, delete2)

    def delete2(message):
        title = message.text
        bot.send_message(message.chat.id, 'Введите автора:')
        bot.register_next_step_handler(message, lambda message: delete3(message, title))

    def delete3(message, title):
        author = message.text
        bot.send_message(message.chat.id, 'Введите год издания:')
        bot.register_next_step_handler(message, lambda message: delete_book(message, title, author))

    def delete_book(message, title, author):
        new_book = DatabaseConnector()
        id = new_book.get_book(title, author, message.text)
        if id != None:
            bot.send_message(message.chat.id, f'Найдена книга: {title} {author} {message.text}. Удаляем?')
            bot.register_next_step_handler(message, lambda message: delete_book2(message, id.book_id, new_book))
        else:
            bot.send_message(message.chat.id, f'Книга не найдена')

    def delete_book2(message, id, new_book):
        print(message.text)
        if message.text == 'Да':
           if new_book.delete(id):
               bot.send_message(message.chat.id, f'Книга удалена')
           else:
               bot.send_message(message.chat.id, f'Невозможно удалить книгу')
        else:
            bot.send_message(message.chat.id, f'Okay b0ss')




    @bot.message_handler(commands=['list'])
    def get_list(message):
        for i in epic_connector.list_books():
            bot.send_message(message.chat.id, f'{i["book_id"]} {i["title"]} {i["author"]} {i["published"]}')

    @bot.message_handler(commands=['find'])
    def find1(message):
        bot.send_message(message.chat.id,'Введите название книги:')
        bot.register_next_step_handler(message, find2)

    def find2(message):
        title = message.text
        bot.send_message(message.chat.id, 'Введите автора:')
        bot.register_next_step_handler(message, lambda message: find3(message, title))

    def find3(message, title):
        author = message.text
        bot.send_message(message.chat.id, 'Введите год издания:')
        bot.register_next_step_handler(message, lambda message: find_book(message, title, author))

    def find_book(message, title, author):
        s = epic_connector.get_book(title, author, message.text)
        if s is not None:
            bot.send_message(message.chat.id, f'ID найденной книги: {s.book_id}')
        else:
            bot.send_message(message.chat.id, 'Такой книги нет')

    @bot.message_handler(commands=['borrow'])
    def borrow(message):
        bot.send_message(message.chat.id,'Введите название книги:')
        bot.register_next_step_handler(message, borrow2)

    def borrow2(message):
        title = message.text
        bot.send_message(message.chat.id, 'Введите автора:')
        bot.register_next_step_handler(message, lambda message: borrow3(message, title))

    def borrow3(message, title):
        author = message.text
        bot.send_message(message.chat.id, 'Введите год издания:')
        bot.register_next_step_handler(message, lambda message: borrow_book(message, title, author))

    def borrow_book(message, title, author):
        id = epic_connector.get_book(title, author, message.text)
        if id != None:
            bot.send_message(message.chat.id, f'Найдена книга: {title} {author} {message.text}. Берем?')
            bot.register_next_step_handler(message, lambda message: borrow_book2(message, id.book_id))
        else:
            bot.send_message(message.chat.id, f'Книга не найдена')

    def borrow_book2(message, id):
        print(message.text)
        if message.text == 'Да':
           if epic_connector.borrow(id, message.from_user.id):
               bot.send_message(message.chat.id, f'Вы взяли книгу')
           else:
               bot.send_message(message.chat.id, f'Книгу сейчас невозможно взять :(')
        else:
            bot.send_message(message.chat.id, f'Okay b0ss')


    @bot.message_handler(commands=['retrieve'])
    def retrieve(message):
        br = epic_connector.get_borrow(message.from_user.id)
        if br is not None:
            book = epic_connector.get_book_by_id(br.book_id)
            epic_connector.retrieve(br.borrow_id, datetime.date.today())
            bot.send_message(message.chat.id, f'Вы вернули книгу {book.title} {book.author} {book.published}')
        else:
            bot.send_message(message.char.id, 'Fuck you, b0ss')


    @bot.message_handler(commands=['stats'])
    def stats(message):
        bot.send_message(message.chat.id,'Введите название книги:')
        bot.register_next_step_handler(message, stats2)

    def stats2(message):
        title = message.text
        bot.send_message(message.chat.id, 'Введите автора:')
        bot.register_next_step_handler(message, lambda message: stats3(message, title))

    def stats3(message, title):
        author = message.text
        bot.send_message(message.chat.id, 'Введите год издания:')
        bot.register_next_step_handler(message, lambda message: get_stats(message, title, author))

    def get_stats(message,title,author):
        s = epic_connector.get_book(title, author, message.text)
        if s is not None:

            bot.send_message(message.chat.id, f'Статистика доступна по адресу http://127.0.0.1:5000/download/{s.book_id}/')
        else:
            bot.send_message(message.chat.id, 'Такой книги нет')





    bot.infinity_polling()
