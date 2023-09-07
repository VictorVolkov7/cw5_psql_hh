from configparser import ConfigParser


def config(path, section="postgresql"):
    """
    Получение словаря с данными для подключения к БД
    :param path: путь к файлу с данными для подключения к БД
    :param section: раздел, откуда берутся параметры для подключения к БД
    :return: словарь с данными для подключения к БД
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(path)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, path))
    return db
