from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import google_sheet

BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()
admins = ['', '']
channels = ['', '']

channel_but = InlineKeyboardButton(text='Подписаться',
                                   url='https://t.me/')

channel_key = InlineKeyboardMarkup(inline_keyboard=[[channel_but]])

all_films = google_sheet.get_sheet()


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    print(message.from_user.username)
    await message.answer(text='Ну короче так. Подписываешься на канал и пишешь номер фильма из видоса. Всё.',
                         reply_markup=channel_key)


@dp.message(Command(commands=['update']))
async def update_command(message: Message):
    if not message.from_user.username in admins:
        return
    global all_films
    all_films = google_sheet.get_sheet()
    await message.answer(text='Данные о фильмах успешно обновлены')


@dp.message()
async def message(message: Message):  #

    user_channel_status = await bot.get_chat_member(chat_id=0, user_id=message.from_user.id)

    if user_channel_status.status == 'left':
        await message.answer(text='Для того, чтобы получить доступ ко всем фильмам необходимо подписаться!',
                             reply_markup=channel_key)
        return
    try:
        int(message.text)
    except ValueError:
        await message.answer(text='Для получения данных о фильме необходимо написать только его номер')
        return
    try:
        info = all_films[message.text]
    except KeyError:
        await message.answer(text='Фильм не найден')
        return
    await message.answer_photo(photo=info[1], caption=info[0], reply_markup=channel_key)


if __name__ == '__main__':
    dp.run_polling(bot)  # Запуск бота
