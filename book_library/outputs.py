import logging

from prettytable import PrettyTable

from book_library.repository import BookSchema


def pretty_books_output(books: list[BookSchema]) -> None:
    task_table = PrettyTable()
    task_table.field_names = (
        "id",
        "title",
        "author",
        "year",
        "availability",
    )
    task_table.align = "l"
    for book in books:
        rows = (
            book.id,
            book.title,
            book.author,
            book.year,
            book.availability,
        )
        task_table.add_row(rows)
    logging.info(f"Выведено {len(books)} книг")
    print(task_table)
