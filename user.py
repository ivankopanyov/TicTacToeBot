class User:

    """
    Класс, описывающий пользователя.
    """

    __id: int
    
    """
    Идентификатор пользователя
    """

    __menu_id: int

    """
    Номер текущего состояния экрана.
    """

    __field_size: int

    """
    Размер игрового поля.
    """

    __win_line: int

    """
    Колличество клеток для победы.
    """

    def __init__(self, id: int, menu_id: int, field_size: int, win_line: int) -> None:

        """
        Инициализация объекта пользователя.
        На вход принимает идентификатор пользователя.
        """

        self.__id = id
        self.__menu_id = menu_id
        self.__field_size = field_size
        self.__win_line = win_line


    def get_id(self) -> int:

        """
        Метод, возвращающий идентификатор пользователя.
        """

        return self.__id


    def get_menu_id(self) -> int:

        """
        Метод, возвращающий номер текущего состояния экрана пользователя.
        """

        return self.__menu_id
        

    def get_field_size(self) -> int:

        """
        Метод, возвращающий размер игрового поля по умолчанию.
        """

        return self.__field_size
        

    def get_win_line(self) -> int:

        """
        Метод, возвращающий колличество клеток для победы по умолчанию.
        """

        return self.__win_line