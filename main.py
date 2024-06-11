from telebot import TeleBot, types
from config import *
from rconadmin import RCONAdmin 

bot = TeleBot(TOKEN)
mcr = RCONAdmin(SERVER_IP, RCON_PASSWORD)
users = {}

def playersmenu():
    menu = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    for player in mcr.playerlist():
        menu.add(types.KeyboardButton(player))
    return menu

def playersinlinemenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    for player in mcr.playerlist():
        menu.add(types.InlineKeyboardButton(text=player, callback_data=f"qap{player}"))
    return menu

def weaponsmenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    for weapon in WEAPONS.keys():
        menu.add(types.InlineKeyboardButton(text=weapon, callback_data=f"weapon{WEAPONS[weapon]}"))
    return menu

def itensmenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    for armor in ARMOR.keys():
        menu.add(types.InlineKeyboardButton(text=armor, callback_data=f"item{ARMOR[armor]}"))
    return menu

def docsmenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    for docname in DOCS.keys():
        menu.add(types.InlineKeyboardButton(text=docname, callback_data=DOCS[docname]))
    return menu


def selectdoc(message : types.Message):
    users[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Какой документ вы ходите выдать игроку {users[message.chat.id]}?", reply_markup=docsmenu())



@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот ркон консоли майнкрафт сервера. Просто отправляй мне команды как будто ты пишешь из в rcon")

@bot.message_handler(commands=["playerlist"])
def showplayers_handler(message : types.Message):
    players = "\n".join(mcr.playerlist())
    bot.send_message(message.chat.id, players)

@bot.message_handler(commands=["giveweapon"])
def giveweapon_handler(message : types.Message):
    bot.send_message(message.chat.id, "Какое оружие вы хотите выдать", reply_markup=weaponsmenu())

@bot.callback_query_handler(func = lambda call : call.data.startswith("weapon"))
def giveweapon_handler(callback : types.CallbackQuery):
    users[callback.message.chat.id] = callback.data
    bot.send_message(callback.message.chat.id, f"Кому вы хотите выдать оружие?", reply_markup=playersinlinemenu())

@bot.callback_query_handler(func = lambda call : call.data.startswith("qap") and users[call.message.chat.id].startswith("weapon"))
def giveweapon_handler(callback : types.CallbackQuery):
    weapon = users[callback.message.chat.id][6:]
    mcr.giveweapon(callback.data[3:], weapon)
    bot.send_message(callback.message.chat.id, f"Выдано оружие {weapon} игроку {callback.data[3:]}")

@bot.message_handler(commands=["giveitem"])
def giveitem_handler(message : types.Message):
    bot.send_message(message.chat.id, "Какой предмет вы хотите выдать", reply_markup=itensmenu())

@bot.callback_query_handler(func = lambda call : call.data.startswith("item"))
def giveitem_handler(callback : types.CallbackQuery):
    users[callback.message.chat.id] = callback.data
    bot.send_message(callback.message.chat.id, f"Кому вы хотите выдать предмет?", reply_markup=playersinlinemenu())


@bot.callback_query_handler(func = lambda call : call.data.startswith("qap") and users[call.message.chat.id].startswith("item"))
def giveitem_handler(callback : types.CallbackQuery):
    item = users[callback.message.chat.id][4:]
    mcr.giveitem(callback.data[3:], item)
    bot.send_message(callback.message.chat.id, f"Выдан предмет {item} игроку {callback.data[3:]}")

@bot.message_handler(commands=["givedoc"])
def givedoc_handler(message : types.Message):
    bot.send_message(message.chat.id, "Кому вы хотите выдать документ", reply_markup=playersmenu())
    bot.register_next_step_handler(message, selectdoc)

@bot.callback_query_handler(func = lambda call : True)
def givegoc_handler(callback : types.CallbackQuery):
    mcr.givedoc(users[callback.message.chat.id], callback.data)
    bot.send_message(callback.message.chat.id, f"Выдан документ игроку {users[callback.message.chat.id]}")



@bot.message_handler(content_types=["text"])
def text(message : types.Message):
    bot.send_message(message.chat.id, mcr.command(message.text))

if __name__ == "__main__": bot.infinity_polling()
