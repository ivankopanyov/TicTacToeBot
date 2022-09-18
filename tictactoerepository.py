from repository import Repository
from tictactoe import TicTacToe

class TicTacToeRepository(Repository):

    """
    Класс, описывающий объект репозитория для записи
    состояния объектов игр в таблицу.
    """

    def create(self, tictactoe: TicTacToe) -> None:

        """
        Метод создания новой записи состояния объекта игры в таблице.
        """

        field = ''.join(tictactoe.get_field())
        self._cursor.execute(f"INSERT INTO {self._table} VALUES ('{tictactoe.get_id()}', '{field}', '{tictactoe.get_sign()}')")

    def read(self, id: str) -> TicTacToe | None:

        """
        Метод чтения записи состояния объекта игры из таблицы.
        """

        res = self._cursor.execute(f"SELECT * FROM {self._table} WHERE id='{id}'")
        result = res.fetchall()
        if len(result) == 0:
            return None
        field = list(result[0][1])
        return TicTacToe(result[0][0], field, result[0][2])

    def update(self, tictactoe: TicTacToe) -> None:

        """
        Метод обновления записи состояния объекта игры в таблице.
        """

        id = tictactoe.get_id()
        if self.read(id) == None:
            return
        field = ''.join(tictactoe.get_field())
        self._cursor.execute(f"UPDATE {self._table} SET field='{field}', sign='{tictactoe.get_sign()}' WHERE id='{tictactoe.get_id()}'")

    def delete(self, id: str) -> None:

        """
        Метод удаления записи состояния объекта игры из таблицы.
        """

        self._cursor.execute(f"DELETE FROM {self._table} WHERE id='{id}'")