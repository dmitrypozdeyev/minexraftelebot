from telebot import TeleBot, types
from config import *
from rconadmin import RCONAdmin 

bot = TeleBot(TOKEN)
mcr = RCONAdmin(SERVER_IP, RCON_PASSWORD)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот ркон консоли майнкрафт сервера. Просто отправляй мне команды как будто ты пишешь из в rcon")

@bot.message_handler(commands=["players"])
def showplayers_handler(message : types.Message):
    players = "\n".join(mcr.playerlist())
    bot.send_message(message.chat.id, players)

@bot.message_handler(content_types=["text"])
def text(message : types.Message):
    bot.send_message(message.chat.id, mcr.command(message.text))

bot.infinity_polling()
