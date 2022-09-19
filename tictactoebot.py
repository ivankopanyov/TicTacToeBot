from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot import Bot
from tictactoe import TicTacToe
from tictactoecontroller import TicTacToeController
from userscontroller import UsersController


class TicTacToeBot(Bot):

    """
    Класс, описывающий телеграм-бота для игры в крестики-нолики.
    """

    __tictactoe_controller: TicTacToeController

    """
    Объект контроллера для работы с играми.
    """

    __users_controller: UsersController

    """
    Объект контроллера для работы с пользователями.
    """

    def __init__(self, token: str, tictactoe_controller: TicTacToeController, 
        users_controller: UsersController) -> None:

        """
        Инициализация объекта класс телеграм-бота для игры в крестики-нолики.
        """

        self.__tictactoe_controller = tictactoe_controller
        self.__users_controller = users_controller
        super().__init__(token)

    def _add_handlers(self) -> None:

        """
        Метод добавления обработчиков сообщений.
        """

        self._app.add_handler(MessageHandler(filters.Regex(r'^[' + TicTacToe.NUMBERS + r']{1}$'), self.__move))
        self._app.add_handler(MessageHandler(filters.Regex(r'^Новая игра$'), self.__new))
        self._app.add_handler(CommandHandler('start', self.__start))
        self._app.add_handler(CommandHandler('new', self.__new))
        self._app.add_handler(MessageHandler(filters.ALL, self.__error))

    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды /start
        """

        id = update.effective_user.id

        if not self.__users_controller.check(id):
            message = f'{update.effective_user.first_name}, добро пожаловать! '
            self.__users_controller.add(id)
        else:
            message = f'{update.effective_user.first_name}, с возвращением! '

        result = self.__tictactoe_controller.get(id)
        state = result[1]

        if state == TicTacToe.STOP:
            message += 'Эта игра завершилась! Начните новую игру!'
        else:
            message += f'Сейчас ваш ход! Вы ходите {self.__tictactoe_controller.get_sign(id)}'

        reply_markup = self.__get_keyboard(result[0])
        await update.message.reply_text(message, reply_markup=reply_markup)

    async def __new(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды запуска новой игры.
        """

        id = update.effective_user.id
        field = self.__tictactoe_controller.new(id)
        name = update.effective_user.first_name
        sign = self.__tictactoe_controller.get_sign(id)
        message = f'{self.__get_name(name, "с")}ейчас Ваш ход! Вы ходите {sign}'
        reply_markup = self.__get_keyboard(field)
        await update.message.reply_text(message, reply_markup=reply_markup)

    async def __move(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки хода игрока.
        """

        id = update.effective_user.id
        name = update.effective_chat.first_name
        result = self.__tictactoe_controller.move(id, update.message.text)
        state = result[1]

        if state == TicTacToe.WIN:
            message = f'{self.__get_name(name, "")}Вы победили! Поздравляем! Начните новую игру!'
        elif state == TicTacToe.LOSE:
            message = f'{self.__get_name(name, "к")} сожалению, Вы проиграли! Попробуйте еще раз!'
        elif state == TicTacToe.DRAW:
            message = f'{self.__get_name(name, "")}Вы сыграли в ничью! Попробуйте еще раз!'
        elif state == TicTacToe.STOP:
            message = f'{self.__get_name(name, "э")}та игра завершилась! Начните новую игру!'
        else:
            name = update.effective_user.first_name
            sign = self.__tictactoe_controller.get_sign(id)
            message = f'{self.__get_name(name, "с")}ейчас ваш ход! Вы ходите {sign}'

        reply_markup = self.__get_keyboard(result[0])
        await update.message.reply_text(message, reply_markup=reply_markup)

    async def __error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки исключений.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name

        result = self.__tictactoe_controller.get(id)
        state = result[1]

        message = "Неизвестная команда! "

        if state == TicTacToe.STOP:
            message += f'{self.__get_name(name, "э")}та игра завершилась! Начните новую игру!'
        else:
            message += f'{self.__get_name(name, "с")}ейчас ваш ход! Вы ходите {self.__tictactoe_controller.get_sign(id)}'

        reply_markup = self.__get_keyboard(result[0])
        await update.message.reply_text(message, reply_markup=reply_markup)

    def __get_keyboard(self, field: list[str]) -> ReplyKeyboardMarkup:

        """
        Метод создания клавиатуры.
        """

        step = 3
        keyboard = [field[i:i+step] for i in range(0, len(field), step)]
        keyboard.append(['Новая игра'])
        return ReplyKeyboardMarkup(keyboard)

    def __get_name(self, name: str | None, start: str) -> str:

        """
        Метод добакления имени пользователя в сообщение.
        """

        startLower = "" if start == "" else start.lower()
        startUpper = "" if start == "" else start.upper()
        return f'{name}, {startLower}' if not name is None and len(name) > 0 else startUpper
