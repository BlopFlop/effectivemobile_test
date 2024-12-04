import logging
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from book_library.constants import (
    ARG_DELETE,
    ARG_GET,
    ARG_GET_ALL,
    ARG_PATCH,
    ARG_POST,
    ARG_SEARCH,
    AUTHOR_FIELD_HELP_TEXT,
    AVAILABILITY_FIELD_HELP_TEXT,
    CRUD_ARGUMENTS_HELD_TEXT,
    DESCRIPTION_CONSOLE_PROGRAM,
    ID_FIELD_HELP_TEXT,
    JSON_FILE,
    LONG_ARG_AUTHOR,
    LONG_ARG_AVAILABILITY,
    LONG_ARG_ID,
    LONG_ARG_NAME_FIELD,
    LONG_ARG_TITLE,
    LONG_ARG_VALUE,
    LONG_ARG_YEAR,
    NAME_FIELD_HELP_TEXT,
    SHORT_ARG_NAME_FIELD,
    SHORT_ARG_VALUE,
    TITLE_FIELD_HELP_TEXT,
    VALUE_HELP_TEXT,
    YEAR_FIELD_HELP_TEXT,
)
from book_library.outputs import pretty_books_output
from book_library.repository import RepositoryBook
from book_library.utils import except_control


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def get(repository: RepositoryBook, namespace: Namespace) -> None:
    """Get book for id."""
    obj_id = namespace.id

    if obj_id is None:
        warning_message = "Чтобы получить элементы, вы должны передать id"
        logging.warning(warning_message)
        print(warning_message)
        return

    books = repository.get(obj_id=obj_id)
    if isinstance(books, list):
        pretty_books_output(books)
    else:
        pretty_books_output([books])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def get_all(repository: RepositoryBook, namespace: Namespace):
    """Get all books."""
    books = repository.get_all()
    pretty_books_output(books)


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def post(repository: RepositoryBook, namespace: Namespace) -> None:
    """Create book."""
    fields = dict(
        title=namespace.title,
        author=namespace.author,
        year=namespace.year,
        availability=namespace.availability,
    )
    for field_name in fields:
        if fields[field_name] is None:
            warning_message = (
                f"У обязательного поля {field_name} нет значения.",
                "Для создания объекта необходимо дать значение",
                "всех обязательных полей.",
            )
            logging.warning(warning_message)
            print(warning_message)
            return

    new_task = repository.create(**fields)
    pretty_books_output([new_task])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def patch(repository: RepositoryBook, namespace: Namespace) -> None:
    """Update book for id."""
    obj_id = namespace.id
    fields = dict(
        title=namespace.title,
        author=namespace.author,
        year=namespace.year,
        availability=namespace.availability,
    )
    if obj_id is None:
        warning_message = "Для изменения объекта вы должны передать айди."
        logging.warning(warning_message)
        print(warning_message)
        return
    if not any(fields.values()):
        warning_message = (
            "Для изменения объекта хотя бы одно поле с "
            "аргументом для изменения."
        )
        logging.warning(warning_message)
        print(warning_message)
        return
    fields = {name: value for name, value in fields if value is not None}

    update_task = repository.update(obj_id=obj_id, **fields)
    pretty_books_output([update_task])


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def delete(repository: RepositoryBook, namespace: Namespace) -> None:
    """Delete book for id."""
    obj_id = namespace.id

    if obj_id is None:
        warning_message = (
            "Чтобы Удалить элементы, вы должны передать"
            " либо id либо имя категории."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    repository.remove(obj_id=obj_id)
    print("Элементы успешно удалены.")


@except_control(
    value_exc_msg="Элементы не найдены.",
    validate_err_msg="Ошибка валидации в переданных полях.",
)
def search(repository: RepositoryBook, namespace: Namespace) -> None:
    """Search books for field and value."""
    field = namespace.field
    value = namespace.value

    if field is None or value is None:
        warning_message = (
            "Вы должны передать в аргументы поле и значение для поиска."
        )
        logging.warning(warning_message)
        print(warning_message)
        return

    books = repository.get_obj_for_field_arg(field=field, arg=value, many=True)
    pretty_books_output(books)


CRUD = {
    ARG_GET_ALL: get_all,
    ARG_GET: get,
    ARG_POST: post,
    ARG_PATCH: patch,
    ARG_DELETE: delete,
    ARG_SEARCH: search,
}


def parser():
    repository = RepositoryBook(JSON_FILE)

    parser = ArgumentParser(
        description=DESCRIPTION_CONSOLE_PROGRAM,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("crud", choices=CRUD, help=CRUD_ARGUMENTS_HELD_TEXT)

    parser.add_argument(LONG_ARG_ID, type=int, help=ID_FIELD_HELP_TEXT)
    parser.add_argument(LONG_ARG_TITLE, type=str, help=TITLE_FIELD_HELP_TEXT)
    parser.add_argument(LONG_ARG_AUTHOR, type=str, help=AUTHOR_FIELD_HELP_TEXT)
    parser.add_argument(LONG_ARG_YEAR, type=int, help=YEAR_FIELD_HELP_TEXT)
    parser.add_argument(
        LONG_ARG_AVAILABILITY,
        type=lambda x: (str(x).lower() == "true"),
        help=AVAILABILITY_FIELD_HELP_TEXT,
    )
    parser.add_argument(
        SHORT_ARG_NAME_FIELD,
        LONG_ARG_NAME_FIELD,
        type=str,
        help=NAME_FIELD_HELP_TEXT,
    )
    parser.add_argument(
        SHORT_ARG_VALUE, LONG_ARG_VALUE, type=str, help=VALUE_HELP_TEXT
    )

    args: Namespace = parser.parse_args()
    parser_crud = args.crud

    logging.info(f"Программа запущена в режиме {parser_crud}")
    logging.info(f"Переданные аргументы {args}")
    CRUD[parser_crud](repository, namespace=args)
