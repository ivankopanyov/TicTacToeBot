from repository import Repository
from user import User


class UsersRepository(Repository):

    """
    Класс, описывающий объект репозитория для записи
    состояния объектов пользователей в таблицу.
    """

    def _create_table(self) -> None:

        """
        Метод создания таблицы для хранения состаяния объектов пользователя.
        """

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER)""")


    def create(self, user: User) -> None:

        """
        Метод создания новой записи состояния объекта пользователя в таблице.
        """

        self._cursor.execute("""INSERT INTO users VALUES (?)""", (user.get_id(),))


    def read(self, id: int) -> User | None:

        """
        Метод чтения записи состояния объекта пользователя из таблицы.
        """

        res = self._cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        result = res.fetchone()
        return None if result is None else User(result[0])


    def update(self, user: User) -> None:

        """
        Метод обновления записи состояния объекта пользователя в таблице.
        Не имеет имплементации.
        """

        pass


    def delete(self, id: int) -> None:

        """
        Метод удаления записи состояния объекта пользователя из таблицы.
        Не имеет имплементации.
        """

        pass
    

    def exists(self, id: int) -> bool:

        """
        Метод проверки наличия записи пользователя в таблице.
        """

        res = self._cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        return not res.fetchone() is None