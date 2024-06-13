from telebot import TeleBot, types
from rconadmin import RCONAdmin
from config import *
from telebotadmin import Telebotadmin

bot = TeleBot(TOKEN)
mcr = RCONAdmin(SERVER_IP, RCON_PASSWORD)
adm = Telebotadmin(bot)


def playersmenu(prefix):
    menu = types.InlineKeyboardMarkup()
    for player in mcr.playerlist():
        menu.add(types.InlineKeyboardButton(text=f"{player}", callback_data=f"{prefix}{player}"))
    return menu


def itemsmenu(items: dict, prefix):
    menu = types.InlineKeyboardMarkup()
    for item in items.keys():
        menu.add(types.InlineKeyboardButton(text=f"{items[item]}", callback_data=f"{prefix}{item}"))
    return menu


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    adm.adduserm(message)
    bot.send_message(message.chat.id,
                     f"Привет, я RCON бот городка Данилы. Вы зарегистрированы как {adm.getpermm(message)}.")


@bot.message_handler(commands=['playerlist'])
@adm.setaccess(2)
def playerlist_handler(message: types.Message):
    players = "\n".join(mcr.playerlist())
    bot.send_message(message.chat.id, f"Игроки на сервере:\n{players}")


@bot.message_handler(commands=['givedoc'])
@adm.setaccess(1)
def givedoc_selectuser(message: types.Message):
    bot.send_message(message.chat.id, "Выберите игрока", reply_markup=playersmenu("doc!"))


@bot.callback_query_handler(func=lambda call: "doc!" in call.data)
def givedoc_selectdoc(callback: types.CallbackQuery):
    player = callback.data[4:]
    bot.send_message(callback.message.chat.id, "Выберите документ", reply_markup=itemsmenu(DOCS, f"{player}|doc|"))


@bot.callback_query_handler(func=lambda call: "|doc|" in call.data)
def givedoc_gice(callback: types.CallbackQuery):
    player, document = callback.data.split("|doc|")
    mcr.givedoc(player, document)
    bot.send_message(callback.message.chat.id, f"Документ {DOCS[document]} выдан игроку {player}")


@bot.message_handler(commands=['giveweitem'])
@adm.setaccess(1)
def giveitem_selectitem(message: types.Message):
    bot.send_message(message.chat.id, "Выберите предмет", reply_markup=itemsmenu(ARMOR, "itm!"))


@bot.callback_query_handler(func=lambda call: "itm!" in call.data)
def giveitem_selectplayer(callback: types.CallbackQuery):
    item = callback.data[4:]
    bot.send_message(callback.message.chat.id, "Выберите игрока", reply_markup=playersmenu(f"{item}|itm|"))


@bot.callback_query_handler(func=lambda call: "|itm|" in call.data)
def giveitem_give(callback: types.CallbackQuery):
    item, player = callback.data.split("|itm|")
    mcr.giveitem(player, item)
    bot.send_message(callback.message.chat.id, f"Предмет {ARMOR[item]} выдан игроку {player}")


@bot.message_handler(commands=['giveweapon'])
@adm.setaccess(1)
def giveweapon_selectweapon(message: types.Message):
    bot.send_message(message.chat.id, "Выберите оружие", reply_markup=itemsmenu(WEAPONS, "wpn!"))


@bot.callback_query_handler(func=lambda call: "wpn!" in call.data)
def giveweapon_selectplayer(callback: types.CallbackQuery):
    weapon = callback.data[4:]
    bot.send_message(callback.message.chat.id, "Выберите игрока", reply_markup=playersmenu(f"{weapon}|wpn|"))


@bot.callback_query_handler(func=lambda call: "|wpn|" in call.data)
def giveweapon_give(callback: types.CallbackQuery):
    weapon, player = callback.data.split("|wpn|")
    mcr.giveweapon(player, weapon)
    bot.send_message(callback.message.chat.id, f"Оружие {WEAPONS[weapon]} выдано игроку {player}")


@bot.message_handler(commands=['incperm'])
@adm.setaccess(2)
def incperm(message: types.Message):
    adm.requestperminc(message)


if __name__ == '__main__':
    bot.infinity_polling()
