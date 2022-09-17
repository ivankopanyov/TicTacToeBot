from sqlite3 import Cursor
from abc import ABC, abstractmethod

class Repository(ABC):

    """
    Абстрактный класс, описывающий репозиторий.
    """
    
    _cursor: Cursor

    """
    Объект курсора модуля sqlite3.
    """

    _table: str

    """
    Имя таблицы, хранящей состояние объектов репозитория.
    """

    def __init__(self, cursor: Cursor, table: str, columns: list[str]) -> None:

        """
        Инициализация объекта репозитория.
        """

        self._cursor = cursor
        self._table = table
        self._create_table(columns)

    def _create_table(self, columns: list[str]) -> None:

        """
        Метод создания таблицы для хранения состаяния объектов репозитория.
        """

        res = self._cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{self._table}'")
        if res.fetchone() is None:
            self._cursor.execute(f"CREATE TABLE {self._table}({', '.join(columns)})")

    @abstractmethod
    def create(self, obj: object) -> None:

        """
        Абстрактный метод создания новой записи в таблицу.
        """

        pass

    @abstractmethod
    def read(self, id: str) -> object | None:

        """
        Абстрактный метод чтения записи в таблицы.
        """

        pass

    @abstractmethod
    def update(self, obj: object) -> None:

        """
        Абстрактный метод обновления записи в таблице.
        """

        pass

    @abstractmethod
    def delete(self, id: str) -> None:

        """
        Абстрактный метод удаления записи из таблицы.
        """

        pass