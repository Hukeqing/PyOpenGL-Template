from functools import reduce
from typing import Optional, Union, List, Tuple

import numpy as np
import pywavefront
from OpenGL.GL import *

import OpenGLEngine.DefaultModel.GLSL as GLSL
from OpenGLEngine.Built_inClass import *
from OpenGLEngine.Component import *
from OpenGLEngine.Class import *


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
    quad_vertices_VTN = [0.5, 0.5, 0, 1.0, 1.0, 0, 0, 1,
                         0.5, -0.5, 0, 1.0, 0.0, 0, 0, 1,
                         -0.5, -0.5, 0, 0.0, 0.0, 0, 0, 1,
                         -0.5, 0.5, 0, 0.0, 1.0, 0, 0, 1]
    quad_indices = [0, 1, 3,
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
    def cube(object_name: str = 'new Cube',
             position: Optional[Vector3] = None,
             rotation: Optional[Vector3] = None,
             scale: Optional[Vector3] = None,
             material: Optional[Material] = None) -> GameObject:
        new_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.GLSL_maker.get_vs(vertex_format='VTN', three_dimensional=True)
        fs = GLSL.GLSL_maker.get_fs(True)
        new_cube.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material)
        new_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VTN, vertex_format='V3T2N3', draw_type=GL_TRIANGLES)
        return new_cube

    @staticmethod
    def quad(object_name: str = 'new quad',
             position: Optional[Vector3] = None,
             rotation: Optional[Vector3] = None,
             scale: Optional[Vector3] = None,
             material: Optional[Material] = None):
        new_quad = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.GLSL_maker.get_vs(vertex_format='VTN', three_dimensional=True)
        fs = GLSL.GLSL_maker.get_fs(True)
        new_quad.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material)
        new_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VTN, vertex_format='V3T2N3', indices=Create.quad_indices,
                               draw_type=GL_TRIANGLES)

    @staticmethod
    def ignore_light_quad(object_name: str = 'new ignore light quad',
                          position: Optional[Vector3] = None,
                          rotation: Optional[Vector3] = None,
                          scale: Optional[Vector3] = None,
                          material: Optional[Material] = None):
        new_ignore_light_quad = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.GLSL_maker.get_vs(vertex_format='VT', three_dimensional=True)
        fs = GLSL.GLSL_maker.get_fs(False)
        new_ignore_light_quad.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material)
        new_ignore_light_quad.add_component(MeshFilter, vertices=Create.quad_vertices_VT, vertex_format='V3T2', indices=Create.quad_indices,
                                            draw_type=GL_TRIANGLES)

    @staticmethod
    def ignore_light_cube(object_name: str = 'new ignore light Cube',
                          position: Optional[Vector3] = None,
                          rotation: Optional[Vector3] = None,
                          scale: Optional[Vector3] = None,
                          material: Optional[Material] = None):
        new_ignore_light_cube = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vs = GLSL.GLSL_maker.get_vs('VT', True)
        fs = GLSL.GLSL_maker.get_fs(False)
        new_ignore_light_cube.add_component(MeshRenderer, vertex_shader=vs, fragment_shader=fs, material=material)
        new_ignore_light_cube.add_component(MeshFilter, vertices=Create.cube_vertices_VT, vertex_format='V3T2', draw_type=GL_TRIANGLES)
        return new_ignore_light_cube

    @staticmethod
    def direction_light(object_name: str = 'new Direction Light',
                        rotation: Optional[Vector3] = None,
                        ambient: Optional[Vector3] = None,
                        diffuse: Optional[Vector3] = None,
                        specular: Optional[Vector3] = None,
                        color: Optional[Color] = None):
        new_direction_light = GameObject(name=object_name, position=None, rotation=rotation, scale=None)
        new_direction_light.add_component(DirectionLight, ambient=ambient, diffuse=diffuse, specular=specular, color=color)
        return new_direction_light

    @staticmethod
    def point_light(object_name='new Point Light',
                    position: Optional[Vector3] = None,
                    light_range: Optional[float] = None,
                    ambient: Optional[float] = None,
                    diffuse: Optional[float] = None,
                    specular: Optional[float] = None,
                    color: Optional[Color] = None):
        new_point_light = GameObject(name=object_name, position=position, rotation=None, scale=None)
        new_point_light.add_component(PointLight, light_range=light_range, ambient=ambient, diffuse=diffuse, specular=specular, color=color)
        return new_point_light

    @staticmethod
    def spot_light(object_name='new Spot Light',
                   cut_off: Optional[float] = None,
                   outer_cut_off: Optional[float] = None,
                   position: Optional[Vector3] = None,
                   light_range: Optional[float] = None,
                   ambient: Optional[float] = None,
                   diffuse: Optional[float] = None,
                   specular: Optional[float] = None,
                   color: Optional[Color] = None):
        new_spot_light = GameObject(name=object_name, position=position, rotation=None, scale=None)
        new_spot_light.add_component(SpotLight, cut_off=cut_off, outer_cut_off=outer_cut_off, light_range=light_range, ambient=ambient,
                                     diffuse=diffuse, specular=specular, color=color)
        return new_spot_light

    @staticmethod
    def obj_object(obj_path: str,
                   object_name: str = 'new obj Object',
                   position: Optional[Vector3] = None,
                   rotation: Optional[Vector3] = None,
                   scale: Optional[Vector3] = None,
                   material: Optional[Material] = None):
        new_obj_Object = GameObject(name=object_name, position=position, rotation=rotation, scale=scale)
        vertex_format, vertices = Create.load_obj(obj_path)
        vs = GLSL.GLSL_maker.get_vs(vertex_format=vertex_format, three_dimensional=True)
        fs = GLSL.GLSL_maker.get_fs(True)
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
