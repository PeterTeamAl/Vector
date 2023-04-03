import logging

from aiogram import Bot, Dispatcher, executor, types
from config import Bot_Token as TOKEN
from config import DD_Chat_ID as DCI

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboard import agrees_keyboard as ak

from dbwork import get_to_users, check_db

# configure logging
logging.basicConfig(level=logging.INFO)

# making list for registration
user_data = []

# initializing bot
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
chat = bot.get_chat(DCI)

# Initializing FSM class

class Registration(StatesGroup):
    username = State()
    password = State()
    confirm = State()


# Client part. Get data to DB.
# Start FSM
@dp.message_handler(commands=['register'])
async def cmd_start(message: types.Message):
    await Registration.username.set()

    await message.reply("Hello, what is your name?")
# get username
@dp.message_handler(state=Registration.username)
async def get_name_to_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    user_data.append(data['username'])

    await Registration.next()
    await message.reply("Alright. Now, make a password. Any password you want, make sure to remember it.")
# get password
@dp.message_handler(state=Registration.password)
async def get_password_to_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    user_data.append(data['password'])

    await Registration.next()
    await message.reply("Confirm your password.")
# confirm registration
@dp.message_handler(state=Registration.confirm)
async def confirm_password(message: types.Message, state: FSMContext):
    if message.text == user_data[1]:
        get_to_users(user_data)
        print("Successfully added new user to DB")
        check_db()
        await state.finish()
        user_data.clear()
        await message.answer("I successfully registered you. You need to read rules and agree with it to get the link and join PAT-dev channel.!")
        await message.answer("1. Respect each other. No insults, hate speech, or discrimination will be tolerated. /n2.Keep the conversation on topic. Off-topic messages may be removed. /n3.No spamming or self-promotion allowed. This includes posting links to external websites or channels. /n4.No NSFW content allowed. /n5.No sharing of personal information. /n6.Be mindful of language. Keep the chat clean and appropriate. /n7.Any violation of these rules may result in a warning or ban from the channel or chat.", reply_markup=ak)
        invite = await bot.create_chat_invite_link(DCI, member_limit=1)
        await message.answer(invite.invite_link)
    else:
        print(message.text)
        print(user_data[0])
        print(user_data[1])
        await message.reply("Sorry, passwords do not match. Try to registrate from the beginning.")
        logging.info("Cancelled state %r", await state.get_state())
        await state.finish()
        user_data.clear()


# Check DB methods
# my_list = [input("Enter username: "), input("Enter password: ")]
# get_to_users(my_list)
#
# cursor.execute("SELECT * FROM users")
# values = cursor.fetchall()
#
# for value in values:
#     print(value)

# Admin part


# Other part

# Echo check
# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.reply(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


