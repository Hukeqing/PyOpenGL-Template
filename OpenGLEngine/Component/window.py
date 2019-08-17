import time
import glfw
from OpenGL.GL import *

from OpenGLEngine.Component.camera import Camera


class Window:
    main_window = None

    def __init__(self, width, height, window_name='MainWindow', fps_clock=0, depth_mode=True):
        """
        The window for the Engine
        :param width:           the width of window
        :param height:          the height of window
        :param window_name:     the name of window
        :param fps_clock:       set the max fps in this window, 0 for INF
        :param depth_mode:      is open the depth test. False for 4 dimension, True for 3 dimension
        """
        # window properties
        self.width = width
        self.height = height
        self.name = window_name
        self.depth_mode = depth_mode
        # fps
        self.fps_clock = fps_clock
        self.fps_clock_deltatime = None if fps_clock == 0 else 1 / fps_clock
        self.fps_count_number = 0
        self.fps_count_time = 0
        # main object for window
        self.window = None
        self.camera = None
        self.light = list()
        # update function
        self.update = list()
        # game object list
        self.game_object_list = list()
        # mouse properties
        self.mouse_position = None
        self.mouse_scroll_value = 0
        # time
        self.last_time = 0
        self.delta_time = 0
        # init window
        self.create_window()
        self.bind_io_process()
        # DIY render
        self.render_function = self.window_render

    def create_window(self):
        """
        Private methods
        :return:                    None
        """
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
        """
        Private methods
        :return:                    None
        """
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

    def set_window_camera(self, camera):
        """
        Public methods
        set a camera for this window
        **You must set a camera for window**
        :camera:                the camera for this window
        :return:                None
        """
        self.camera = camera

    def add_light(self, light):
        """
        Public methods
        add a light in this window
        this light will be used in every object
        :param light:
        :return:
        """
        self.light.append(light)

    def add_update_function(self, func):
        """
        Public methods
        add a function in a list
        this function will be called in every frame
        this function should not have any args
        :param func:                function name
        :return:                    None
        """
        self.update.append(func)

    def draw(self):
        """
        Private methods
        :return:                    None
        """
        self.delta_time = glfw.get_time() - self.last_time
        self.last_time = glfw.get_time()
        if self.fps_clock != 0 and self.delta_time < self.fps_clock_deltatime:
            time.sleep(self.fps_clock_deltatime - self.delta_time)
            self.delta_time = self.fps_clock_deltatime

        for function_name in self.update:
            function_name()
        view = self.camera.get_component(Camera).get_view_matrix()
        projection = self.camera.get_component(Camera).projection
        self.render_function(view, projection)

        self.fps_count_number += 1
        self.fps_count_time += self.delta_time
        if self.fps_count_time >= 5:
            print('fps:', self.fps_count_number / 5)
            self.fps_count_time = 0
            self.fps_count_number = 0

    def window_render(self, view, projection):
        """
        Private methods
        :param view:                view of camera
        :param projection:          projection of camera
        :return:                    None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for item in self.game_object_list:
            item.draw(view, projection, self.light)

    def input_get_key(self, key_code):
        """
        judge the key_code is pressed
        :param key_code:        a static variable in class KeyCode
        :return:                if the key_code is pressed return (True) else (False)
        """
        return glfw.get_key(self.window, key_code) == glfw.PRESS

    def mouse_callback(self, window, xpos, ypos):
        """
        Private methods
        :return:                    None
        """
        self.mouse_position = (xpos, ypos)

    def scroll_callback(self, window, xoffset, yoffset):
        """
        Private methods
        :return:                    None
        """
        self.camera.get_component(Camera).zoom_in(yoffset)

    def window_main_loop(self):
        """
        Public methods
        start the window
        :return:                    None
        """
        self.last_time = glfw.get_time()
        self.mouse_scroll_value = 0
        while not glfw.window_should_close(self.window):
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()  # 终止 glfw

    def close(self):
        """
        Public methods
        end the window
        :return:                    None
        """
        glfw.set_window_should_close(self.window, True)

    def destroy(self):
        """
        Public methods
        destroy the window
        :return:                    None
        """
        glfw.destroy_window(self.window)


def window_test():
    try:
        test_window = Window(1, 1, 'test')
        test_window.destroy()
    except RuntimeError as err:
        print('\33[31mTest on windows.py Error: ' + str(err) + '\33[0m')
    else:
        print('\33[32mOK\33[0m')


if __name__ == '__main__':
    window_test()
