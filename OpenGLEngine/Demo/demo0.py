# 创建一个简单的窗口

# 导入包
from OpenGLEngine import *

# 定义一个窗口，大小为 800x500
main_win = Window(800, 500)
# 定义一个摄像机，并设置其可见范围为 main_win 窗口的大小
main_camera = Create.camera(main_win)
# 将摄像机提供给 main_win 窗口
main_win.set_window_camera(main_camera)
# 启动循环
main_win.window_main_loop()
