from repository import Repository
from user import User


class UsersRepository(Repository):

    """
    Класс, описывающий объект репозитория для записи
    состояния объектов пользователей в таблицу.
    """

    def create(self, user: User) -> None:

        """
        Метод создания новой записи состояния объекта пользователя в таблице.
        """

        self._cursor.execute(f"INSERT INTO {self._table} VALUES ('{user.get_id()}')")

    def read(self, id: str) -> User | None:

        """
        Метод чтения записи состояния объекта пользователя из таблицы.
        """

        res = self._cursor.execute(f"SELECT * FROM {self._table} WHERE id='{id}'")
        result = res.fetchall()
        return None if len(result) == 0 else User(result[0][0])

    def update(self, user: User) -> None:

        """
        Метод обновления записи состояния объекта пользователя в таблице.
        Не имеет имплементации.
        """

        pass

    def delete(self, id: str) -> None:

        """
        Метод удаления записи состояния объекта пользователя из таблицы.
        Не имеет имплементации.
        """

        pass