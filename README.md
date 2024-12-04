# test_higthlenth
## О проекте 
Консольное приложение для управления библиотекой книг с 
возможностью добавления, выполнения, удаления и поиска книг

# Автор:
- BlopFlop - Артур Юнгблюд

# Технологии:
- python 3.11.2
- pydantic 2.10.2
- pytest 8.3.3

# Схема директории проекта:
```
effectivemobile_test
│
├── book_library/                       Каталог с файлами проекта
|   ├── __init__.py
|   ├── config.py                       Конфигурация проекта логгирование
|   ├── console_parser.py               Чтение аргументов командной строки
|   ├── constants.py                    Константы
|   ├── outputs.py                      Вывод книг в командной строке
|   ├── repository.py                   Управления книгами
|   ├── schemas.py                      Схемы для книг
|   └── utils.py                        Вспомогательные компоненты
│
├── tests/                              Тестирование
|   ├── conftest.py                     Тестовые компоненты
|   ├── constants.py                    Тестовые константы
|   └── test_01_repository_books.py      Тестирование манипуляции над книгами
│
├── main.py                             Точка входа в программу
│
├── .gitignore                          Что игнорировать в Git
├── requirements.txt                    Основные зависимости проекта
├── pyproject.toml                      Настройки для black
└── README.md                           Этот файл
```

# Поля у модели книга:
- **id** - int Autoincrement. Идентификатор в json.
- **title** - str. Название книги.
- **author** - str. Автор.
- **year** - int. Год издания.
- **availability** - bool. Наличие книги

# Аргументы командной строки:
- **get_all** - Получение всех книг.
- **get --id={}** - Получение книг по айди.
- **post --title={} --author={} --year={} --availability={}** - Создание книги. Обязательные поля(Название книги, Автор, Год издания, Наличие книги).
- **patch --id={} --title={} --author={} --year={} --availability={}** - Изменение книги. Обязательные поля(Идентификатор). Опциональные поля (Название книги, Автор, Год издания, Наличие книги).
- **delete --id={}** - Удаление книги по айди. 
- **search -f={} || -v={}** - Получение книг по имени поля и его значению.

# Инструкция
Клонировать репозиторий:
```
git@github.com:BlopFlop/effectivemobile_test.git
```
Перейти в репо в командной строке
```
cd /effectivemobile_test
```

Cоздать виртуальное окружение:

```
py -3.11 -m venv venv
```
Активировать виртуальное окружение:

```
source venv/Skripts/Activate
```
Обновить pip:

```
py -3.11 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Получить справку для командной строки:
```
python main.py -h
```
Пользоваться.
