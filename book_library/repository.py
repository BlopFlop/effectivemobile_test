import logging
from functools import wraps
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter
from pydantic_core import ValidationError

from book_library.schemas import BookSchema, BookSchemaUpdate


class RepositoryBook:
    """Base CRUD operations for Book objects."""

    __book_adapter = TypeAdapter(list[BookSchema])

    def __init__(self, path_json: Path):
        self.path_json = self.__get_or_create_json(path_json)
        self.data = self.__get_data()

    @property
    def __autoincrement_id(self) -> int:
        """Property method for unique id in objects."""
        if not self.data:
            return 1
        ids = map(lambda book: book.id, self.data)
        return max(ids) + 1

    def __get_or_create_json(self, path_file: Path) -> Path:
        """Private method for check or create json file."""
        if not path_file.is_file():
            with open(path_file, mode="w", encoding="utf-8"):
                logging.info(f"Создан json файл {path_file.name}.")
        return path_file

    def __get_data(self) -> list[BookSchema]:
        """Get data in json file."""
        with open(self.path_json, mode="r", encoding="utf-8") as json_file:
            json_data = json_file.read()
            if not json_data:
                return []

            try:
                obj_data = self.__book_adapter.validate_json(json_data)
            except ValidationError:
                except_message = (
                    f"Файл {self.path_json.name} в корне проекта имеет"
                    " невалидные данные, получение данных из него невозможно,"
                    " пожалуйста перенесите его в другое место."
                )
                logging.error(except_message)
                raise ValueError(except_message)

        return obj_data

    def update_data_transaction(func):
        """Decorator transaction for change json file."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self: RepositoryBook = args[0]

            result = func(*args, **kwargs)
            with open(self.path_json, mode="w", encoding="utf-8") as json_file:
                json_data = self.__book_adapter.dump_json(
                    self.data, indent=4
                ).decode()
                json_file.write(json_data)

                logging.info(
                    f"В json перезаписано {len(self.data)} элементов."
                )
            return result

        return wrapper

    def get(self, obj_id: int) -> BookSchema | list[BookSchema]:
        """Get book model for id or category."""
        return self.get_obj_for_field_arg("id", obj_id, False)

    def get_all(self) -> list[BookSchema]:
        return self.data

    @update_data_transaction
    def create(self, **kwargs) -> BookSchema:
        """Create book."""
        book_new_obj = BookSchema(id=self.__autoincrement_id, **kwargs)
        self.data.append(book_new_obj)

        logging.info(f"Создана книга {book_new_obj}.")
        return book_new_obj

    @update_data_transaction
    def update(self, obj_id: int, **kwargs) -> BookSchema:
        """Update book for id or other fields."""
        obj_db = self.get(obj_id)
        obj_data = obj_db.model_dump()

        obj_update = BookSchemaUpdate(**kwargs)
        obj_update_data = obj_update.model_dump()

        for field in obj_data:
            if field not in obj_update_data:
                continue
            if obj_update_data.get(field) is not None:
                setattr(obj_db, field, obj_update_data[field])

        logging.info(f"Изменена книга id {obj_id} поля {obj_update_data}.")
        return obj_db

    @update_data_transaction
    def remove(self, obj_id: int) -> None:
        """Delete book for id or category."""
        self.get_obj_for_field_arg("id", obj_id, False)
        self.data = list(filter(lambda book: book.id != obj_id, self.data))
        logging.info(f"Книга под id {obj_id} удалена.")

    def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        """Get book for keyword argument."""
        filter_data = list(
            filter(
                lambda book: str(getattr(book, field)) == str(arg), self.data
            )
        )

        if not filter_data:
            except_message = (
                f"Элементы по полю: {field} и аргументу: {arg} не найдены."
            )
            logging.error(except_message)
            raise ValueError(except_message)

        if many:
            return filter_data
        return filter_data[0]
