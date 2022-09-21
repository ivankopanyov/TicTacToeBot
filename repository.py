from abc import ABC, abstractmethod
from sqlite3 import Cursor


class Repository(ABC):

    """
    Абстрактный класс, описывающий репозиторий.
    """
    
    _cursor: Cursor

    """
    Объект курсора модуля sqlite3.
    """

    def __init__(self, cursor: Cursor) -> None:

        """
        Инициализация объекта репозитория.
        """

        self._cursor = cursor
        self._create_table()


    @abstractmethod
    def _create_table(self) -> None:

        """
        Абстрактный метод создания таблицы для хранения состаяния объектов репозитория.
        """

        pass


    @abstractmethod
    def create(self, obj: object) -> None:

        """
        Абстрактный метод создания новой записи в таблицу.
        """

        pass


    @abstractmethod
    def read(self, id: int) -> object | None:

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
    def delete(self, id: int) -> None:

        """
        Абстрактный метод удаления записи из таблицы.
        """

        pass
    

    @abstractmethod
    def exists(self, id: int) -> bool:

        """
        Абстрактный метод проверки наличия записи в таблице.
        """

        pass