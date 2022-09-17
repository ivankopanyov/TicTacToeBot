from db import DataBase
from tictactoerepository import TicTacToeRepository
from usersrepository import UsersRepository
from tictactoecontroller import TicTacToeController
from userscontroller import UsersController
from tictactoebot import TicTacToeBot
from telegram.error import InvalidToken
from config import Config

def main() -> None:

    """
    Точка входа в приложение.
    """

    if Config.token() == None:
        print("Укажите токен телеграм-бота в файле 'bot.conf'")
        print("Завершение работы приложения...")
        return

    db = DataBase('tictactoe.db')
    cursor = db.connect()

    tictactoe_repository = TicTacToeRepository(cursor, 'tictactoe', ['id', 'field', 'sign'])
    tictactoe_controller = TicTacToeController(tictactoe_repository)

    users_repository = UsersRepository(cursor, 'users', ['id'])
    users_controller = UsersController(users_repository)

    try:
        bot = TicTacToeBot(Config.token(), tictactoe_controller, users_controller)
        bot.start()
    except InvalidToken:
        print("Неверный токен!")

    print("Завершение работы приложения...")

if __name__ == "__main__":
    main()