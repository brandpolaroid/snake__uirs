from random import choice, randint
import csv
import maps
from pathlib import Path


class Game:
    """Класс Game описывает все, что касается игрового процесса.
    Все взаимодействие с игровыми объектами во время игрового процесса происходит
    непосредственно через взаимодействие с экземпляром этого класса.
    Экземпляр каждый раз заново создается для каждого нового уровня, а также
    при рестарте. Содержит в себе объекты классов Snake и Level"""

    def __init__(self, snake, level):
        self.snake = snake
        self.level = level
        self.active = True
        self.status = None
        self.score = 0

    def update(self):

        """Обновляет состояние всех игровых объектов, требующих обновления"""

        if self.active:
            self.snake.update()
            self.collide_wall()
            self.collide_food()
            self.collide_snake()

    def collide_wall(self):

        """Обрабатывает коллизию змейки со стеной"""

        if any(self.level.full_map[dot[1]][dot[0]] == 0 for dot in self.snake.get_peaks()):
            self.snake.kill()
            self.status = False
            self.active = False

    def collide_snake(self):

        """Обрабатывает коллизию змейки с самой собой"""

        if any(self.snake.collide_function(x, y) for x, y in self.snake.previous_positions[:-2]):
            self.snake.kill()
            self.status = False
            self.active = False

    def collide_food(self):

        """Обрабатывает коллизию змейки и еды"""

        if any(self.snake.collide_function(x, y) for x, y in self.level.food.trigger_coords):
            self.new_score()

    def change_direction(self, new_direction: tuple):

        """Метод вызывается при попытке игроком поменять направление движения змейки.
        Если такое направление возможно, то оно добавляется в общий список команд для змейки"""

        if abs(new_direction[0]) != abs(self.snake.vectors[-1][0]) or \
                abs(new_direction[1]) != abs(self.snake.vectors[-1][1]):
            if len(self.snake.vectors) < 3:
                self.snake.change_vector(new_direction)

    def pause(self):

        """Метод останавливает обновление игры, ставя ее на паузу."""

        self.active = not self.active

    def new_score(self):

        """Метод увеличивает счёт, а также длину змейки на 1, при этом меняя текущий статус игры,
        если счёт уровня достиг цели уровня."""

        self.score += 1
        self.snake.length += 1
        if self.score == self.level.level_task:
            self.status = True
            self.active = False
        else:
            self.level.generate_food()

    def click(self, x, y):
        pass


class Food:
    """Класс описывает основные параметры для еды, появляющейся на уровне"""

    def __init__(self, coords: tuple, trigger_coords: tuple, color: tuple):
        self.coords = coords
        self.trigger_coords = trigger_coords
        self.color = color


