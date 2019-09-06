# 创建一个简单的立方体

# 导入包
from OpenGLEngine import *

# 定义一个窗口，大小为 800x500
main_win = Window(800, 500)
# 定义一个摄像机，并设置其可见范围为 main_win 窗口的大小，注意，为了看到立方体，我们把摄像机的位置向后移动两个单位
main_camera = Create.camera(main_win, position=Vector3(0, 0, -2))
# 创建一个立方体，由于我们没有用到光照系统，所以使用 no_light_cube 函数创建一个不受环境光线的立方体
cube = Create.no_light_cube()
# 将摄像机提供给 main_win 窗口
main_win.set_window_camera(main_camera)
# 将立方体放入窗口
main_win.game_object_list.append(cube)
# 启动循环
main_win.window_main_loop()
