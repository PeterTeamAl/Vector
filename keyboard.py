from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# Start Bot

# Agree or Disagree button
agree = KeyboardButton("I agree! 👍")
disagree = KeyboardButton("I disagree!👎")

agrees_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(agree, disagree)
