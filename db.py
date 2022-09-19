import sqlite3


class DataBase:

    """
    Класс для подключения к базе данных.
    """

    __db_name: str

    """
    Имя базы данных.
    """
    
    def __init__(self, db_name: str) -> None:

        """
        Инициализация объекта класса подключения к базе данных.
        """

        self.__db_name = db_name

    def connect(self) -> sqlite3.Cursor:

        """
        Метод подключения к базе данных.
        """

        con = sqlite3.connect(self.__db_name)
        return con.cursor()