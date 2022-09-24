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


    def execute(self, sql: str, parameters: list[object] = []):

        """
        Метод запроса к базе данных.
        """

        con = sqlite3.connect(self.__db_name)
        cursor = con.cursor()
        exec = cursor.execute(sql, tuple(parameters))
        result = exec.fetchone()
        con.commit()
        con.close()
        return result

