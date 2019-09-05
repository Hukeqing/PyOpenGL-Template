import pywavefront
import numpy as np
from OpenGLEngine.Class import *
from OpenGLEngine.Component import *
from OpenGLEngine.DefaultModel import *
from OpenGL.GL import *
import OpenGLEngine.DefaultModel.glsl as glsl


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
    cube_vertices_VTN = [
        -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, -1.0,
        0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 0.0, -1.0,
        0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 0.0, -1.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, -1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 0.0, -1.0, 0.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, -1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, -1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, -1.0, 0.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, -1.0, 0.0, 0.0,
        -0.5, 0.5, 0.5, 1.0, 0.0, -1.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, 0.0, -1.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -1.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0, -1.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0, -1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, -1.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, 0.0, -1.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0]
    quad_vertices_VT = [0.5, 0.5, 0, 1.0, 1.0,
                        0.5, -0.5, 0, 1.0, 0.0,
                        -0.5, -0.5, 0, 0.0, 0.0,
                        -0.5, 0.5, 0, 0.0, 1.0]
    quad_indices_VT = [0, 1, 3,
                       1, 2, 3]

    @staticmethod
    def camera(window, object_name='new camera', position=None, rotation=None, scale=None, zoom=45, near=0.3, far=1000):
        new_camera = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        new_camera.add_component(Camera, window=(window.width, window.height) if isinstance(window, Window) else window, zoom=zoom, near=near,
                                 far=far)
        return new_camera

    @staticmethod
    def orthogonal_camera(left, right, bottom, up, object_name='new camera', position=None, rotation=None, scale=None, near=0.3, far=1000):
        new_orthogonal_camera = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        new_orthogonal_camera.add_component(OrthogonalCamera, left=left, right=right, bottom=bottom, up=up, near=near, far=far)
        return new_orthogonal_camera

    @staticmethod
    def quad(object_name='new Quad', position=None, rotation=None, scale=None, base_color=DefaultColor.white, texture_path=None):
        # Bate mode
        new_quad = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        # vs = join(Create.default_vs_path, 'VN_MVP.vs_maker')
        # if texture_path is None:
        #     fs = join(Create.default_fs_path, '_C.fs_maker')
        # elif isinstance(texture_path, str):
        #     fs = join(Create.default_fs_path, 'T_C.fs_maker')
        # else:
        #     fs = join(Create.default_fs_path, 'T' + str(len(texture_path)) + '_C.fs_maker')
        vs = ''
        fs = ''
        # TODO...
        new_quad.add_component(MeshRenderer, vertex_shader_path=vs, fragment_shader_path=fs,
                               base_color=base_color, texture_path=texture_path)
        new_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VT, vertex_format='V3T2', indices=Create.quad_indices_VT,
                               draw_type=GL_TRIANGLES)

    @staticmethod
    def cube(object_name='new Cube', position=None, rotation=None, scale=None, base_color=DefaultColor.white, texture_path=None,
             texture_mix_value=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        # vs_maker = join(Create.default_vs_path, 'VTN_MVP.vs_maker')
        # if texture_path is None:
        #     fs_maker = join(Create.default_fs_path, '_LC.fs_maker')
        # elif isinstance(texture_path, str):
        #     fs_maker = join(Create.default_fs_path, 'T_LC.fs_maker')
        # else:
        #     fs_maker = join(Create.default_fs_path, 'T' + str(len(texture_path)) + '_LC.fs_maker')
        vs = glsl.vs_maker('VTN', True).data
        fs = glsl.fs_maker(len(texture_path), True).data
        new_cube.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, base_color=base_color, texture_path=texture_path,
                               texture_mix_value=texture_mix_value)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VTN, vertex_format='V3T2N3', draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def point_light(object_name='new Point Light', position=None, scale=None, base_color=DefaultColor.white):
        new_light = GameObject(name=object_name, position=position, rotation=None, scale=scale)
        # vs_maker = join(Create.default_vs_path, 'VT_MVP.vs_maker')
        vs = glsl.vs_maker('VT', True).data
        # fs_maker = join(Create.default_fs_path, '_C.fs_maker')
        fs = glsl.fs_maker(0, False).data
        new_light.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, base_color=base_color, texture_path=None,
                                texture_mix_value=None)
        new_light.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format='V3T2', draw_type=GL_TRIANGLES)
        return new_light

    @staticmethod
    def obj_object(obj_path: str, object_name='new obj Object', position=None, rotation=None, scale=None, base_color=DefaultColor.white):
        new_obj_Object = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vertices = Create.load_obj(obj_path)
        vs = glsl.vs_maker('VN', True).data
        fs = glsl.fs_maker(0, True).data
        print(fs)
        new_obj_Object.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, base_color=base_color)
        new_obj_Object.add_component(MeshFilter, vertices=vertices, vertex_format='V3N3', draw_type=GL_TRIANGLES)
        return new_obj_Object

    @staticmethod
    def load_obj(path: str):
        obj_wf = pywavefront.Wavefront(path)
        obj_wf.parse()
        for name, material in obj_wf.materials.items():
            vertices = np.array(material.vertices, dtype=np.float32)
            vertices.resize((vertices.size // 6, 6))
            vertices[:, [0, 1, 2, 3, 4, 5]] = vertices[:, [3, 4, 5, 0, 1, 2]]
            vertices.resize(vertices.size)
            return vertices
