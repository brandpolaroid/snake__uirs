import arcade
from arcade import gui


class UserLevels:
    def __init__(self, window, const, data):
        self.command = None
        self.level_to_play = 0

        self.window = window
        self.all_paths = data['paths']
        self.const = const

        self.managerUI = gui.UIManager(self.window)
        self.managerUI.enable()

        self.box = arcade.gui.UIBoxLayout()
        self.levels = []
        self.level_handlers = []

        for i_path in range(len(self.all_paths)):
            level = arcade.gui.UIFlatButton(text=f'{self.all_paths[i_path]}'[10:-4], width=200)
            level.on_click = self.play
            self.box.add(level.with_space_around(bottom=20))
            self.levels.append(level)

        self.go_home = arcade.gui.UIFlatButton(text='Назад', width=200)
        self.go_home.on_click = self.home

        self.box.add(self.go_home)

        self.managerUI.add(
            arcade.gui.UIAnchorWidget(
                child=self.box,
                anchor_y='center',
                anchor_x='right',
                align_x=-(self.const.window.width - 200) // 2
            )
        )

        arcade.set_background_color(self.const.window.bg_color)

    def play(self, click_data):
        button_obj = click_data.source
        for i_level in range(len(self.levels)):
            if self.levels[i_level] == button_obj:
                self.level_to_play = i_level + 1
                self.command = 'P'

    def get_level_to_play(self):
        return self.level_to_play

    def home(self, click_data):
        if click_data:
            self.command = 'H'

    def clear(self):
        self.window.clear()
        self.managerUI.clear()

    def on_draw(self):
        self.window.clear()
        self.managerUI.draw()
