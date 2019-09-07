import numpy as np
from OpenGL.GL import *
import glfw
from ctypes import c_float, c_void_p, sizeof

# 创建窗口
window_width = 400
window_height = 300
window_name = "test"
glfw.init()
window = glfw.create_window(window_width, window_height, window_name, None, None)
glfw.make_context_current(window)
# glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
# glfw.set_cursor_pos_callback(window, mouse_callback)
# glfw.set_scroll_callback(window, scroll_callback)
# glfw.set_framebuffer_size_callback(window, reshape)

vertices = np.array([0.5, 0.5, 0, 1.0, 0.0, 0.0,
                     0.5, -0.5, 0, 0.0, 1.0, 0.0,
                     -0.5, -0.5, 0, 0.0, 0.0, 1.0,
                     -0.5, 0.5, 0, 1.0, 0.0, 1.0], dtype=np.float32)

# 创建一个VAO
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# 顶点输入
# 使用glGenBuffers函数和一个缓冲ID生成一个VBO对象
vbo = glGenBuffers(1)
# 顶点缓冲对象的缓冲类型是GL_ARRAY_BUFFER。OpenGL允许我们同时绑定多个缓冲，只要它们是不同的缓冲类型。
# 使用glBindBuffer函数把新创建的缓冲绑定到GL_ARRAY_BUFFER目标上
glBindBuffer(GL_ARRAY_BUFFER, vbo)
# 调用glBufferData函数，它会把之前定义的顶点数据复制到缓冲的内存中
# 它的第一个参数是目标缓冲的类型：顶点缓冲对象当前绑定到GL_ARRAY_BUFFER目标上。第二个参数是我们希望发送的实际数据。
# 第四个参数指定了我们希望显卡如何管理给定的数据。它有三种形式：
# GL_STATIC_DRAW ：数据不会或几乎不会改变。
# GL_DYNAMIC_DRAW：数据会被改变很多。
# GL_STREAM_DRAW ：数据每次绘制时都会改变。
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

# 索引缓冲对象
indices = np.array([0, 1, 3,
                    1, 2, 3], dtype=np.int32)
ebo = glGenBuffers(1)
# 绑定EBO然后用glBufferData把索引复制到缓冲里。
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

# 编译顶点着色器
# 创建一个顶点着色器对象
vertexShader = glCreateShader(GL_VERTEX_SHADER)
# vertexShaderSource = open('GLSL_Template/vc/v3c3/v3c3.VS', 'r').read()
vertexShaderSource = '''#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

void main()
{
    gl_Position = vec4(aPos.xyz, 1.0);
    ourColor = aColor;
}
'''
# 下一步我们把这个着色器源码附加到着色器对象上，然后编译它
# glShaderSource函数把要编译的着色器对象作为第一个参数。
# 第二个参数是顶点着色器真正的源码
glShaderSource(vertexShader, vertexShaderSource)
glCompileShader(vertexShader)
# 检测在调用glCompileShader后编译是否成功
message = glGetShaderInfoLog(vertexShader)
print("shader compile error: ", message) if message else print('shader compile success')

# 片段着色器
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
# fragmentShaderSource = open('GLSL_Template/vc/v3c3/v3c3.GLSL_maker', 'r').read()
fragmentShaderSource = '''#version 330 core
out vec4 FragColor;  
in vec3 ourColor;

void main()
{
    FragColor = vec4(ourColor, 1.0);
}'''
glShaderSource(fragmentShader, fragmentShaderSource)
glCompileShader(fragmentShader)
# 检测在调用glCompileShader后编译是否成功
message = glGetShaderInfoLog(vertexShader)
print("shader compile error: ", message) if message else print('shader compile success')

