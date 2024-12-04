from pathlib import Path

import pytest

from book_library.repository import RepositoryTask, BookSchema


@pytest.fixture
def repository(tmpdir: Path) -> RepositoryTask:
    json_path = Path(tmpdir / "test_task.json")
    return RepositoryTask(json_path)


@pytest.fixture
def task() -> BookSchema:
    task_ = BookSchema(
        id=1,
        title="Изучить основы FastAPI",
        description="Пройти документация по FastAPI",
        category="Обучение",
        due_date="2024-11-30",
        priority="Высокий",
        status=True,
    )
    return task_


@pytest.fixture
def task_update() -> BookSchema:
    task_ = BookSchema(
        id=1,
        title="Изучить основы FastAPI_update",
        description="Пройти документация по FastAPI_update",
        category="Update category",
        due_date="2024-01-13",
        priority="Низкий",
        status=False,
    )
    return task_
