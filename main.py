import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile, CallbackQuery, ReplyKeyboardRemove

from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from utils.commands import FILMS_COMMAND, FILM_CREATE_COMMAND

from data_film.data import get_films, add_film
from keyboards.inline_keyboards import films_keyboard_markup, FilmCallback
from models.models import Film
from utils.states import FilmForm
import logging


load_dotenv()

TOKEN: str = os.getenv("TOKEN")

dp = Dispatcher()

logger = logging.getLogger(__name__)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Вітаю, {html.bold(message.from_user.full_name)}!\n"
                         f"Я перший бот, Python розробника - Кондратюка ОСтапа")


@dp.message(FILMS_COMMAND)
async def command_start_handler(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)

    await message.answer(f"Перелік фільмів. Натисність на назву для отримання деталей", reply_markup=markup)





@dp.message(FILM_CREATE_COMMAND)
async def command_start_handler(message: Message, state:FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.name)
    await message.answer(
       f'Введіть назву фільмую',
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Введіть опис фільму', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FilmForm.description)


@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(f'Введіть рейтинг фільму від 0 до 10', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FilmForm.rating)


@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=message.text)
    await message.answer(f'Введіть жанр фільму', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FilmForm.genre)


@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await message.answer(
        text=f"Введіть акторів фільму через роздільник ', '\n"
             + html.bold("Обов'язкова кома та відступ після неї."),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(FilmForm.actors)


@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    actors_list = [actor.strip() for actor in message.text.split(',')]

    await state.update_data(actors=actors_list)
    await message.answer(f'Введіть постер фільму', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FilmForm.poster)


@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    data = await state.update_data(poster=message.text)
    film = Film(**data)
    add_film(film.model_dump())
    await state.clear()
    await message.answer(f'Фільм {film.name} успішно додано!',
                         reply_markup=ReplyKeyboardRemove())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
