import logging

from aiogram import types, executor, Dispatcher, Bot
from config import Kvant_Token as TOKEN

from aiogram.dispatcher.filters import BoundFilter, Command

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# filters
class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check_admin(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()

# register filters
dp.filters_factory.bind(AdminFilter)


@dp.message_handler(commands=['start'])
async def check(message: types.Message):
    await message.reply("Hi there! I'm Kvant. Bot, that will be watching this group and i'm going to help you get news.")

@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix=['!'])
async def ban_member(message: types.Message):
    await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)