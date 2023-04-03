from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# Start Bot

# Agree or Disagree button
agree = InlineKeyboardButton("I agree! 👍", callback_data='I agree!👍')
disagree = InlineKeyboardButton("I disagree!👎", callback_data='I disagree!👎')

agrees_keyboard = InlineKeyboardMarkup().row(agree, disagree)