class Snake:
    """Класс описывает поведение змейки на уровне, а также позволяет взаимодействовать с самой змейкой.
    С ним напрямую работает только экземпляр класса Game."""

    def __init__(self, const, start_position):
        self.coords = list(start_position)
        self.peak_coords = [(), ()]
        self.vectors = [const.vector]
        self.end_vector = const.vector
        self.size = const.size
        self.color = const.color
        self.speed = const.speed
        self.length = 1
        self.previous_positions = []

    def change_vector(self, new_vector):

        """Метод добавляет новый вектор движения в список векторов движения"""

        self.vectors.append(new_vector)

    def update(self):

        """Метод, который вызывается постоянно при обновлении состояния змейки.
        В нем описаны законы ее перемещения и роста"""

        if (self.coords[0] - self.size // 2) % self.size == 0 and (self.coords[1] - self.size // 2) % self.size == 0:
            if self.length > 1:
                self.previous_positions.append(self.coords[:])
                self.previous_positions = self.previous_positions[-self.length:]
                if len(self.previous_positions) > 1:
                    self.end_vector = ((self.previous_positions[1][0] - self.previous_positions[0][0]) // self.size,
                                       (self.previous_positions[1][1] - self.previous_positions[0][1]) // self.size)

            if len(self.vectors) > 1:
                self.vectors = self.vectors[1:]

        self.coords[0] += self.vectors[0][0] * self.speed
        self.coords[1] += self.vectors[0][1] * self.speed
        self.peak_coords = [(self.coords[0] + self.size // 2 - 1, self.coords[1] + self.size // 2 - 1),
                            (self.coords[0] - self.size // 2 + 1, self.coords[1] + self.size // 2 - 1),
                            (self.coords[0] + self.size // 2 - 1, self.coords[1] - self.size // 2 + 1),
                            (self.coords[0] - self.size // 2 + 1, self.coords[1] - self.size // 2 + 1)]

        if len(self.previous_positions) > 1:
            self.previous_positions[0][0] += self.end_vector[0] * self.speed
            self.previous_positions[0][1] += self.end_vector[1] * self.speed

    def get_info(self):

        """Метод возвращает информацию о текущем положении змейки, ее размере и цвете"""

        return *self.coords, self.size, self.size, self.color

    def get_peaks(self):

        """Метод возвращает список координат углов змейки"""

        return self.peak_coords

    def kill(self):

        """Метод останавливает змейку, задавая ей нулевой вектор для перемещения"""

        self.vectors = [(0, 0)]

    def collide_function(self, x, y):

        """Метод вызывается для проверки коллизии с равным или меньшим по размеру объектом, принимает
        координаты объекта"""

        return self.coords[0] - self.size // 2 - 1 <= x <= self.coords[0] + self.size // 2 + 1 and \
            self.coords[1] - self.size // 2 - 1 <= y <= self.coords[1] + self.size // 2 + 1


class Loader:
    """Класс описывает объект загрузчика, основные функции которого: генерировать карты уровня,
    считывая информацию с .csv-файла; создавать объект класса Game для запуска новой игры"""

    def __init__(self, const):
        self.is_campaign = True
        self.path = const.level.campaign_path
        self.max_level = maps.CAMPAIGN_COUNT
        self.level_width = const.level.width
        self.level_height = const.level.height
        self.csv_resolution = const.level.csv_resolution
        self.cell = const.level.cell
        self.const_level = const.level
        self.const = const
        self.current_level = 1

    def change_to_user_maps(self, level):
        self.is_campaign = False
        self.path = self.const.level.user_path
        self.max_level = maps.get_user_amount()
        self.current_level = level

    def change_to_campaign_maps(self):
        self.is_campaign = True
        self.path = self.const.level.campaign_path
        self.max_level = maps.CAMPAIGN_COUNT
        self.current_level = 1

    def load_level(self, level_number):

        """Метод считывает .csv-файл с уровнем, после чего генерирует полную карту
        и уменьшенную ее модель. Возвращает объект типа Level"""
        path = Path(self.path)
        level_path = list(path.iterdir())[level_number - 1]
        with open(level_path, 'r') as file:
            data = [line.split(';') for table in csv.reader(file) for line in table][::-1]
        model_map = data[1:]
        level_task = int(data[0][0])
        full_map = [[1 for _ in range(self.level_width)] for _ in range(self.level_height)]
        for line in range(self.level_height):
            for pixel in range(self.level_width):
                full_map[line][pixel] = int(model_map[line // (self.level_height // self.csv_resolution)][
                                                pixel // (self.level_width // self.csv_resolution)])
        place_for_food = []
        snake_start_position = None
        for line in range(self.csv_resolution):
            for dot in range(self.csv_resolution):
                if int(model_map[line][dot]) == 1:
                    place_for_food.append((
                        dot * self.cell + self.cell // 2,
                        line * self.cell + self.cell // 2
                    ))
                if int(model_map[line][dot]) == 2:
                    snake_start_position = [dot * self.cell + self.cell // 2,
                                            line * self.cell + self.cell // 2]
        level = Level(model_map,
                      full_map,
                      place_for_food,
                      self.const_level,
                      level_task,
                      level_number,
                      snake_start_position)
        return level

    def load_game(self, is_next):

        """Метод генерирует новый объект класса Game и возвращает его. Если закончили уровни, то возвращает None."""

        if is_next:
            self.current_level += 1
        if self.current_level > self.max_level:
            return None
        level = self.load_level(self.current_level)
        snake = Snake(self.const.snake, level.snake_start_pos)
        game = Game(snake, level)
        return game

    def load_editor(self):
        editor = MapEditor(self.const_level)
        return editor

    # def set_mode(self, is_campaign):
    #     if is_campaign:
    #         self.is_campaign = is_campaign
    #         self.path = self.const.level.campaign_path
    #         self.max_level = maps.CAMPAIGN_COUNT
    #     else:
    #         self.is_campaign = is_campaign
    #         self.path = self.const.level.user_path
    #         self.max_level = maps.get_user_amount()


class MapEditor:
    def __init__(self, const):
        self.snake_position = None
        self.active_element = 'W'
        self.walls_position = []
        # self.template = []
        self.const = const
        self.path = const.user_path

    def change_active(self, new_active):
        self.active_element = new_active[0]

    def make_template(self):
        for line in range(self.const.csv_resolution):
            for dot in range(self.const.csv_resolution):
                if dot == 0 or line == 0 or \
                        dot == self.const.csv_resolution - 1 or \
                        line == self.const.csv_resolution - 1:
                    self.walls_position.append((dot, line))

    def get_all_data(self):
        return self.snake_position, self.walls_position, self.active_element

    def click(self, x, y):
        if x > self.const.width or y > self.const.height:
            return
        x = x // self.const.cell
        y = y // self.const.cell
        if (x % (self.const.csv_resolution - 1)) * (y % (self.const.csv_resolution - 1)) == 0:
            return
        if (x, y) == self.snake_position:
            if self.active_element == 'W':
                pass
            elif self.active_element == 'S':
                self.delete_snake()
        elif (x, y) in self.walls_position and self.active_element != 'S':
            self.remove_wall((x, y))
        elif (x, y) not in self.walls_position:
            if self.active_element == 'W':
                self.add_wall((x, y))
            elif self.active_element == 'S':
                self.new_snake_position((x, y))

    def new_snake_position(self, position: tuple):
        self.snake_position = position

    def delete_snake(self):
        self.snake_position = None

    def add_wall(self, position: tuple):
        self.walls_position.append(position)

    def remove_wall(self, position: tuple):
        self.walls_position.remove(position)

    def save_level(self, name, task):
        with open(f'{self.path}{name}.csv', 'w+', newline='') as level_file:
            level_writer = csv.writer(level_file, delimiter=';', dialect='excel')
            for i_line in range(self.const.csv_resolution - 1, -1, -1):
                row = []
                for i_dot in range(self.const.csv_resolution):
                    current_position = (i_dot, i_line)
                    if self.snake_position == current_position:
                        row.append('2')
                    elif current_position in self.walls_position:
                        row.append('0')
                    else:
                        row.append('1')
                level_writer.writerow(''.join(row))
            level_writer.writerow([f'{task}'])


class Level:
    """Класс описывает все параметры уровня, а также содержит в себе экземпляр класса Food и метод для
    генерации таких объектов"""

    def __init__(self, small_map, full_map, place_for_food, const, level_task, level_number, snake_start_pos):
        self.small_map = small_map
        self.full_map = full_map
        self.place_for_food = place_for_food
        self.const = const
        self.level_task = level_task
        self.level_number = level_number
        self.snake_start_pos = snake_start_pos
        self.food = None
        self.generate_food()

    def get_walls_position(self):

        """Метод позволяет узнать, по каким координатам на карте-модели располагаются стены"""

        walls_list = []
        for line in range(self.const.csv_resolution):
            for dot in range(self.const.csv_resolution):
                if self.small_map[line][dot] == '0':
                    walls_list.append((dot, line))
        return walls_list

    def generate_food(self):

        """Метод генерирует новый объект типа Food для объекта уровня"""

        apex = self.const.cell // 4
        coords = choice(self.place_for_food)
        trigger_coords = ((coords[0] + apex, coords[1] + apex),
                          (coords[0] - apex, coords[1] + apex),
                          (coords[0] + apex, coords[1] - apex),
                          (coords[0] - apex, coords[1] - apex))
        color = (randint(100, 150), randint(100, 150), randint(100, 150))
        food = Food(coords, trigger_coords, color)
        self.food = food

    def get_food_info(self):

        """Метод возвращает кортеж из координат центра экземпляра Food, пиковых координат и цвета """

        return self.food.coords, \
            self.food.trigger_coords, \
            self.food.color
