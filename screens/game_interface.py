import arcade
from arcade import gui


class GameInterface:
    def __init__(self, window, const, data):
        self.command = None
        self.window = window
        self.const = const
        self.walls_position = data['walls_position']
        self.level_task = data['level_task']

        self.snake_position = None
        self.food_position = None
        self.food_color = None
        self.snake_previous_pos = None

        self.manager_UI = gui.UIManager(self.window)
        self.manager_UI.enable()
        self.level_particles = arcade.ShapeElementList()
        self.level_grid = arcade.ShapeElementList()
        self.box = arcade.gui.UIBoxLayout()
        self.first = arcade.gui.UIFlatButton(text='Дальше', width=200)
        self.second = arcade.gui.UIFlatButton(text='Рестарт', width=200)
        self.third = arcade.gui.UIFlatButton(text='Домой', width=200)

        self.second.on_click = self.reload_level
        self.first.on_click = self.next
        self.third.on_click = self.home

        self.pause_window = gui.UIMessageBox(width=400,
                                             height=400,
                                             message_text='Пауза',
                                             buttons=('Продолжить',))
        self.endgame_info = arcade.gui.UITextArea(width=200,
                                                  text="",
                                                  text_color=(0, 0, 0),
                                                  font_name='Times New Roman',
                                                  font_size=30)
        self.scoreboard = arcade.gui.UITextArea(width=200,
                                                text="Счёт:",
                                                text_color=(0, 0, 0),
                                                font_name='Times New Roman',
                                                font_size=30)
        self.task = arcade.gui.UITextArea(width=200,
                                          text=f"Цель: {self.level_task}",
                                          text_color=(0, 0, 0),
                                          font_name='Times New Roman',
                                          font_size=30)

        self.manager_UI.add(
            arcade.gui.UIAnchorWidget(
                child=self.box,
                anchor_y='center',
                anchor_x='right',
                align_x=-(self.const.window.width - self.const.level.width - 200) // 2
            )
        )

        self.box.add(self.scoreboard)
        self.box.add(self.task)
        arcade.set_background_color(self.const.window.bg_color)
        self.load_level_particles()

    def reload_level(self, click_data):
        if click_data:
            self.command = 'R'

    def next(self, click_data):
        if click_data:
            self.command = 'N'

    def home(self, click_data):
        if click_data:
            self.command = 'H'

    def load_level_particles(self):
        self.level_particles = arcade.ShapeElementList()
        for x, y in self.walls_position:
            self.level_particles.append(arcade.create_rectangle_filled(
                x * self.const.level.cell + self.const.level.cell // 2,
                y * self.const.level.cell + self.const.level.cell // 2,
                self.const.level.cell,
                self.const.level.cell,
                self.const.level.walls_color))
        self.make_grid()

    def make_grid(self):
        for line in range(self.const.level.csv_resolution):
            for dot in range(self.const.level.csv_resolution):
                self.level_particles.append(
                    arcade.create_rectangle_outline(
                        dot * self.const.level.cell + self.const.level.cell // 2,
                        line * self.const.level.cell + self.const.level.cell // 2,
                        self.const.level.cell,
                        self.const.level.cell,
                        (0, 0, 0, 30),
                        2.0,
                    )
                )

    def update_score(self, new_score):
        self.scoreboard.text = f'Счёт: {new_score}'

    def on_draw(self):
        self.window.clear()
        self.level_particles.draw()
        self.manager_UI.draw()
        arcade.draw_rectangle_filled(*self.food_position, color=self.food_color)

        for x, y in self.snake_previous_pos:
            arcade.draw_rectangle_filled(x, y, self.const.snake.size, self.const.snake.size, self.const.snake.color)

        arcade.draw_rectangle_filled(*self.snake_position)

    def set_data_to_draw(self, snake_position, food_position, food_color, snake_previous_pos):
        self.snake_position = snake_position
        self.food_position = food_position
        self.food_color = food_color
        self.snake_previous_pos = snake_previous_pos

    def show_lose(self):
        self.endgame_info.text = 'Поражение!'
        self.box.add(self.endgame_info)
        self.box.add(self.second.with_space_around(20))
        self.box.add(self.third.with_space_around(20))

    def show_win(self):
        self.endgame_info.text = 'Победа!'
        self.box.add(self.endgame_info)
        self.box.add(self.first.with_space_around(20))
        self.box.add(self.second.with_space_around(20))
        self.box.add(self.third.with_space_around(20))

    def clear(self):
        self.window.clear()
        self.manager_UI.clear()
