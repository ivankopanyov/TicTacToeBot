from os import getenv

from dotenv import load_dotenv, set_key
from telegram.error import InvalidToken

from db import DataBase
from tictactoebot import TicTacToeBot
from tictactoecontroller import TicTacToeController
from tictactoerepository import TicTacToeRepository
from userscontroller import UsersController
from usersrepository import UsersRepository


def main() -> None:

    """
    Точка входа в приложение.
    """
    
    load_dotenv()
    token = getenv('TOKEN')

    if token == None:
        token = input("Укажите токен телеграм-бота: ")
        set_key('.env', 'TOKEN', token)

    db = DataBase('tictactoe.db')

    tictactoe_repository = TicTacToeRepository(db)
    tictactoe_controller = TicTacToeController(tictactoe_repository)

    users_repository = UsersRepository(db)
    users_controller = UsersController(users_repository)

    try:
        bot = TicTacToeBot(token, tictactoe_controller, users_controller)
        bot.start()
    except InvalidToken:
        print("Неверный токен!")

    print("Завершение работы приложения...")


if __name__ == "__main__":
    main()