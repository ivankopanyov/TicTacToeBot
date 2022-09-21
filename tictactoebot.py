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
    
    NUMBERS = '⁰¹²³⁴⁵⁶⁷⁸⁹'

    """
    Константа, хранящая символы цифр.
    """

    MIN = 3

    """
    Константа, хранящая значение минимального размера поля.
    """

    MAX = 5

    """
    Константа, хранящая значение максимального размера поля.
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

        self._app.add_handler(MessageHandler(filters.Regex(r'^[' + TicTacToeBot.NUMBERS + r']{1,}$'), self.__move))
        self._app.add_handler(MessageHandler(filters.Regex(r'^Новая игра$'), self.__reset))
        self._app.add_handler(MessageHandler(filters.Regex(r'^[345]{1} x [345]{1}$'), self.__new))
        self._app.add_handler(CommandHandler('start', self.__start))
        self._app.add_handler(CommandHandler('new', self.__reset))
        self._app.add_handler(MessageHandler(filters.ALL, self.__error))


    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды /start
        """

        id = update.effective_user.id
        name = update.effective_user.first_name

        if not self.__users_controller.exists(id):
            message = f'{name}, добро пожаловать! '
            self.__users_controller.add(id)
        else:
            message = f'{name}, с возвращением! '

        field = self.__tictactoe_controller.get(id)
        state = None if field == None else field[1]

        if state == None:
            message += f'Выберите размер поля!'
            reply_markup = self.__get_size_keyboard()
        elif state == TicTacToe.STOP:
            message += 'Эта игра завершилась! Начните новую игру!'
            reply_markup = self.__get_keyboard(field[0])
        else:
            message += f'Сейчас ваш ход! Вы ходите {self.__tictactoe_controller.get_sign(id)}!'
            reply_markup = self.__get_keyboard(field[0])
            
        await update.message.reply_text(message, reply_markup=reply_markup)


    async def __reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды запуска новой игры.
        """

        id = update.effective_user.id
        self.__tictactoe_controller.delete(id)
        name = update.effective_user.first_name
        message = f'{self.__get_name(name, "в")}ыберите размер поля!'
        reply_markup = self.__get_size_keyboard()
        await update.message.reply_text(message, reply_markup=reply_markup)


    async def __new(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды выбора размера игрового поля.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name
        nums = list(map(int, update.message.text.split(' x ')))

        if nums[0] != nums[1]:
            message = f'Неизвестная команда! {self.__get_name(name, "в")}ыберите размер поля!'
            reply_markup = self.__get_size_keyboard()
        else:
            field = self.__tictactoe_controller.new(id, nums[0])
            sign = self.__tictactoe_controller.get_sign(id)
            message = f'{self.__get_name(name, "с")}ейчас Ваш ход! Вы ходите {sign}!'
            reply_markup = self.__get_keyboard(field)

        await update.message.reply_text(message, reply_markup=reply_markup)


    async def __move(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки хода игрока.
        """

        id = update.effective_user.id
        name = update.effective_chat.first_name
        field = self.__tictactoe_controller.get(id)

        if field == None:
            message = f'Неизвестная команда! {self.__get_name(name, "в")}ыберите размер поля!'
            reply_markup = self.__get_size_keyboard()
        else:
            result = self.__tictactoe_controller.move(id, self.__mini_int_to_int(update.message.text))
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
                message = f'{self.__get_name(name, "с")}ейчас ваш ход! Вы ходите {sign}!'

            reply_markup = self.__get_keyboard(result[0])

        await update.message.reply_text(message, reply_markup=reply_markup)


    async def __error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки исключений.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name

        field = self.__tictactoe_controller.get(id)
        state = None if field == None else field[1]

        message = "Неизвестная команда! "

        if state == None:
            message = f'Неизвестная команда! {self.__get_name(name, "в")}ыберите размер поля!'
            reply_markup = self.__get_size_keyboard()
        elif state == TicTacToe.STOP:
            message += f'{self.__get_name(name, "э")}та игра завершилась! Начните новую игру!'
            reply_markup = self.__get_keyboard(field[0])
        else:
            message += f'{self.__get_name(name, "с")}ейчас ваш ход! Вы ходите {self.__tictactoe_controller.get_sign(id)}!'
            reply_markup = self.__get_keyboard(field[0])

        reply_markup = self.__get_keyboard(field[0])
        await update.message.reply_text(message, reply_markup=reply_markup)


    def __get_size_keyboard(self) -> ReplyKeyboardMarkup:

        """
        Метод создания клавиатуры выбора игрового поля.
        """

        return ReplyKeyboardMarkup([[f'{i} x {i}' for i in range(TicTacToeBot.MIN, TicTacToeBot.MAX + 1)]], resize_keyboard=True)


    def __get_keyboard(self, field: list[str]) -> ReplyKeyboardMarkup:

        """
        Метод создания клавиатуры.
        """

        step = int(len(field) ** 0.5)
        temp = list(map(lambda i: self.__int_to_mini_int(i + 1) if field[i] == TicTacToe.EMPTY else field[i], range(len(field))))
        keyboard = [temp[i:i+step] for i in range(0, len(temp), step)]
        keyboard.append(['Новая игра'])
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


    def __mini_int_to_int(self, value: str) -> int:

        """
        Метод преобразования строки в числовые символы
        """

        return int(''.join([str(TicTacToeBot.NUMBERS.index(i)) for i in value]))


    def __int_to_mini_int(self, value: int) -> str:

        """
        Метод преобразования числа в строку
        """

        return ''.join([TicTacToeBot.NUMBERS[int(i)] for i in str(value)])


    def __get_name(self, name: str | None, start: str) -> str:

        """
        Метод добакления имени пользователя в сообщение.
        """

        startLower = "" if start == "" else start.lower()
        startUpper = "" if start == "" else start.upper()
        return f'{name}, {startLower}' if not name is None and len(name) > 0 else startUpper
