from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
JSON_FILE: Final[Path] = BASE_DIR / "library_db.json"

LOG_DIR: Final[Path] = BASE_DIR / "logging"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_FILE_NAME: Final[str] = "book_library.log"

# parser constants
DESCRIPTION_CONSOLE_PROGRAM: Final[str] = (
    "Консольная программа для просмотра, приложение для управления \n"
    "библиотекой книг с возможностью добавления, выполнения, удаления и \n"
    "поиска книг."
)

ARG_GET_ALL: Final[str] = "get_all"
ARG_GET: Final[str] = "get"
ARG_POST: Final[str] = "post"
ARG_PATCH: Final[str] = "patch"
ARG_DELETE: Final[str] = "delete"
ARG_SEARCH: Final[str] = "search"

LONG_ARG_ID: Final[str] = "--id"
ID_FIELD_HELP_TEXT: Final[str] = "Идентификатор книги в json."

LONG_ARG_TITLE: Final[str] = "--title"
TITLE_FIELD_HELP_TEXT: Final[str] = "Название книги."

LONG_ARG_AUTHOR: Final[str] = "--author"
AUTHOR_FIELD_HELP_TEXT: Final[str] = "Автор."

LONG_ARG_YEAR: Final[str] = "--year"
YEAR_FIELD_HELP_TEXT: Final[str] = "Год издания."

LONG_ARG_AVAILABILITY: Final[str] = "--availability"
AVAILABILITY_FIELD_HELP_TEXT: Final[str] = "Наличие книги."

SHORT_ARG_NAME_FIELD: Final[str] = "-f"
LONG_ARG_NAME_FIELD: Final[str] = "--field"
NAME_FIELD_HELP_TEXT: Final[str] = "Имя поля."

SHORT_ARG_VALUE: Final[str] = "-v"
LONG_ARG_VALUE: Final[str] = "--value"
VALUE_HELP_TEXT: Final[str] = "Значение для поиска."

CRUD_ARGUMENTS_HELD_TEXT: Final[str] = (
    f"{ARG_GET_ALL} - Получение всех книг.\n"
    f"{ARG_GET} - Получение книг по айди. \n"
    f" Обязательные поля ({LONG_ARG_ID}={ID_FIELD_HELP_TEXT})\n"
    f"{ARG_POST} - Создание книги. \n"
    " Обязательные поля\n"
    f" ({LONG_ARG_TITLE}={TITLE_FIELD_HELP_TEXT},"
    f" {LONG_ARG_AUTHOR}={AUTHOR_FIELD_HELP_TEXT}, \n"
    f" {LONG_ARG_YEAR}={YEAR_FIELD_HELP_TEXT},"
    f" {LONG_ARG_AVAILABILITY}={AVAILABILITY_FIELD_HELP_TEXT}) \n"
    f"{ARG_PATCH} - Обновление книги. Обязательные поля(--id=Идентификатор) \n"
    f" ({LONG_ARG_TITLE}={TITLE_FIELD_HELP_TEXT},"
    f" {LONG_ARG_AUTHOR}={AUTHOR_FIELD_HELP_TEXT}, \n"
    f" {LONG_ARG_YEAR}={YEAR_FIELD_HELP_TEXT},"
    f" {LONG_ARG_AVAILABILITY}={AVAILABILITY_FIELD_HELP_TEXT}) \n"
    f"{ARG_DELETE} - Удаление книги. \n"
    f" Обязательные поля ({LONG_ARG_ID}={ID_FIELD_HELP_TEXT})\n"
    f"{ARG_SEARCH} - Поиск книги по полю и ключевому слову.\n"
    f" Обязательные поля("
    f"{SHORT_ARG_NAME_FIELD}/{LONG_ARG_NAME_FIELD}={NAME_FIELD_HELP_TEXT},"
    f" {SHORT_ARG_VALUE}/{LONG_ARG_VALUE}={VALUE_HELP_TEXT})"
)
