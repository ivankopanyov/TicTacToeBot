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

    def add(self, id: str) -> None:

        """
        Метод добавления пользователя в базу данных.
        """

        user = User(id)
        self.__repository.create(user)

    def check(self, id: str) -> bool:

        """
        Метод проверки наличия пользователя в базе данных.
        """

        return not self.__repository.read(id) is None