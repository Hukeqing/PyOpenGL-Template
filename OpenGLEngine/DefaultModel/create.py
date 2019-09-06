import pywavefront
import numpy as np
from OpenGLEngine.Built_inClass import *
from OpenGLEngine.Component import *
from OpenGLEngine.Class import *
import OpenGLEngine.DefaultModel.GLSL as GLSL
from OpenGL.GL import *
from typing import Optional, Union, Callable, List, Tuple
from functools import reduce


class Create:
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
    def camera(window: Window,
               object_name: str = 'new camera',
               position: Optional[Vector3] = None,
               rotation: Optional[Vector3] = None,
               scale: Optional[Vector3] = None,
               zoom: int = 45,
               near: float = 0.3,
               far: float = 1000) -> GameObject:
        new_camera = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        new_camera.add_component(Camera, window=(window.width, window.height) if isinstance(window, Window) else window, zoom=zoom, near=near,
                                 far=far)
        return new_camera

    @staticmethod
    def orthogonal_camera(left: int,
                          right: int,
                          bottom: int,
                          up: int,
                          object_name: str = 'new camera',
                          position: Optional[Vector3] = None,
                          rotation: Optional[Vector3] = None,
                          scale: Optional[Vector3] = None,
                          near: float = 0.3,
                          far: float = 1000) -> GameObject:
        new_orthogonal_camera = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        new_orthogonal_camera.add_component(OrthogonalCamera, left=left, right=right, bottom=bottom, up=up, near=near, far=far)
        return new_orthogonal_camera

    @staticmethod
    def quad(object_name: str = 'new Quad',
             position: Optional[Vector3] = None,
             rotation: Optional[Vector3] = None,
             scale: Optional[Vector3] = None,
             material: Color = DefaultMaterial,
             texture_path: Optional[List[str]] = None):
        # Bate mode
        new_quad = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.vs_maker(vertex_format='VT', three_dimensional=True)
        fs = GLSL.fs_maker(texture_number=0, light=False)
        new_quad.add_component(MeshRenderer, vertex_shader_path=vs, fragment_shader_path=fs,
                               material=material, texture_path=texture_path)
        new_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VT, vertex_format='V3T2', indices=Create.quad_indices_VT,
                               draw_type=GL_TRIANGLES)

    @staticmethod
    def cube(object_name='new Cube', position=None, rotation=None, scale=None, material=DefaultMaterial, texture_path=None,
             texture_mix_value=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.vs_maker('VTN', True).data
        fs = GLSL.fs_maker(len(texture_path), True).data
        new_cube.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material, texture_path=texture_path,
                               texture_mix_value=texture_mix_value)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VTN, vertex_format='V3T2N3', draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def no_light_cube(object_name='new Cube', position=None, rotation=None, scale=None, material=DefaultMaterial,
                      texture_path: Optional[Union[List[str], tuple]] = None,
                      texture_mix_value=None):
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.vs_maker('VT', True).data
        fs = GLSL.fs_maker(0 if texture_path is None else len(texture_path), False).data
        new_cube.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material, texture_path=texture_path,
                               texture_mix_value=texture_mix_value)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format='V3T2', draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def point_light(object_name='new Point Light', position=None, scale=None):
        new_light = GameObject(name=object_name, position=position, rotation=None, scale=scale)
        vs = GLSL.vs_maker('VT', True).data
        fs = GLSL.fs_maker(0, False).data
        new_light.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=DefaultMaterial, texture_path=None,
                                texture_mix_value=None)
        new_light.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format='V3T2', draw_type=GL_TRIANGLES)
        return new_light

    @staticmethod
    def obj_object(obj_path: str, object_name='new obj Object', position=None, rotation=None, scale=None, material=DefaultColor.white):
        new_obj_Object = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vertex_format, vertices = Create.load_obj(obj_path)
        vs = GLSL.vs_maker(vertex_format, True).data
        fs = GLSL.fs_maker(0, True).data
        new_obj_Object.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material)
        new_obj_Object.add_component(MeshFilter, vertices=vertices, vertex_format='V3N3', draw_type=GL_TRIANGLES)
        return new_obj_Object

    @staticmethod
    def load_obj(path: str):
        obj_wf = pywavefront.Wavefront(path)
        obj_wf.parse()
        for obj_name, material in obj_wf.materials.items():
            vertices = np.array(material.vertices, dtype=np.float32)
            vertex_format = reduce(lambda a, b: a + b, [item[0] for item in material.vertex_format.split('_')])
            vertices.resize((vertices.size // 6, 6))
            vertices.resize(vertices.size)
            return vertex_format, vertices
