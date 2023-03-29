import arcade
from arcade import gui


class MainMenu:
    def __init__(self, window, const, data):
        self.command = None
        self.window = window
        self.const = const
        self.data = data

        arcade.set_background_color(self.const.window.bg_color)

        self.managerUI = gui.UIManager(window)
        self.managerUI.enable()

        self.box = gui.UIBoxLayout(vertical=True, space_between=20,)

        self.box_wrapper = gui.UIAnchorWidget(
            child=self.box,
            anchor_y='center',
            anchor_x='right',
            align_x=-(self.const.window.width - 200) // 2,
        )

        self.play = arcade.gui.UIFlatButton(text='Игра', width=200)
        self.user_levels = arcade.gui.UIFlatButton(text='Свои карты', width=200)
        self.settings = arcade.gui.UIFlatButton(text='Редактор карт', width=200)
        self.exit = arcade.gui.UIFlatButton(text='Выйти', width=200)

        self.play.on_click = self.go_play
        self.user_levels.on_click = self.go_user_levels
        self.settings.on_click = self.go_editor
        self.exit.on_click = self.go_exit

        self.box.add(self.play)
        self.box.add(self.user_levels)
        self.box.add(self.settings)
        self.box.add(self.exit)

        self.managerUI.add(self.box_wrapper)

    def go_user_levels(self, click_data):
        if click_data:
            self.command = 'U'

    def go_play(self, click_data):
        if click_data:
            self.command = 'P'

    def go_editor(self, click_data):
        if click_data:
            self.command = 'Editor'

    def go_exit(self, click_data):
        if click_data:
            self.command = 'E'

    def on_draw(self):
        self.window.clear()
        self.managerUI.draw()

    def clear(self):
        self.window.clear()
        self.managerUI.clear()
