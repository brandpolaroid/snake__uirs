import arcade
from arcade import gui
import maps


class Editor:
    def __init__(self, window, const, data):
        self.command = None
        self.level_name = f'level_{maps.get_user_amount() + 1}'
        self.level_task = None
        self.window = window
        self.const = const
        self.data = data
        self.snake_position = None
        self.active_element = None
        self.walls_position = None
        self.all_particles = {}

        arcade.set_background_color(self.const.window.bg_color)

        self.managerUI = gui.UIManager(window)
        self.managerUI.enable()

        self.box = gui.UIBoxLayout(space_between=20)

        self.box_wrapper = gui.UIAnchorWidget(
            child=self.box,
            anchor_y='center',
            anchor_x='right',
            align_x=-(self.const.window.width - self.const.level.width - 500) // 2,
        )

        self.change_button = gui.UIFlatButton(text='Стена', width=200)
        self.change_button.on_click = self.change_active

        self.save_button = gui.UIFlatButton(text='Сохранить', width=200)
        self.save_button.on_click = self.save_level

        self.back_button = gui.UIFlatButton(text='В меню', width=200)
        self.back_button.on_click = self.go_home

        self.info = arcade.gui.UITextArea(width=500,
                                          text="Нажми на верхнюю кнопку, "
                                               "чтобы изменить предмет, "
                                               "который ставится на карту. "
                                               "Снизу нужно вписать цель уровня, "
                                               "после чего сохранить его.",
                                          text_color=(0, 0, 0),
                                          font_name='Times New Roman',
                                          font_size=25,
                                          height=200,
                                          )

        self.level_task_label = arcade.gui.UIInputText(width=200,
                                                       height=50,
                                                       text='8',
                                                       font_name='Times New Roman',
                                                       font_size=25,
                                                       text_color=(0, 0, 0))

        self.box.add(self.change_button)
        self.box.add(self.info)
        self.box.add(self.level_task_label)
        self.box.add(self.save_button.with_space_around(top=50))
        self.box.add(self.back_button.with_space_around(top=20))

        self.managerUI.add(self.box_wrapper)

        self.level_particles = arcade.ShapeElementList()
        self.grid = arcade.ShapeElementList()
        self.make_grid()

    def change_active(self, click_data):
        if click_data:
            if self.active_element == 'W':
                self.change_button.text = 'Змейка'
                self.command = 'active_S'
            elif self.active_element == 'S':
                self.change_button.text = 'Стена'
                self.command = 'active_W'

    def save_level(self, click_data):
        if click_data:
            self.level_task = int(self.level_task_label.text)
            self.command = 'save'

    def clear(self):
        self.window.clear()
        self.managerUI.clear()

    def go_home(self, click_data):
        if click_data:
            self.command = 'H'

    def set_data_to_draw(self, data):
        self.snake_position = data[0]
        self.walls_position = data[1]
        self.active_element = data[2]

    def add_square(self, click, is_snake=False):
        element_x = click[0]
        element_y = click[1]
        if is_snake:
            color = self.const.snake.color
        else:
            color = self.const.level.walls_color
        particle = arcade.create_rectangle_filled(
            element_x * self.const.level.cell + self.const.level.cell // 2,
            element_y * self.const.level.cell + self.const.level.cell // 2,
            self.const.level.cell,
            self.const.level.cell,
            color)
        self.level_particles.append(particle)
        self.all_particles[(element_x, element_y)] = particle

    def remove_square(self, click):
        element_x = click[0]
        element_y = click[1]
        self.level_particles.remove(self.all_particles[(element_x, element_y)])
        self.all_particles.pop(click)
        if len(self.level_particles) == 0:
            self.level_particles = arcade.ShapeElementList()

    def make_grid(self):
        for line in range(self.const.level.csv_resolution):
            for dot in range(self.const.level.csv_resolution):
                self.grid.append(
                    arcade.create_rectangle_outline(
                        dot * self.const.level.cell + self.const.level.cell // 2,
                        line * self.const.level.cell + self.const.level.cell // 2,
                        self.const.level.cell,
                        self.const.level.cell,
                        (0, 0, 0, 30),
                        2.0,
                    )
                )

    def on_draw(self):
        self.window.clear()
        self.managerUI.draw()
        self.level_particles.draw()
        self.grid.draw()

    def update(self):
        particles_keys = list(self.all_particles.keys())
        for i in self.walls_position:
            if i not in particles_keys:
                self.add_square(i)

        if self.snake_position is not None and self.snake_position not in particles_keys:
            self.add_square(self.snake_position, True)

        for i in particles_keys:
            if i not in self.walls_position and i != self.snake_position:
                self.remove_square(i)
