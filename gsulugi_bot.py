#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

USLUGA, SHTRAF_CHOICE, NEXT, BIO, END_OR_NOT, LOCATION, TERAPEVT_CHOICE = range(7)


def start(bot, update):
    reply_keyboard = [[u'Штраф', u'Детсад', u'Поликлиника']]

    update.message.reply_text(
        'Добрый день!' 
        'Я помошник по услугамы Ростовской области. '
        'Для друзей я Дон Ростов. Надеюсь мы подружимся. '
        'Я знаю все об электронных услугах. '
        'Я помогу Вам записаться на прием к врачу, оплатить штраф, ' 
        'отыскать нужное ведомство, проверить очередь в детский сад и многое другое.\n\n' 
        'Сообщите Ваш вопрос:',

        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return USLUGA


def shtraf(bot, update):
    reply_keyboard = [[u'Проверить наличие', u'Произвести оплату']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(  'Уточните, Вы хотите проверить наличие штрафов?'
                                'Или произвести оплату штрафа?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SHTRAF_CHOICE

def terapevt(bot, update):
    reply_keyboard = [[u'09:30', u'12:00', u'15:00']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(  'Вы прикреплены к Городской поликлинике №4.\n'
                                'Доступное время для записи на 15 ноября: 09:30, 12:00 и 15:00\n' 
                                'Терапевт: Иванова Елена\n'
                                'Какое время Вам удобно?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TERAPEVT_CHOICE

def terapevt_accept(bot, update):
    reply_keyboard = [[u'Да', u'Нет']]

    update.message.reply_text(
                                'Давайте проверим данные:\n'
                                'Городская поликлиника №4\n'
                                'Терапевт: Иванова Елена\n'
                                'Дата приема: 15 ноября\n'
                                'Время: 15:00\n'
                                'Все верно?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))    
    return END_OR_NOT

def dummy_usluga(bot, update):
    reply_keyboard = [[u'Штраф', u'Детсад', u'Запись к терапевту']]

    update.message.reply_text(
        'К сожалению в данный момент услуга не реализована!' 
        'Сообщите Ваш вопрос:',

        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return USLUGA

def shtraf_info(bot, update):
    reply_keyboard = [[u'Позднее', u'Оплата']]

    update.message.reply_text(
        'У Вас есть 1 неоплаченный штраф, получен сегодня.'  
        '«показывается штраф»' 
        'В течение 20 дней Вы можете произвести оплату с 50% скидкой.'
        'Вы хотите произвести оплату сейчас?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))    
    return NEXT


def next_usluga(bot, update):
    reply_keyboard = [[u'Да', u'Нет']]

    update.message.reply_text(
        'Хотите еще заказать услугу?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))    
    return END_OR_NOT


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Спасибо! Увидимся!')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():

    TOKEN='792182386:AAHFOAdrw0TndvTTejMYA3HVK21RaX18UKg'
    REQUEST_KWARGS={
        'proxy_url': 'socks5://sr.spry.fail:1080',
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': 'telegram',
            'password': 'telegram',
        }
    }

    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)

   
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            USLUGA: [RegexHandler(u'^(Штраф)$', shtraf),
                     RegexHandler(u'^(Запись к терапевту)$', terapevt),
                     RegexHandler(u'^(Детсад)$', dummy_usluga)],

            SHTRAF_CHOICE: [RegexHandler(u'^(Проверить наличие)$', shtraf_info),
                     RegexHandler(u'^(Произвести оплату)$', dummy_usluga)],

            NEXT: [RegexHandler(u'^(Позднее)$', next_usluga),
                     RegexHandler(u'^(Оплата)$', dummy_usluga)],

            END_OR_NOT: [RegexHandler(u'^(Да)$', dummy_usluga),
                     RegexHandler(u'^(Нет)$', bio)],

            TERAPEVT_CHOICE: [MessageHandler(Filters.text, terapevt_accept)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()