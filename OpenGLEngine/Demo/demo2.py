# 3D化立方体

# 导入包
from OpenGLEngine import *

# 定义一个窗口，大小为 800x500
main_win = Window(800, 500)
# 定义一个摄像机，并设置其可见范围为 main_win 窗口的大小，注意，为了看到立方体，我们把摄像机的位置向后移动两个单位
main_camera = Create.camera(main_win, position=Vector3(0, 0, -2))
# 创建一个立方体，由于我们没有用到光照系统，所以使用 no_light_cube 函数创建一个不受环境光线的立方体
# 这里添加一个参数，让 cube 获得背景贴图(请换成本地的图片链接)
cube = Create.no_light_cube(texture_path=['souce/wall.jpg'])
# 让 cube 向左边移动 0.5 个单位
cube.transform.translate(Vector3(0.5, 0, 0))
# 让 cube 旋转一定角度
cube.transform.rotate(Vector3(30, 60, 0))
# 将摄像机提供给 main_win 窗口
main_win.set_window_camera(main_camera)
# 将立方体放入窗口
main_win.game_object_list.append(cube)
# 启动循环
main_win.window_main_loop()
