from repository import Repository
from tictactoe import TicTacToe


class TicTacToeRepository(Repository):

    """
    Класс, описывающий объект репозитория для записи
    состояния объектов игр в таблицу.
    """

    def _create_table(self) -> None:

        """
        Метод создания таблицы для хранения состаяния объектов игры.
        """

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS games (id INTEGER, field TEXT, sign TEXT)""")


    def create(self, tictactoe: TicTacToe) -> None:

        """
        Метод создания новой записи состояния объекта игры в таблице.
        """

        field = ''.join(tictactoe.get_field())
        self._cursor.execute("""INSERT INTO games VALUES (?, ?, ?)""", (tictactoe.get_id(), field, tictactoe.get_sign()))


    def read(self, id: int) -> TicTacToe | None:

        """
        Метод чтения записи состояния объекта игры из таблицы.
        """

        res = self._cursor.execute("""SELECT * FROM games WHERE id = ?""", (id,))
        result = res.fetchone()
        if result is None:
            return None
        field = list(result[1])
        return TicTacToe(result[0], field, result[2])


    def update(self, tictactoe: TicTacToe) -> None:

        """
        Метод обновления записи состояния объекта игры в таблице.
        """

        id = tictactoe.get_id()
        if self.read(id) == None:
            return
        field = ''.join(tictactoe.get_field())
        self._cursor.execute("""UPDATE games SET field = ?, sign = ? WHERE id = ?""", (field, tictactoe.get_sign(), tictactoe.get_id()))


    def delete(self, id: int) -> None:

        """
        Метод удаления записи состояния объекта игры из таблицы.
        """

        self._cursor.execute("""DELETE FROM games WHERE id = ?""", (id,))
    

    def exists(self, id: int) -> bool:

        """
        Метод проверки наличия записи игры в таблице.
        """

        res = self._cursor.execute("""SELECT * FROM games WHERE id = ?""", (id,))
        result = res.fetchone()
        return not result is None