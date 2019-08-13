import time

import glfw


class GLWindow:
    """
    使用 glfw 创建窗体
    """

    def __init__(self, width, height, window_name='MainWindow', fps_clock=0):
        """
        创建窗体，创建后自动生成并将此窗口作为当前窗口
        :param width:           窗体宽度
        :param height:          窗体高度
        :param window_name:     窗体名字
        """
        self.width = width
        self.height = height
        self.name = window_name
        self.fps_clock = fps_clock
        self.fps_clock_deltatime = None if fps_clock == 0 else 1 / fps_clock
        self.fps_count_number = 0
        self.fps_count_time = 0

        self.window = None
        self.render = None
        self.camera = None

        self.create_window()
        self.last_time = glfw.get_time()

    def create_window(self):
        """
        创建窗体，由程序自动调用，不需要手动调用
        :return:                None
        """
        if not glfw.init():
            raise RuntimeError('Init glfw error')
        self.window = glfw.create_window(self.width, self.height, self.name, None, None)
        if self.window is None:
            glfw.terminate()
            raise RuntimeError('Init glfw error')
        glfw.make_context_current(self.window)

    def set_window_camera(self, camera):
        self.camera = camera

    def set_render_function(self, render):
        """
        设置 render 函数，此函数将在窗体 mainloop 的时候去调用
        :param render:          渲染函数
        :return:                None
        """
        self.render = render

    def input_getkey(self, deltatime):
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)
        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.camera.translate(self.camera.forward * deltatime)
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.camera.translate(self.camera.forward * -deltatime)
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.camera.rotate(self.camera.up * -deltatime)
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.camera.rotate(self.camera.up * deltatime)

    def draw(self):
        delta_time = glfw.get_time() - self.last_time
        self.last_time = glfw.get_time()
        if self.fps_clock != 0 and delta_time < self.fps_clock_deltatime:
            time.sleep(self.fps_clock_deltatime - delta_time)
            delta_time = self.fps_clock_deltatime
        self.input_getkey(delta_time)

        self.render()

        self.fps_count_number += 1
        self.fps_count_time += delta_time
        if self.fps_count_time >= 1:
            print('fps:', self.fps_count_number)
            self.fps_count_time = 0
            self.fps_count_number = 0

    def window_main_loop(self):
        """
        窗体循环。调用此函数后，将持续占用当前线程，直到关闭窗体
        :return:                None
        """
        self.last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()  # 终止 glfw

    def destroy(self):
        """
        销毁窗体，销毁后请使用 create_window 函数重新创建
        :return:                None
        """
        glfw.destroy_window(self.window)


def window_test():
    try:
        test_window = GLWindow(1, 1, 'test')
        test_window.destroy()
    except RuntimeError as err:
        print('\33[31mTest on windows.py Error: ' + str(err) + '\33[0m')
    else:
        print('\33[32mOK\33[0m')


if __name__ == '__main__':
    window_test()
