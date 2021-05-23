import telebot
from telebot import types
import config_data
import db_query

client = telebot.TeleBot(config_data.config['token'], parse_mode=None)


@client.message_handler(commands=['start', 'memo', 'help'])
def commands(message):
    if message.text == '/start':
        client.send_message(
            message.chat.id,
            f'Hi. I am @{client.get_me().username}, the test Telegram bot by pecd. Type /help to see the manual.'
        )
    elif message.text == '/memo':
        keyboard = types.InlineKeyboardMarkup()
        key_input = types.InlineKeyboardButton(text='Input', callback_data='input')
        key_output = types.InlineKeyboardButton(text='Output', callback_data='output')
        keyboard.add(key_input, key_output)

        client.send_message(message.from_user.id, text='Choose an option:', reply_markup=keyboard)
    elif message.text == '/help':
        client.send_message(
            message.chat.id,
            '''/start
Restart bot.

/help
Show manual.

/memo
Input/output your message to/from database.

Also bot can reply your greetings.
            '''
        )


@client.callback_query_handler(func=lambda call: True)
def input_output_management(call):
    if call.data == 'input':
        instruction = client.send_message(call.message.chat.id, 'Please type your message.')
        client.register_next_step_handler(instruction, input_message)
    elif call.data == 'output':
        client.send_message(call.message.chat.id, f'Your message:\n{db_query.db_output_message(call.from_user.id)}')


def input_message(message):
    db_query.db_input_message(message.from_user.id, message.from_user.first_name, message.text)


@client.message_handler(content_types=['text'])
def message_processer(message):
    if message.text.lower() in ['hello', 'hello!', 'hi', 'hi!', 'привет', 'привет!']:
        client.send_message(
            message.chat.id,
            f'Hi, {message.from_user.first_name}! 👾'
        )
    else:
        client.send_message(
            message.chat.id,
            f"Sorry, I don't understand you."
        )

client.polling()

