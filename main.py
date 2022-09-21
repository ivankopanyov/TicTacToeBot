from os import getenv

from dotenv import load_dotenv
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
    TOKEN = getenv('TOKEN')

    if TOKEN == None:
        print("Укажите токен телеграм-бота в файле '.env'")
        print("Завершение работы приложения...")
        return

    db = DataBase('tictactoe.db')
    cursor = db.connect()

    tictactoe_repository = TicTacToeRepository(cursor)
    tictactoe_controller = TicTacToeController(tictactoe_repository)

    users_repository = UsersRepository(cursor)
    users_controller = UsersController(users_repository)

    try:
        bot = TicTacToeBot(TOKEN, tictactoe_controller, users_controller)
        bot.start()
    except InvalidToken:
        print("Неверный токен!")

    print("Завершение работы приложения...")

if __name__ == "__main__":
    main()