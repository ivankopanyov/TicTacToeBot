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


    def new(self, id: int, field_size: int, win_line: int) -> TicTacToe:

        """
        Метод создания новой игры.
        """

        self.__repository.delete(id)
        tictactoe = TicTacToe(id, field_size=field_size, win_line=win_line)
        self.__repository.create(tictactoe)
        return tictactoe


    def get(self, id: int) -> TicTacToe:

        """
        Метод, возвращающий объект игры.
        """

        return self.__repository.read(id)


    def move(self, id: int, index: int) -> tuple[TicTacToe, str]:

        """
        Метод хода игрока.
        """

        tictactoe = self.__repository.read(id)
        if tictactoe is None:
            return None
        result = tictactoe.move(index - 1)
        self.__repository.update(tictactoe)
        return (tictactoe, result)


    def get_sign(self, id: int) -> str:

        """
        Метод, возвращающий символ игрока.
        """

        tictactoe = self.__repository.read(id)
        return None if tictactoe is None else tictactoe.get_sign()


    def delete(self, id: int) -> None:

        """
        Метод удаления игры.
        """

        self.__repository.delete(id)

