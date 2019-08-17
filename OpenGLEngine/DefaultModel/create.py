from OpenGLEngine.Component.camera import Camera
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.mesh_filter import MeshFilter
from OpenGLEngine.Component.mesh_filter import vertices_pattern
from OpenGLEngine.Component.mesh_renderer import MeshRenderer
from OpenGLEngine.Class.color import DefaultColor
from OpenGL.GL import *
from os.path import join


class Create:
    default_vs_path = r'OpenGLEngine/DefaultModel/GLSL/VS'
    default_fs_path = r'OpenGLEngine/DefaultModel/GLSL/FS'

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
    cube_vertices_VN = [
        -0.5, -0.5, -0.5, 0.0, 0.0, -1.0,
        0.5, -0.5, -0.5, 0.0, 0.0, -1.0,
        0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
        0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
        -0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, -1.0,

        -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,

        -0.5, 0.5, 0.5, -1.0, 0.0, 0.0,
        -0.5, 0.5, -0.5, -1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, -1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, -1.0, 0.0, 0.0,
        -0.5, -0.5, 0.5, -1.0, 0.0, 0.0,
        -0.5, 0.5, 0.5, -1.0, 0.0, 0.0,

        0.5, 0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0,

        -0.5, -0.5, -0.5, 0.0, -1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, -1.0, 0.0,
        0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
        0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, -1.0, 0.0,

        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0]
    quad_vertices_VT = [0.5, 0.5, 0, 1.0, 1.0,
                        0.5, -0.5, 0, 1.0, 0.0,
                        -0.5, -0.5, 0, 0.0, 0.0,
                        -0.5, 0.5, 0, 0.0, 1.0]
    quad_indices_VT = [0, 1, 3,
                       1, 2, 3]

    @staticmethod
    def camera(window, object_name='new camera', position=None, rotation=None, scale=None, zoom=45, near=0.3, far=1000):
        new_camera = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        new_camera.add_component(Camera, window=window, zoom=zoom, near=near, far=far)
        return new_camera

    @staticmethod
    def cube(object_name='new Cube', position=None, rotation=None, scale=None, base_color=DefaultColor.white, texture_path=None,
             texture_mix_value=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = join(Create.default_vs_path, 'VT_MVP.vs')
        if texture_path is None:
            fs = join(Create.default_fs_path, '_C.fs')
        elif isinstance(texture_path, str):
            fs = join(Create.default_fs_path, 'T_C.fs')
        else:
            fs = join(Create.default_fs_path, 'T' + str(len(texture_path)) + '_C.fs')
        new_cube.add_component(MeshRenderer, vertex_shader_path=vs, fragment_shader_path=fs, base_color=base_color, texture_path=texture_path,
                               texture_mix_value=texture_mix_value)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format=vertices_pattern('V3T2'), draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def quad(object_name='new Quad', position=None, rotation=None, scale=None, base_color=DefaultColor.white, texture_path=None):
        new_quad = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = join(Create.default_vs_path, 'VT_MVP.vs')
        if texture_path is None:
            fs = join(Create.default_fs_path, '_C.fs')
        elif isinstance(texture_path, str):
            fs = join(Create.default_fs_path, 'T_C.fs')
        else:
            fs = join(Create.default_fs_path, 'T' + str(len(texture_path)) + '_C.fs')
        new_quad.add_component(MeshRenderer, vertex_shader_path=vs, fragment_shader_path=fs,
                               base_color=base_color, texture_path=texture_path)
        new_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VT, vertex_format=vertices_pattern('V3T2'), indices=Create.quad_indices_VT,
                               draw_type=GL_TRIANGLES)

    @staticmethod
    def test_cube(object_name='new Cube', position=None, rotation=None, scale=None, base_color=DefaultColor.white, texture_path=None,
                  texture_mix_value=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        # TODO...vs
        vs = join(Create.default_vs_path, 'VN_MVP.vs')
        if texture_path is None:
            fs = join(Create.default_fs_path, '_LC.fs')
        elif isinstance(texture_path, str):
            fs = join(Create.default_fs_path, 'T_LC.fs')
        else:
            fs = join(Create.default_fs_path, 'T' + str(len(texture_path)) + '_LC.fs')
        new_cube.add_component(MeshRenderer, vertex_shader_path=vs, fragment_shader_path=fs, base_color=base_color, texture_path=texture_path,
                               texture_mix_value=texture_mix_value)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VN, vertex_format=vertices_pattern('V3N3'), draw_type=GL_TRIANGLES)
        return new_cube
