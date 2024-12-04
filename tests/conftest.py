from pathlib import Path

import pytest

from book_library.repository import BookSchema, RepositoryBook


@pytest.fixture
def repository(tmpdir: Path) -> RepositoryBook:
    json_path = Path(tmpdir / "test_task.json")
    return RepositoryBook(json_path)


@pytest.fixture
def book() -> BookSchema:
    book_ = BookSchema(
        id=1,
        title="Основы Python",
        author="Лутц",
        year=2023,
        availability=True,
    )
    return book_


@pytest.fixture
def book_update() -> BookSchema:
    book_ = BookSchema(
        id=2,
        title="Отцы и дети",
        author="Не Пушкин",
        year=1999,
        availability=False,
    )
    return book_
