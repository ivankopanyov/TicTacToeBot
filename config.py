from os.path import exists


class Config:

    """
    Класс, описывающий конфигурации приложения.
    """

    __FILE_NAME: str = 'bot.conf'

    """
    Имя файла с конфигурациями.
    """

    __token: str | None = None

    """
    Токен для подключения к телеграмм-боту.
    """

    def token() -> str | None:

        """
        Метод, возвращающий токен для подключения к телеграмм-боту.
        """

        if Config.__token != None:
            return Config.__token

        if not exists(Config.__FILE_NAME):
            return None

        with open(Config.__FILE_NAME, 'r', encoding='utf8') as file:
            for line in file:
                if line.find('token') == 0:
                    result = line.split('=')[1].strip()
                    if result == '':
                        return None
                    Config.__token = result
                    return Config.__token
        
        return None
