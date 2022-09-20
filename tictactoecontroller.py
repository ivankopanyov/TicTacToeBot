from tictactoe import TicTacToe
from tictactoerepository import TicTacToeRepository


class TicTacToeController():

    """
    Класс, описывающий контроллер для работы с объектами игры.
    """

    __repository: TicTacToeRepository

    """
    Объект репозитория игр.
    """

    def __init__(self, repository: TicTacToeRepository) -> None:

        """
        Инициализация объекта класс репозитория игр.
        """

        self.__repository = repository


    def new(self, id: str, size: int) -> list[str]:

        """
        Метод создания новой игры.
        """

        self.__repository.delete(id)
        tictactoe = TicTacToe(id, side = size)
        self.__repository.create(tictactoe)
        return tictactoe.get_field()


    def get(self, id: str) -> tuple([list[str], str]):

        """
        Метод, возвращающий текущее состояние и поле игры.
        """

        tictactoe = self.__repository.read(id)
        if tictactoe is None:
            return None #(self.new(id), TicTacToe.NONE)
        return (tictactoe.get_field(), tictactoe.get_state())


    def move(self, id: str, index: int) -> tuple([list[str], str]):

        """
        Метод хода игрока.
        """

        tictactoe = self.__repository.read(id)
        if tictactoe is None:
            return None #(self.new(id), TicTacToe.NONE)
        result = tictactoe.move(index - 1)
        self.__repository.update(tictactoe)
        return result


    def get_sign(self, id: str) -> str | None:

        """
        Метод, возвращающий символ игрока.
        """

        tictactoe = self.__repository.read(id)
        return None if tictactoe is None else tictactoe.get_sign()


    def delete(self, id: str) -> None:

        """
        Метод удаления игры.
        """

        self.__repository.delete(id)

