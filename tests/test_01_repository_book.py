import pytest
from pydantic_core import ValidationError

from book_library.repository import RepositoryBook
from book_library.schemas import BookSchema
from tests.constants import JSON_INVALID_DATA, JSON_VALID_DATA


class TestRepository:
    """Test class for RepositoryBook.
    It is testing CRUD features for book objects."""

    invalid_id = 999
    invalid_type_title = invalid_id
    invalid_type_author = invalid_id
    invalid_type_date = "Невалидный тип даты"
    invalid_type_availability = invalid_id

    def create_element_in_json(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ) -> int:
        count_item = 20
        count_item_other_category = 80

        book_data = book.model_dump()
        book_data.pop("id")
        for _ in range(count_item):
            repository.create(**book_data)

        book_update_data = book_update.model_dump()
        book_update_data.pop("id")
        for _ in range(count_item_other_category):
            repository.create(**book_update_data)

        return count_item + count_item_other_category

    def test_create_json_file(self, repository: RepositoryBook):
        path_json = repository.path_json
        assert repository.path_json.is_file(), (
            f"После инициализации класса {RepositoryBook.__name__}, "
            f"должен появиться json файл по пути {path_json}."
        )

    def test_read_json_file_data(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        count_elements_confirm = self.create_element_in_json(
            repository, book, book_update
        )
        json_file = RepositoryBook(JSON_VALID_DATA)
        count_elements = len(json_file.get_all())
        assert count_elements == count_elements_confirm, (
            "После чтения валидного файла, результатом должен быть список "
            f"из {count_elements_confirm} объектов, а сейчас {count_elements}."
        )

    def test_read_json_file_invalid_data(self):
        with pytest.raises(ValueError) as ex:
            RepositoryBook(JSON_INVALID_DATA)
            assert ex, (
                "После чтения файла с невалидными данными должна появиться"
                f" ошибка {ValueError.__name__}."
            )

    def test_create_book(self, repository: RepositoryBook, book: BookSchema):
        book_data = book.model_dump()
        book_data.pop("id")

        new_book = repository.create(**book_data)

        assert isinstance(new_book, BookSchema), (
            "После создания книги должен вернуться объект"
            f" {BookSchema.__name__}"
        )

        new_book_data = new_book.model_dump()

        for field, value in book_data.items():
            assert field in new_book_data, (
                f"После создания книги в объекте {BookSchema.__name__} "
                f"должно присутствовать поле {field}"
            )
            assert str(value) == str(new_book_data[field]), (
                f"После создания книги в объекте {BookSchema.__name__} "
                f"Поле {field} должно иметь значение {value}, "
                f"а не {new_book_data[field]}."
            )

    def test_create_book_invalid_data(self, repository: RepositoryBook):
        invalid_data = dict(
            title=self.invalid_type_title,
            author=self.invalid_type_author,
            year=self.invalid_type_date,
            availability=self.invalid_type_availability,
        )
        with pytest.raises(ValidationError) as ex:
            repository.create(**invalid_data)
            assert ex, (
                "При передаче невалидных данных для создания должна"
                f" возникнуть ошибка {ValidationError.__name__}."
            )

    def test_get_all_book(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        count_item = self.create_element_in_json(repository, book, book_update)

        books = repository.get_all()

        assert isinstance(books, list), (
            "При получении всех книг результатом "
            "должен быть список элементов."
        )
        assert len(books) == count_item, (
            "При получении всех элементов из json файла, количество"
            f" элементов должно быть равно {count_item}, а равняется"
            f" {len(books)}."
        )
        assert all(
            map(lambda item: isinstance(item, BookSchema), books)
        ), f"Все книги должны быть типом {BookSchema.__name__}."

    def test_get_book_for_id(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)

        get_book = repository.get(obj_id=book.id)
        assert isinstance(get_book, BookSchema), (
            "При получении элемента по айди, должен "
            f"вернуться единственный элемент с типом {BookSchema.__name__}"
        )
        assert book.model_dump() == get_book.model_dump(), (
            "Все поля и значения из полученной модели по айди, и"
            "поля из первоначальной модели должны быть равны."
        )

    def test_get_book_for_invalid_id(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)
        with pytest.raises(ValueError) as ex:
            repository.get(obj_id=self.invalid_id)
            assert ex, (
                "При передаче невалидных данных для создания должна"
                f" возникнуть ошибка {ValueError.__name__}."
            )

    def test_update_book(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)

        book_data = book.model_dump()
        book_data.pop("id")
        update_book_data = book_update.model_dump()
        update_book_data.pop("id")

        patch_book = repository.update(obj_id=book.id, **update_book_data)
        get_id_patch_book = repository.get(obj_id=book.id)

        patch_book_data = patch_book.model_dump()
        get_id_patch_book_data = get_id_patch_book.model_dump()

        patch_book_id = patch_book_data.pop("id")
        get_id_patch_book_data.pop("id")

        assert book.id == patch_book_id, (
            "Айди объекта после обновления не должен "
            f"измениться, {book.id} != {patch_book_id}"
        )

        for field in book_data:
            fst_value_field = book_data[field]
            update_book_value_field = patch_book_data[field]
            get_id_book_value_filed = get_id_patch_book_data[field]

            assert fst_value_field != update_book_value_field, (
                "После обновления всех полей, значения объекта не "
                "должны быть равны значениям до обновления. "
                f"{fst_value_field} != {update_book_value_field}"
            )
            assert update_book_value_field == get_id_book_value_filed, (
                "После обновления всех полей, у полученного объекта по "
                "айди, все поля должны быть равны. "
                f"{update_book_value_field} != {get_id_book_value_filed}"
            )

    def test_update_book_invalid_data(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        invalid_data = dict(
            title=self.invalid_type_title,
            author=self.invalid_type_author,
            year=self.invalid_type_date,
            availability=self.invalid_type_availability,
        )
        self.create_element_in_json(repository, book, book_update)
        with pytest.raises(ValidationError) as ex:
            repository.update(obj_id=book.id, **invalid_data)
            assert ex, (
                "При получении элемента по несуществующей категори, должна "
                f"возникнуть ошибка {ValidationError.__name__}."
            )

    def test_delete_book_for_id(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)

        for book in repository.get_all()[:]:
            repository.remove(obj_id=book.id)
            new_all_data = repository.get_all()
            delete_book = list(
                filter(lambda book_: book_.id == book.id, new_all_data)
            )
            assert (
                not delete_book
            ), "После удаления объектов из json, он должен быть удален из бд."

    def test_delete_book_for_invalid_id(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)
        with pytest.raises(ValueError) as ex:
            repository.remove(obj_id=self.invalid_id)
            assert ex, (
                "При удалении элемента по несуществующему id, должна "
                f"возникнуть ошибка {ValueError.__name__}."
            )

    def test_search_book_for_keyword_argument(
        self,
        repository: RepositoryBook,
        book: BookSchema,
        book_update: BookSchema,
    ):
        self.create_element_in_json(repository, book, book_update)

        for field in book.model_fields_set:
            book_search = repository.get_obj_for_field_arg(
                field=field, arg=getattr(book, field), many=True
            )
            len_book_search = len(book_search)
            assert len_book_search > 0, (
                f"Поиск сущестующих элементов по полю {field}, "
                "должен дать список с элементами, сейчас он пуст."
            )
            filter_book_search = list(
                filter(
                    lambda book_: getattr(book_, field)
                    == getattr(book, field),
                    book_search,
                )
            )
            len_filter_book_search = len(filter_book_search)
            assert len_filter_book_search == len_book_search, (
                f"Значения поля {field} у всех найденных "
                "элементов должны быть равны."
            )
