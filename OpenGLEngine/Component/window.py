import time
import glfw
import glm
from OpenGLEngine.Component.camera import Camera

class GLWindow:
    def __init__(self, width, height, window_name='MainWindow', fps_clock=0, sensitivity=0.005):
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

        self.lastX = None
        self.lastY = None
        self.sensitivity = sensitivity

        self.create_window()
        self.bind_io_process()
        self.last_time = glfw.get_time()

    def create_window(self):
        if not glfw.init():
            raise RuntimeError('Init glfw error')
        self.window = glfw.create_window(self.width, self.height, self.name, None, None)
        if self.window is None:
            glfw.terminate()
            raise RuntimeError('Init glfw error')
        glfw.make_context_current(self.window)

    def bind_io_process(self):
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

    def set_window_camera(self, camera):
        self.camera = camera

    def set_render_function(self, render):
        self.render = render

    def input_getkey(self, deltatime):
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)
        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.camera.transfrom.translate(self.camera.transfrom.forward * deltatime)
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.camera.transfrom.translate(self.camera.transfrom.forward * -deltatime)
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.camera.transfrom.translate(self.camera.transfrom.right * -deltatime)
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.camera.transfrom.translate(self.camera.transfrom.right * deltatime)

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
        if self.fps_count_time >= 5:
            print('fps:', self.fps_count_number / 5)
            self.fps_count_time = 0
            self.fps_count_number = 0

    def mouse_callback(self, window, xpos, ypos):
        if self.lastX is None or self.lastY is None:
            self.lastX = xpos
            self.lastY = ypos
        else:
            xoffset = xpos - self.lastX
            yoffset = self.lastY - ypos
            self.lastX = xpos
            self.lastY = ypos
            xoffset *= self.sensitivity
            yoffset *= self.sensitivity
            self.camera.transfrom.rotate(glm.vec3(yoffset, xoffset, 0))

    def scroll_callback(self, window, xoffset, yoffset):
        self.camera.get_component(Camera).zoom_in(yoffset)

    def window_main_loop(self):
        self.last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()  # 终止 glfw

    def destroy(self):
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
