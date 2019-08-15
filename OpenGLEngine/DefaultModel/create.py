from OpenGLEngine.Component.camera import Camera
from OpenGLEngine.Component.window import Window
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.mesh_filter import MeshFilter
from OpenGLEngine.Component.mesh_filter import vertices_pattern
from OpenGLEngine.Component.mesh_renderer import MeshRenderer
from OpenGLEngine.Component.color import DefaultColor
import glm
from OpenGL.GL import *


class Create:
    default_vt_vs_path = r'OpenGLEngine/DefaultModel/GLSL/VT.vs'
    default_vt_fs_path = r'OpenGLEngine/DefaultModel/GLSL/VT.fs'
    cube_vertices_VT = [
        -0.5, -0.5, -0.5, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0,

        -0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,

        -0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, 0.5, 1.0, 0.0,

        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,

        -0.5, -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, -0.5, 1.0, 1.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0,

        -0.5, 0.5, -0.5, 0.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0]
    quad_vertices_VT = [0.5, 0.5, 0, 1.0, 1.0,
                        0.5, -0.5, 0, 1.0, 0.0,
                        -0.5, -0.5, 0, 0.0, 0.0,
                        -0.5, 0.5, 0, 0.0, 1.0]
    quad_indices_VT = [0, 1, 3,
                       1, 2, 3]

    @staticmethod
    def camera(window, object_name='new camera', position=None, rotation=None, zoom=45, near=0.3, far=1000):
        new_camera = GameObject(name=object_name, position=position, rotation=rotation)
        new_camera.add_component(Camera, window=window, zoom=zoom, near=near, far=far)

    @staticmethod
    def cube(object_name='new Cube', position=None, rotation=None, base_color=DefaultColor.white, texture_path=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation)
        new_cube.add_component(MeshRenderer, vertex_shader_path=Create.default_vt_vs_path, fragment_shader_path=Create.default_vt_fs_path,
                               base_color=base_color, texture_path=texture_path)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format=vertices_pattern('V3T2'), draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def quad(object_name='new Quad', position=None, rotation=None, base_color=DefaultColor.white, texture_path=None):
        new_quad = GameObject(name=object_name, position=position, rotation=rotation)
        new_quad.add_component(MeshRenderer, vertex_shader_path=Create.default_vt_vs_path, fragment_shader_path=Create.default_vt_fs_path,
                               base_color=base_color, texture_path=texture_path)
        new_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VT, vertex_format=vertices_pattern('V3T2'), indices=Create.quad_indices_VT,
                               draw_type=GL_TRIANGLES)