# 着色器程序
# 把它们链接(Link)为一个着色器程序对象
# 创建一个程序对象
shaderProgram = glCreateProgram()
glAttachShader(shaderProgram, vertexShader)
glAttachShader(shaderProgram, fragmentShader)
glLinkProgram(shaderProgram)
# 检测在调用glLinkProgram后是否成功
message = glGetProgramInfoLog(shaderProgram)
print("program link error: ", message) if message else print('program link success')
# 删除着色器对象
glDeleteShader(vertexShader)
glDeleteShader(fragmentShader)
# 调用glUseProgram函数，用刚创建的程序对象作为它的参数，以激活这个程序对象
# glUseProgram(shaderProgram)

# 链接顶点属性
# 使用glVertexAttribPointer函数告诉OpenGL该如何解析顶点数据
# 第一个参数指定我们要配置的顶点属性。还记得我们在顶点着色器中使用layout(location = 0)定义了position顶点属性的位置值(Location)吗？
# 它可以把顶点属性的位置值设置为0。因为我们希望把数据传递到这一个顶点属性中，所以这里我们传入0。
#
# 第二个参数指定顶点属性的大小。顶点属性是一个vec3，它由3个值组成，所以大小是3。
# 第三个参数指定数据的类型，这里是GL_FLOAT(GLSL中vec*都是由浮点数值组成的)。
#
# 下个参数定义我们是否希望数据被标准化(Normalize)。如果我们设置为GL_TRUE，
# 所有数据都会被映射到0（对于有符号型signed数据是-1）到1之间。我们把它设置为GL_FALSE。
#
# 第五个参数叫做步长(Stride)，它告诉我们在连续的顶点属性组之间的间隔。由于下个组位置数据在3个float之后，
# 我们把步长设置为3 * sizeof(float)。要注意的是由于我们知道这个数组是紧密排列的（在两个顶点属性之间没有空隙）
# 我们也可以设置为0来让OpenGL决定具体步长是多少（只有当数值是紧密排列时才可用）。
# 一旦我们有更多的顶点属性，我们就必须更小心地定义每个顶点属性之间的间隔，我们在后面会看到更多的例子（
# 译注: 这个参数的意思简单说就是从这个属性第二次出现的地方到整个数组0位置之间有多少字节）。
#
# 最后一个参数的类型是void*，所以需要我们进行这个奇怪的强制类型转换。它表示位置数据在缓冲中起始位置的偏移量(Offset)。由于位置数据在数组的开头，所以这里是0。我们会在后面详细解释这个参数。
glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(c_float), c_void_p(0 * sizeof(c_float)))
# 使用glEnableVertexAttribArray，以顶点属性位置值作为参数，启用顶点属性；顶点属性默认是禁用的。
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
glEnableVertexAttribArray(1)


# 绘制
# glDrawArrays函数第一个参数是我们打算绘制的OpenGL图元的类型。
# 由于我们在一开始时说过，我们希望绘制的是一个三角形，这里传递GL_TRIANGLES给它。
# 第二个参数指定了顶点数组的起始索引，我们这里填0。
# 最后一个参数指定我们打算绘制多少个顶点，这里是3（我们只从我们的数据中渲染一个三角形，它只有3个顶点长）。
def render():
    glUseProgram(shaderProgram)
    glBindVertexArray(vao)
    # 使用 Uniform 添加颜色
    # glUniform4f(glGetUniformLocation(shaderProgram, 'ourColor'), 1, 0, 1, 1)

    # 绘制VAO
    # glDrawArrays(GL_TRIANGLES, 0, 4)

    # 绘制EBO
    # 第一个参数指定了我们绘制的模式，这个和glDrawArrays的一样。
    # 第二个参数是我们打算绘制顶点的个数，这里填6，也就是说我们一共需要绘制6个顶点。
    # 第三个参数是索引的类型，这里是GL_UNSIGNED_INT。
    # 最后一个参数里我们可以指定EBO中的偏移量（或者传递一个索引数组，但是这是当你不在使用索引缓冲对象的时候），
    # 但是我们会在这里填写None。
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    glBindVertexArray(0)


while not glfw.window_should_close(window):
    render()
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
