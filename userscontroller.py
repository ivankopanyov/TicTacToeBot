from user import User
from usersrepository import UsersRepository


class UsersController():

    """
    Класс, описывающий контроллер для работы с объектами пользователей.
    """

    __repository: UsersRepository

    """
    Объект репозитория пользователей.
    """

    def __init__(self, repository: UsersRepository) -> None:

        """
        Инициализация объекта класс репозитория пользователей.
        """

        self.__repository = repository


    def add(self, id: int, menu_id: int = 0, field_size: int = 3, win_line: int = 3) -> User:

        """
        Метод добавления пользователя в базу данных.
        """

        user = User(id, menu_id, field_size, win_line)
        self.__repository.create(user)
        return user

    
    def get(self, id: int) -> User:

        """
        Метод получения объекта пользователя из базы данных.
        """

        return self.__repository.read(id)

    
    def set_menu_id(self, id: int, menu_id: int) -> None:

        """
        Метод обновления значения номера текущего экрана пользователя.
        """

        user = self.__repository.read(id)
        self.__repository.update(User(id, menu_id, user.get_field_size(), user.get_win_line()))

    
    def set_field_size(self, id: int, field_size: int) -> None:

        """
        Метод обновления значения размера игрового поля.
        """

        user = self.__repository.read(id)
        self.__repository.update(User(id, user.get_menu_id(), field_size, user.get_win_line()))

    
    def set_win_line(self, id: int, win_line: int) -> None:

        """
        Метод обновления значения колличества клеток для победы.
        """

        user = self.__repository.read(id)
        self.__repository.update(User(id, user.get_menu_id(), user.get_field_size(), win_line))


    def exists(self, id: int) -> bool:

        """
        Метод проверки наличия пользователя в базе данных.
        """

        return self.__repository.exists(id)