from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix='film', sep=';'):
    id: int


def films_keyboard_markup(films_list: list[dict], offset: int | None = None, skip: int | None = None):
    """
    Створює клавіатуру на основі отриманого списку фільмів
    """

    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, film_data in enumerate(films_list):
        callback_data = FilmCallback(id=index, name="")

        builder.button(
            text=f'{film_data["name"]}',
            callback_data=callback_data.pack()
        )

    builder.adjust(1, repeat=True)
    return builder.as_markup()


