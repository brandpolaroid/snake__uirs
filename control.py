from screens.main_menu import MainMenu
from screens.game_interface import GameInterface
from screens.editor import Editor
from screens.user import UserLevels
from pathlib import Path


class Controller:
    def __init__(self, loader, interface_builder, const):
        self.loader = loader
        self.interface_builder = interface_builder
        self.current_game = None
        self.current_screen = None
        self.editor_is_active = False
        self.const = const
        self.screen_commands = ()
        self.to_update = ()
        self.to_draw = ()

    def go_main_menu(self):
        self.clear()
        self.to_update = (self.update_screen, )
        data_to_screen = {}
        self.current_screen = self.interface_builder.build(MainMenu, data_to_screen)
        self.to_draw = (self.current_screen.on_draw, )
        self.screen_commands = {'P': self.go_campaign_game,
                                'Editor': self.go_editor,
                                'E': exit,
                                'U': self.go_user_levels}

    def go_user_levels(self):
        self.clear()
        self.to_update = (self.update_screen, )
        path = Path(self.const.level.user_path)
        all_paths = list(path.iterdir())
        data_to_screen = {'paths': all_paths}
        self.current_screen = self.interface_builder.build(UserLevels, data_to_screen)
        self.to_draw = (self.current_screen.on_draw, )
        self.screen_commands = {'P': self.go_user_game, 'H': self.go_main_menu}

    def go_user_game(self):
        level = self.current_screen.get_level_to_play()
        self.loader.change_to_user_maps(level)
        return self.go_game()

    def go_campaign_game(self):
        self.loader.change_to_campaign_maps()
        return self.go_game()

    def go_editor(self):
        self.clear()
        self.to_update = (self.update_screen, self.update_editor)
        self.current_game = self.loader.load_editor()
        self.current_game.make_template()
        data_to_screen = {}
        self.current_screen = self.interface_builder.build(Editor, data_to_screen)
        self.to_draw = (self.draw_editor, self.current_screen.on_draw)
        self.screen_commands = {'active_S': (self.current_game.change_active, 'S'),
                                'active_W': (self.current_game.change_active, 'W'),
                                'save': self.save_level,
                                'H': self.go_main_menu,
                                }
        self.editor_is_active = True

    def save_level(self):
        level_name = self.current_screen.level_name
        level_task = self.current_screen.level_task
        self.current_game.save_level(level_name, level_task)
        self.go_main_menu()

    def go_game(self, is_next=False):
        self.clear()
        self.current_game = self.loader.load_game(is_next)
        self.to_update = (self.update_screen, self.update_game)
        if self.current_game is None:
            self.go_main_menu()
            return

        data_to_screen = {
            'walls_position': self.current_game.level.get_walls_position(),
            'level_task': self.current_game.level.level_task,
        }
        self.current_screen = self.interface_builder.build(GameInterface, data_to_screen)
        self.to_draw = (self.draw_game, self.current_screen.on_draw)
        self.screen_commands = {'H': self.go_main_menu, 'R': self.go_game, 'N': (self.go_game, True)}

    def clear(self):
        if self.current_screen is not None:
            self.current_screen.clear()
        self.current_game = None
        self.current_screen = None
        self.editor_is_active = False
        self.to_update = ()
        self.to_draw = ()

    def update(self):
        for func in self.to_update:
            func()

    def update_game(self):
        if self.current_game is not None and self.current_game.active:
            self.current_game.update()
            self.current_screen.update_score(self.current_game.score)
            if self.current_game.status is True:
                self.current_screen.show_win()
            elif self.current_game.status is False:
                self.current_screen.show_lose()

    def draw_game(self):
        data = self.current_game.snake.get_info()
        food_pos = (*self.current_game.level.food.coords,
                    self.const.level.food_size,
                    self.const.level.food_size)
        food_color = self.current_game.level.food.color
        snake_previous_pos = self.current_game.snake.previous_positions
        self.current_screen.set_data_to_draw(data, food_pos, food_color, snake_previous_pos)

    def draw_editor(self):
        data = self.current_game.get_all_data()
        self.current_screen.set_data_to_draw(data)

    def update_editor(self):
        pass

    def on_key_press(self, symbol):
        if self.editor_is_active is not True and self.current_game.active:
            match symbol:
                case 119: self.current_game.change_direction((0, 1))
                case 115: self.current_game.change_direction((0, -1))
                case 100: self.current_game.change_direction((1, 0))
                case 97: self.current_game.change_direction((-1, 0))

    def on_mouse_press(self, x, y):
        if self.editor_is_active:
            self.current_game.click(x, y)

    def on_draw(self):
        for func in self.to_draw:
            func()

    def update_screen(self):
        if self.current_screen.command in self.screen_commands:
            to_execute = self.screen_commands[self.current_screen.command]
            self.current_screen.command = None
            if isinstance(to_execute, tuple):
                args = tuple(to_execute[1:])
                to_execute = to_execute[0]
                to_execute(args)
                return
            else:
                to_execute()
                return
        if self.editor_is_active:
            self.current_screen.update()


class InterfaceBuilder:
    def __init__(self, const):
        self.window = None
        self.const = const

    def build(self, screen_cls, data):
        return screen_cls(self.window, self.const, data)

    def set_window(self, window):
        self.window = window
