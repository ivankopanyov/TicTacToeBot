from random import randint

class TicTacToe:
    
    """
    Класс, описывающий игру в крестики-нолики.
    """

    CROSS = '❌'

    """
    Константа, хранящая символ крестика.
    """

    ZERO = '🟢'

    """
    Константа, хранящая символ нолика.
    """

    NUMBERS = '¹²³⁴⁵⁶⁷⁸⁹'

    """
    Константа, хранящая строку с номерами клеток.
    """

    LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    """
    Список, хранящий линии для проверки окончания игры.
    """

    WIN = 'win'

    """
    Победа игрока.
    """

    LOSE = 'lose'

    """
    Поражение игрока.
    """

    STOP = 'stop'

    """
    Игра закончена.
    """

    DRAW = 'draw'

    """
    Ничья.
    """

    NONE = 'none'

    """
    Игра продолжается.
    """

    __id: str

    """
    Идентификатор игры.
    """

    __field: list[str]

    """
    Список, хранящий значения клеток игрового поля.
    """

    __sign: str

    """
    Символ игрока.
    """

    def __init__(self, id: str, field: list[str] | None = None, sign: str | None = None) -> None:

        """
        Инициализация объекта класса игры.
        """

        self.__id = id
        self.__field = field if not field is None else list(TicTacToe.NUMBERS)
        
        if sign is None:
            self.__sign = TicTacToe.CROSS if randint(0, 1) == 1 else TicTacToe.ZERO
            if self.__sign == TicTacToe.ZERO:
                self.__bot_move()
        else:
            self.__sign = sign

    def get_id(self) -> str:

        """
        Метод, возвращающий идентификатор игры.
        """

        return self.__id

    def get_field(self) -> list[str]:

        """
        Метод, возвращающий игровое поле.
        """

        return self.__field.copy()

    def get_state(self) -> str:

        """
        Метод, возвращающий состояние игры.
        """

        result = self.__check()
        return TicTacToe.STOP if result != TicTacToe.NONE else TicTacToe.NONE

    def get_sign(self) -> str:

        """
        Метод, возвращающий символ игрока.
        """

        return self.__sign

    def move(self, index: int) -> tuple([list[str], str]):

        """
        Метод хода игрока.
        """

        result = self.__check()
        if result != TicTacToe.NONE:
            return (self.__field, TicTacToe.STOP)

        if self.__field[index] == TicTacToe.CROSS or self.__field[index] == TicTacToe.ZERO:
            return (self.__field, TicTacToe.NONE)

        self.__field[index] = self.__sign
        result = self.__check()
        if result == TicTacToe.DRAW:
            return (self.__field, result)
        elif result == TicTacToe.STOP:
            return (self.__field, TicTacToe.WIN)

        self.__bot_move()
        result = self.__check()
        if result == TicTacToe.DRAW:
            return (self.__field, result)
        elif result == TicTacToe.STOP:
            return (self.__field, TicTacToe.LOSE)

        return (self.__field, TicTacToe.NONE)

    def __bot_move(self) -> None:

        """
        Метод хода бота.
        """

        bot_sign = TicTacToe.CROSS if self.__sign != TicTacToe.CROSS else TicTacToe.ZERO
        moves = [(self.__sign, 2), (bot_sign, 2), (self.__sign, 1), (bot_sign, 1)]
        for move in moves:
            result = self.__find_cell(move[0], move[1])
            if result != None:
                self.__field[result] = bot_sign
                return

        self.__field[randint(0, len(self.__field) - 1)] = bot_sign

    def __find_cell(self, sign, sign_count) -> int:

        """
        Поиск наилучшего хода для бота.
        """

        empties = []
        for line in TicTacToe.LINES:
            counter = 0
            temp_empties = []
            for i in line:
                if self.__field[i] != TicTacToe.CROSS and self.__field[i] != TicTacToe.ZERO:
                    temp_empties.append(i)
                if self.__field[i] == sign:
                    counter += 1
            if counter >= sign_count and temp_empties != None:
                empties += temp_empties
        return None if len(empties) == 0 else empties[randint(0, len(empties) - 1)]

    def __check(self) -> str:

        """
        Метод проверки текущего состояния игры.
        """

        for line in TicTacToe.LINES:
            if len(set([self.__field[i] for i in line])) == 1:
                return TicTacToe.STOP

        if len(set(self.__field)) == 2:
            return TicTacToe.DRAW

        return TicTacToe.NONE