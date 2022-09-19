from abc import ABC, abstractmethod

from telegram.ext import Application, ApplicationBuilder


class Bot(ABC):

    """
    Абстрактный класс, описывающий телеграм-бота.
    """
    
    _app: Application

    """
    Объект класса точки входа в приложение для работы с телеграм-ботом.
    """

    def __init__(self, token: str) -> None:

        """
        Инициализация объекта класса телеграм-бота.
        """

        self._app = ApplicationBuilder().token(token).build()
        self._add_handlers()

    @abstractmethod
    def _add_handlers(self) -> None:

        """
        Абстрактный метод добавления обработчиков сообщений.
        """

        pass
    
    def start(self) -> None:

        """
        Метод запуска телеграм-бота.
        """

        self._app.run_polling()