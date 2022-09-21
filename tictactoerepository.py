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

        self._db.execute("""CREATE TABLE IF NOT EXISTS games (
            id INTEGER, 
            field TEXT, 
            sign TEXT, 
            win_line INTEGER
        )""")


    def create(self, tictactoe: TicTacToe) -> None:

        """
        Метод создания новой записи состояния объекта игры в таблице.
        """

        field = ''.join(tictactoe.get_field())
        self._db.execute("""INSERT INTO games VALUES (?, ?, ?, ?)""", (tictactoe.get_id(), field, tictactoe.get_sign(), tictactoe.get_win_line()))


    def read(self, id: int) -> TicTacToe:

        """
        Метод чтения записи состояния объекта игры из таблицы.
        """

        result = self._db.execute("""SELECT * FROM games WHERE id = ?""", (id,))
        if result is None:
            return None
        field = list(result[1])
        return TicTacToe(result[0], field, result[2])


    def update(self, tictactoe: TicTacToe) -> None:

        """
        Метод обновления записи состояния объекта игры в таблице.
        """

        id = tictactoe.get_id()
        if not self.exists(id):
            return
        field = ''.join(tictactoe.get_field())
        self._db.execute("""UPDATE games SET field = ? WHERE id = ?""", (field, tictactoe.get_id()))


    def delete(self, id: int) -> None:

        """
        Метод удаления записи состояния объекта игры из таблицы.
        """

        self._db.execute("""DELETE FROM games WHERE id = ?""", (id,))
    

    def exists(self, id: int) -> bool:

        """
        Метод проверки наличия записи игры в таблице.
        """

        result = self._db.execute("""SELECT * FROM games WHERE id = ?""", (id,))
        return not result is None