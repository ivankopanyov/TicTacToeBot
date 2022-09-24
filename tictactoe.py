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

    EMPTY = ' '

    """
    Константа, хранящая символ пустой клетки.
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

    __id: int

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

    __field_size: int

    """
    Длина стороны игрового поля
    """

    __lines: list[list[int]]

    """
    Список, хранящий линии для проверки окончания игры.
    """

    __win_line: int

    """
    Колличество клеток для победы.
    """

    def __init__(self, 
                id: int, 
                field: list[str] = None, 
                sign: str = None, 
                field_size: int = 3, 
                win_line: int = 3) -> None:

        """
        Инициализация объекта класса игры.
        """

        self.__id = id
        self.__field = field if not field is None else [TicTacToe.EMPTY] * field_size * field_size
        self.__field_size = int(len(self.__field) ** 0.5)

        self.__win_line = win_line
        
        self.__lines = []

        for i in range(0, len(self.__field), self.__field_size):
            self.__lines.append(list(range(i, i + self.__field_size)))

        for i in range(0, self.__field_size):
            self.__lines.append(list(range(i, len(self.__field), self.__field_size)))

        starts = [i for i in range(self.__field_size - self.__win_line + 1)]
        for i in range(len(starts)):
            self.__lines.append([j for j in range(starts[i], len(self.__field), self.__field_size + 1)][0:self.__field_size - i])
            
        starts = [i for i in list(range(self.__field_size, len(self.__field), self.__field_size))[0:self.__field_size - self.__win_line]]
        for i in range(len(starts)):
            self.__lines.append([j for j in range(starts[i], len(self.__field), self.__field_size + 1)][0:self.__field_size - i])
            
        starts = [i for i in range(self.__win_line - 1, self.__field_size)]
        for i in range(len(starts)):
            self.__lines.append([j for j in range(starts[i], len(self.__field), self.__field_size - 1)][0:self.__field_size + i - (self.__field_size - self.__win_line)])

        starts = [i for i in list(range(self.__field_size - 1, len(self.__field), self.__field_size))[1:self.__field_size - (self.__win_line - 1)]]
        for i in range(len(starts)):
            self.__lines.append([j for j in range(starts[i], len(self.__field), self.__field_size - 1)][0:self.__field_size - i])
            
        
        if sign is None:
            self.__sign = TicTacToe.CROSS if randint(0, 1) == 1 else TicTacToe.ZERO
            if self.__sign == TicTacToe.ZERO:
                self.__bot_move()
        else:
            self.__sign = sign


    def get_id(self) -> int:

        """
        Метод, возвращающий идентификатор игры.
        """

        return self.__id


    def get_field(self) -> list[str]:

        """
        Метод, возвращающий игровое поле.
        """

        return self.__field.copy()


    def is_active(self) -> bool:

        """
        Проверка состояния игры. Возвращает False, если игра завершена.
        """

        return self.__check() == TicTacToe.NONE


    def get_sign(self) -> str:

        """
        Метод, возвращающий символ игрока.
        """

        return self.__sign

    def get_win_line(self) -> int:

        """
        Метод, возвращающий колличество клеток для победы.
        """

        return self.__win_line
        

    def move(self, index: int) -> str:

        """
        Метод хода игрока.
        """

        result = self.__check()
        if result != TicTacToe.NONE:
            return TicTacToe.STOP

        if not index in range(len(self.__field)) or self.__field[index] != TicTacToe.EMPTY:
            return TicTacToe.NONE

        self.__field[index] = self.__sign
        result = self.__check()
        if result == TicTacToe.DRAW:
            return result
        elif result == TicTacToe.STOP:
            return TicTacToe.WIN

        self.__bot_move()
        result = self.__check()
        if result == TicTacToe.DRAW:
            return (self.__field, result)
        elif result == TicTacToe.STOP:
            return TicTacToe.LOSE

        return TicTacToe.NONE


    def __bot_move(self) -> None:

        """
        Метод хода бота.
        """

        bot_sign = TicTacToe.CROSS if self.__sign != TicTacToe.CROSS else TicTacToe.ZERO

        moves = []
        for i in range(1, self.__win_line):
            moves.insert(0, (self.__sign, i))
            moves.insert(0, (bot_sign, i))

        for move in moves:
            result = self.__find_cell(move[0], move[1])
            if len(result) != 0:
                self.__field[result[randint(0, len(result) - 1)]] = bot_sign
                return

        while True:
            num = randint(0, len(self.__field) - 1)
            if self.__field[num] == TicTacToe.EMPTY:
                self.__field[num] = bot_sign
                return


    def __find_cell(self, sign: str, sign_count: int) -> list[int]:

        """
        Поиск наилучшего хода для бота.
        """

        other = TicTacToe.CROSS if sign == TicTacToe.ZERO else TicTacToe.ZERO

        empties = []
        for line in self.__lines:
            for i in range(len(line) - (self.__win_line - 1)):
                cells = line[i:i+3]
                temp = list(map(lambda j: self.__field[j], cells))
                if not other in temp and len(list(filter(lambda k: k == sign, temp))) == sign_count:
                    empties += list(filter(lambda l: self.__field[l] == TicTacToe.EMPTY, cells))

        return empties


    def __check(self) -> str:

        """
        Метод проверки текущего состояния игры.
        """
        
        for line in self.__lines:
            for i in range(len(line) - (self.__win_line - 1)):
                temp = list(set(map(lambda j: self.__field[j], line[i:i+self.__win_line])))
                if len(temp) == 1 and temp[0] != TicTacToe.EMPTY:
                    return TicTacToe.STOP

        temp = list(set(self.__field))
        if len(temp) == 2 and not TicTacToe.EMPTY in temp:
            return TicTacToe.DRAW

        return TicTacToe.NONE