class WindowConstants:
    """Настройки окна"""
    width = 1400
    height = 800
    title = 'Змейка'
    bg_color = (173, 218, 183)


class SnakeConstants:
    """Базовые параметры змейки"""
    size = 40
    speed = 4
    vector = (0, 0)
    start_position = (140, 140)
    color = (5, 100, 5)


class LevelConstants:
    """Базовые параметры уровня"""
    campaign_path = 'maps/campaign/'
    user_path = 'maps/user/'
    width = 800
    height = 800
    cell = 40
    csv_resolution = 20
    walls_color = (30, 30, 30)
    food_size = 20


class Commands:
    command = None


class Constants:
    window = WindowConstants()
    snake = SnakeConstants()
    level = LevelConstants()
    commands = Commands()
