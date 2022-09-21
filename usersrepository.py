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

        self._db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            menu_id INTEGER,
            field_size INTEGER,
            win_line INTEGER
        )""")


    def create(self, user: User) -> None:

        """
        Метод создания новой записи состояния объекта пользователя в таблице.
        """

        self._db.execute("""INSERT INTO users VALUES (?, ?, ?, ?)""", \
            (user.get_id(), user.get_menu_id(), user.get_field_size(), user.get_win_line()))


    def read(self, id: int) -> User:

        """
        Метод чтения записи состояния объекта пользователя из таблицы.
        """

        result = self._db.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        return None if result is None else User(*result)


    def update(self, user: User) -> None:

        """
        Метод обновления записи состояния объекта пользователя в таблице.
        Не имеет имплементации.
        """

        id = user.get_id()
        if not self.exists(id):
            return
        self._db.execute("""UPDATE users SET 
            menu_id = ?,
            field_size = ?,
            win_line = ?
        WHERE id = ?""", (user.get_menu_id(), user.get_field_size(), user.get_win_line(), user.get_id()))


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

        result = self._db.execute("""SELECT id FROM users WHERE id = ?""", (id,))
        return not result is None