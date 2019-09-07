import time
from typing import Optional, Union, Callable, List, Tuple

import glfw
from OpenGL.GL import *

from OpenGLEngine.Built_inClass import *
from OpenGLEngine.Component import *
from OpenGLEngine.Component.direction_light import DirectionLight
from OpenGLEngine.Component.point_light import PointLight
from OpenGLEngine.Component.spot_light import SpotLight


class Window:
    def __init__(self,
                 width: int,
                 height: int,
                 window_name: Optional[str] = 'MainWindow',
                 background_color: Optional[Color] = None,
                 fps_clock: int = 0,
                 depth_mode: bool = True,
                 alpha_mode: bool = True,
                 basic_move: Optional[Union[Tuple[Union[int, float], Union[int, float], Union[int, float]], List[Union[int, float]]]] = None):
        """
        The window for the Engine
        :param width:           the width of window(int)
        :param height:          the height of window(int)
        :param background_color the background color in this window(Color)
        :param window_name:     the name of window(str)
        :param fps_clock:       set the max fps in this window, 0 for INF(int)
        :param depth_mode:      is open the depth test. False for 4 dimension, True for 3 dimension(bool)
        :param alpha_mode:      allow the object has alpha(bool)
        :param basic_move:      enable the basic move by key(tuple, list)
        """
        # window properties
        self.width: int = width
        self.height: int = height
        self.name: str = window_name
        self.depth_mode: bool = depth_mode
        self.alpha_mode: bool = alpha_mode
        self.background_color: Color = Color(0, 0, 0) if background_color is None else background_color
        # fps
        self.fps_clock: int = fps_clock
        self.fps_clock_deltatime: float = None if fps_clock == 0 else 1 / fps_clock
        self.fps_count_number: int = 0
        self.fps_count_time: int = 0
        # main object for window
        self.window: object = None
        self.camera: Optional[GameObject] = None
        self.direction_light: List[GameObject] = list()
        self.point_light: List[GameObject] = list()
        self.spot_light: List[GameObject] = list()
        self.light: Tuple[List[GameObject], List[GameObject], List[GameObject]] = (self.direction_light, self.point_light, self.spot_light)
        # update function
        self.update: List[Callable[[], bool]] = list()
        # game object list
        self.game_object_list: List[GameObject] = list()
        # mouse properties
        self.mouse_position: Tuple[int, int] = (0, 0)
        self.mouse_scroll_value: int = 0
        # time
        self.last_time: int = 0
        self.delta_time: float = 0
        self.basic_move: Optional[Union[Tuple[Union[int, float], Union[int, float], Union[int, float]], List[Union[int, float]]]] = basic_move
        # init window
        self.create_window()
        self.bind_io_process()
        # DIY render
        self.render_function = self.window_render

    def create_window(self):
        if not glfw.init():
            raise RuntimeError('Init glfw error')
        self.window = glfw.create_window(self.width, self.height, self.name, None, None)
        if self.window is None:
            glfw.terminate()
            raise RuntimeError('Init glfw error')
        glfw.make_context_current(self.window)
        Window.main_window = self.window
        self.last_time = glfw.get_time()
        if self.depth_mode:
            glEnable(GL_DEPTH_TEST)

    def bind_io_process(self):
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

    def set_window_camera(self, camera: GameObject):
        self.camera = camera

    def add_light(self, light: GameObject):
        if light.get_component(DirectionLight) is not None:
            self.direction_light.append(light)
        elif light.get_component(PointLight) is not None:
            self.point_light.append(light)
        elif light.get_component(SpotLight) is not None:
            self.spot_light.append(light)
        else:
            raise ValueError('This is not a Light')

    def add_update_function(self, update: Callable[[], bool]):
        self.update.append(update)

    def draw(self):
        self.delta_time = glfw.get_time() - self.last_time
        self.last_time = glfw.get_time()
        if self.fps_clock != 0 and self.delta_time < self.fps_clock_deltatime:
            time.sleep(self.fps_clock_deltatime - self.delta_time)
            self.delta_time = self.fps_clock_deltatime

        for function_name in self.update:
            if not function_name():
                raise RuntimeError('Function ' + function_name.__name__ + ' runtime error')
        view = self.camera.transform.get_view_matrix()
        projection = self.camera.get_component(Camera).projection
        self.render_function(view, projection)

        self.fps_count_number += 1
        self.fps_count_time += self.delta_time
        if self.fps_count_time >= 5:
            print('fps:', self.fps_count_number / 5)
            self.fps_count_time = 0
            self.fps_count_number = 0

    def window_render(self, view, projection):
        if self.basic_move is not None:
            if self.input_get_key(glfw.KEY_W):
                self.camera.transform.translate(self.camera.transform.forward * self.basic_move[0] * self.delta_time)
            if self.input_get_key(glfw.KEY_S):
                self.camera.transform.translate(-self.camera.transform.forward * self.basic_move[0] * self.delta_time)
            if self.input_get_key(glfw.KEY_A):
                self.camera.transform.rotate(-self.camera.transform.up * self.basic_move[1] * self.delta_time)
            if self.input_get_key(glfw.KEY_D):
                self.camera.transform.rotate(self.camera.transform.up * self.basic_move[1] * self.delta_time)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for item in self.game_object_list:
            item.draw(view, projection, self.light, self.camera.transform.position)

    def input_get_key(self, key_code):
        return glfw.get_key(self.window, key_code) == glfw.PRESS

    def mouse_callback(self, window, xpos, ypos):
        self.mouse_position = (xpos, ypos)

    def scroll_callback(self, window, xoffset, yoffset):
        if self.basic_move is not None:
            self.camera.get_component(Camera).zoom_in(yoffset * self.basic_move[2])
        self.mouse_scroll_value += yoffset

    def window_main_loop(self):
        glClearColor(*self.background_color.get_value())
        # glClearDepth(1.0)
        # glPointSize(5)

        if self.alpha_mode:
            glEnable(GL_BLEND)  # 使透明生效
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 使透明生效
        self.last_time = glfw.get_time()
        self.mouse_scroll_value = 0
        while not glfw.window_should_close(self.window):
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()  # 终止 glfw

    def close(self):
        glfw.set_window_should_close(self.window, True)

    def destroy(self):
        glfw.destroy_window(self.window)


def window_test():
    try:
        test_window = Window(1, 1, 'test')
        test_window.destroy()
    except RuntimeError as error_str:
        print('\33[31mTest on windows.py Error: ' + str(error_str) + '\33[0m')
    else:
        print('\33[32mOK\33[0m')


if __name__ == '__main__':
    window_test()
