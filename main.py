import arcade
from basic_constants import Constants
import game
import control


class ArcadeGame(arcade.Window):
    def __init__(self, controller, const):
        super().__init__(const.window.width, const.window.height, const.window.title)
        self.controller = controller
        self.controller.interface_builder.set_window(self)
        self.controller.go_main_menu()

    def on_draw(self):
        self.controller.on_draw()

    def update(self, delta_time: float):
        self.controller.update()

    def on_key_press(self, symbol: int, modifiers: int):
        self.controller.on_key_press(symbol)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.controller.on_mouse_press(x, y)


def main():
    const = Constants()
    loader = game.Loader(const)
    interface_builder = control.InterfaceBuilder(const)
    controller = control.Controller(loader, interface_builder, const)
    ArcadeGame(controller, const)
    arcade.run()


if __name__ == '__main__':
    main()
