import glm
import warnings
from typing import Optional
from OpenGLEngine.Component.transform import Transform
from OpenGLEngine.Component.mesh_filter import MeshFilter
from OpenGLEngine.Component.mesh_renderer import MeshRenderer
from OpenGLEngine.Built_inClass import *


class GameObject:
    def __init__(self, name='new GameObject', position=None, rotation=None, scale=None):
        self.name = name
        self.transform = Transform(self, position=position, rotation=rotation, scale=scale)
        self.component_list = [self.transform]

    def get_component(self, component_name):
        for component in self.component_list:
            if type(component) == component_name:
                return component
        warnings.warn('GameObject: ' + self.name + 'do not have component: ' + component_name.__name__)
        return None

    def add_component(self, component_name, *args, **kwargs):
        new_component = component_name(self, *args, **kwargs)
        self.component_list.append(new_component)

    def draw(self, view, projection, light, view_position):
        this_mesh_renderer: Optional[MeshRenderer] = self.get_component(MeshRenderer)
        this_mesh_filter: Optional[MeshFilter] = self.get_component(MeshFilter)

        if this_mesh_renderer is not None:
            this_mesh_renderer.use()

            m = glm.translate(glm.mat4(1), self.transform.position)
            m = glm.rotate(m, glm.radians(self.transform.rotation.x), glm.vec3(1, 0, 0))
            m = glm.rotate(m, glm.radians(self.transform.rotation.y), glm.vec3(0, 1, 0))
            m = glm.rotate(m, glm.radians(self.transform.rotation.z), glm.vec3(0, 0, 1))
            m = glm.scale(m, self.transform.scale)
            this_mesh_renderer.set_matrix('model', glm.value_ptr(m))
            this_mesh_renderer.set_matrix('view', glm.value_ptr(view))
            this_mesh_renderer.set_matrix('projection', glm.value_ptr(projection))
            this_mesh_renderer.un_use()
        light_view = None
        if light is not None:
            light_pos: Vector3 = light.transform.position
            light_color: Color = light.get_component(MeshRenderer).base_color.color
            light_view = (light_pos, light_color, view_position)
        if this_mesh_renderer is not None:
            this_mesh_renderer.draw(light_view=light_view)
        if this_mesh_filter is not None:
            this_mesh_filter.draw()
