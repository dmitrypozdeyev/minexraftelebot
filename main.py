from telebot import TeleBot, types
from mcrcon import MCRcon
from config import *


bot = TeleBot(TOKEN)
mcr = MCRcon(SERVER_IP, RCON_PASSWORD)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот ркон консоли майнкрафт сервера. Просто отправляй мне команды как будто ты пишешь из в rcon")

@bot.message_handler(content_types=["text"])
def text(message : types.Message):
    mcr.connect()
    resp = mcr.command(message.text)
    bot.send_message(message.chat.id, resp)
    mcr.disconnect()

bot.infinity_polling()