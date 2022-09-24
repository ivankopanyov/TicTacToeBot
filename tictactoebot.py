from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot import Bot
from user import User
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

        self._app.add_handler(CommandHandler('start', self.__start))

        self._app.add_handler(MessageHandler(filters.Regex(r'^Новая игра$'), self.__new))
        self._app.add_handler(CommandHandler('new', self.__new))

        self._app.add_handler(MessageHandler(filters.Regex(r'^Вернуться к игре$'), self.__back))

        self._app.add_handler(MessageHandler(filters.Regex(r'^Настройки$'), self.__field_size))
        self._app.add_handler(CommandHandler('settings', self.__field_size))
        
        self._app.add_handler(MessageHandler(filters.Regex(r'^[345]{1} x [345]{1}$'), self.__win_line))
        
        self._app.add_handler(MessageHandler(filters.Regex(r'^[345]{1}$'), self.__save_settings))
        
        self._app.add_handler(MessageHandler(filters.Regex(r'^[' + TicTacToeBot.NUMBERS + r']{1,}$'), self.__move))
        
        self._app.add_handler(MessageHandler(filters.ALL, self.__error))


    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды /start
        """

        id = update.effective_user.id
        name = update.effective_user.first_name

        if not self.__users_controller.exists(id):
            message = f'{self.__get_name("Д", name)}обро пожаловать! '
            user = self.__users_controller.add(id)
        else:
            message = f'{self.__get_name("С", name)} возвращением! '
            self.__users_controller.set_menu_id(id, 0)
            user = self.__users_controller.get(id)

        tictactoe = self.__tictactoe_controller.get(id)
        if tictactoe is None:
            tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())

        mes, keyboard = self.__game_menu(tictactoe, None)

        await update.message.reply_text(message + mes, reply_markup=keyboard)


    async def __new(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды создания новой игры.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)

        self.__tictactoe_controller.delete(id)
        tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())

        self.__users_controller.set_menu_id(id, 0)

        message, keyboard = self.__game_menu(tictactoe, name)

        await update.message.reply_text(message, reply_markup=keyboard)


    async def __back(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды возврата к игре.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)

        tictactoe = self.__tictactoe_controller.get(id)
        if tictactoe is None:
            tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())
        message, keyboard = self.__game_menu(tictactoe, name)

        self.__users_controller.set_menu_id(id, 0)

        await update.message.reply_text(message, reply_markup=keyboard)

    
    async def __field_size(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды изменения размера игрового поля.
        """
        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)
        message, keyboard = self.__field_size_menu(name)

        self.__users_controller.set_menu_id(id, 1)

        await update.message.reply_text(message, reply_markup=keyboard)


    async def __win_line(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки команды изменения колличества клеток для победы.
        """
        
        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)
        nums = list(map(int, update.message.text.split(' x ')))

        if nums[0] != nums[1]:
            message = 'Неизвестная команда! '
            mes, keyboard = self.__field_size_menu(name)
            message += mes
        else:
            self.__users_controller.set_field_size(id, nums[0])

            win_line = user.get_win_line()

            if win_line > nums[0]:
                self.__users_controller.set_win_line(id, nums[0])
                win_line = nums[0]

            message = f"Настройки сохранены!\nРазмер игрового поля: {nums[0]} x {nums[0]}\nКолличество клеток для победы: {win_line}\n\n"

            if nums[0] == 3:
                tictactoe = self.__tictactoe_controller.get(id)
                if tictactoe is None:
                    tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())
                mes, keyboard = self.__game_menu(tictactoe, name)
            else:
                mes, keyboard = self.__win_line_menu(name, nums[0])
                self.__users_controller.set_menu_id(id, 2)

            message += mes

        await update.message.reply_text(message, reply_markup=keyboard)

    
    async def __save_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод возврата к текущей игре.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)
        num = int(update.message.text)
        size = user.get_field_size()

        if user.get_menu_id() != 2:
            message, keyboard = self.__error_handle(user, name)
        elif num > size:
            message = 'Неизвестная команда! '
            mes, keyboard = self.__win_line_menu(name, size)
            message += mes
        else:
            self.__users_controller.set_win_line(id, num)
            message = f"Настройки сохранены!\nРазмер игрового поля: {size} x {size}\nКолличество клеток для победы: {num}\n\n"
            tictactoe = self.__tictactoe_controller.get(id)
            if tictactoe is None:
                tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())
            self.__users_controller.set_menu_id(id, 0)
            mes, keyboard = self.__game_menu(tictactoe, name)
            message += mes

        await update.message.reply_text(message, reply_markup=keyboard)


    async def __move(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки хода игрока.
        """

        id = update.effective_user.id
        name = update.effective_chat.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)

        if user.get_menu_id() != 0:
            message, keyboard = self.__error_handle(user, name)
        else:

            result = self.__tictactoe_controller.move(id, self.__mini_int_to_int(update.message.text))
            if result is None:
                tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())
                state = TicTacToe.NONE
            else:
                tictactoe, state = result

            if state == TicTacToe.WIN:
                message = f'{self.__get_name("", name)}Вы победили! Поздравляем! Начните новую игру!'
            elif state == TicTacToe.LOSE:
                message = f'{self.__get_name("к", name)} сожалению, Вы проиграли! Попробуйте еще раз!'
            elif state == TicTacToe.DRAW:
                message = f'{self.__get_name("", name)}Вы сыграли в ничью! Попробуйте еще раз!'
            elif state == TicTacToe.STOP:
                message = f'{self.__get_name("э", name)}та игра завершилась! Начните новую игру!'
            else:
                name = update.effective_user.first_name
                sign = self.__tictactoe_controller.get_sign(id)
                message = f'{self.__get_name("с", name)}ейчас ваш ход! Вы ходите {sign}!'

            keyboard = self.__get_keyboard_game(tictactoe.get_field())

        await update.message.reply_text(message, reply_markup=keyboard)


    async def __error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """
        Метод обработки исключений.
        """

        id = update.effective_user.id
        name = update.effective_user.first_name
        user = self.__users_controller.get(id)
        if user == None:
            user = self.__users_controller.add(id)
        message, keyboard = self.__error_handle(user, name)
        await update.message.reply_text(message, reply_markup=keyboard)

    
    def __game_menu(self, tictactoe: TicTacToe, name: str) -> tuple[str, ReplyKeyboardMarkup]:

        """
        Метод, возвращающий игровое меню.
        """

        if tictactoe.is_active():
            message = f'{self.__get_name("С", name)}ейчас Ваш ход! Вы ходите {tictactoe.get_sign()}! Колличество клеток для победы:  {tictactoe.get_win_line()}'
        else:
            message = f'{self.__get_name("э", name)}та игра завершилась! Начните новую игру!'
        return(message, self.__get_keyboard_game(tictactoe.get_field()))


    def __field_size_menu(self, name: str) -> tuple[str, ReplyKeyboardMarkup]:

        """
        Метод, возвращающий меню для выбора размера игрового поля.
        """

        message = f'{self.__get_name("В", name)}ыберите размер игрового поля!'
        keyboard = ReplyKeyboardMarkup([['3 x 3', '4 x 4', '5 x 5'], ['Вернуться к игре']], resize_keyboard=True)
        return(message, keyboard)
        

    def __win_line_menu(self, name: str, field_size: int) -> tuple[str, ReplyKeyboardMarkup]:

        """
        Метод, возвращающий меню для выбора колличества клеток для победы.
        """

        message = f'{self.__get_name("В", name)}ыберите колличество клеток для победы!'
        
        keyboard = ReplyKeyboardMarkup([list(map(str, [i for i in range(3, field_size + 1)])), ['Вернуться к игре']], resize_keyboard=True)
        return(message, keyboard)

    
    def __error_handle(self, user: User, name: str) -> tuple[str, ReplyKeyboardMarkup]:

        """
        Метод обработки неизвестных команд.
        """

        id = user.get_id()
        message = "Неизвестная команда! "
        menu_id = user.get_menu_id()

        if menu_id == 0:
            tictactoe = self.__tictactoe_controller.get(id)
            if tictactoe is None:
                tictactoe = self.__tictactoe_controller.new(id, user.get_field_size(), user.get_win_line())
            mes, keyboard = self.__game_menu(tictactoe, name)
        elif menu_id == 1:
            mes, keyboard = self.__field_size_menu(name)
        else:
            mes, keyboard = self.__win_line_menu(name)

        message += mes

        return(message, keyboard)


    def __get_keyboard_game(self, field: list[str]) -> ReplyKeyboardMarkup:

        """
        Метод, возвращающий клавиатуру для игры.
        """

        step = int(len(field) ** 0.5)
        temp = list(map(lambda i: self.__int_to_mini_int(i + 1) if field[i] == TicTacToe.EMPTY else field[i], range(len(field))))
        keyboard = [temp[i:i+step] for i in range(0, len(temp), step)]
        keyboard.append(['Новая игра', 'Настройки'])
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


    def __get_name(self, first_symbol: str, name: str = None) -> str:

        """
        Метод добакления имени пользователя в сообщение.
        """

        symbol_lower = "" if first_symbol == "" else first_symbol.lower()
        symbol_upper = "" if first_symbol == "" else first_symbol.upper()
        return f'{name}, {symbol_lower}' if not name is None and len(name) > 0 else symbol_upper