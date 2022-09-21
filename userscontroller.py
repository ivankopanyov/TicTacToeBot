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

    def add(self, id: int) -> None:

        """
        Метод добавления пользователя в базу данных.
        """

        user = User(id)
        self.__repository.create(user)

    def exists(self, id: int) -> bool:

        """
        Метод проверки наличия пользователя в базе данных.
        """

        return self.__repository.exists(id)