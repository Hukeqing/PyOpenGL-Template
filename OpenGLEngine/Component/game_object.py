import warnings
from typing import Optional

import glm

from OpenGLEngine.Component.mesh_filter import MeshFilter
from OpenGLEngine.Component.mesh_renderer import MeshRenderer
from OpenGLEngine.Component.transform import Transform


class GameObject:
    def __init__(self,
                 name='new GameObject',
                 position=None,
                 rotation=None,
                 scale=None,
                 draw_rotate=None):
        self.name = name
        self.transform = Transform(self, position=position, rotation=rotation, scale=scale)
        self.component_list = [self.transform]
        self.draw_rotate = draw_rotate if draw_rotate is not None else 'xyz'
        self.renderer = lambda model, view, projection: (model, view, projection)

    def get_component(self, component_name):
        for component in self.component_list:
            if type(component) == component_name or type(component).__name__ == component_name:
                return component
        # warnings.warn('GameObject: ' + self.name + ' do not have component: ' + component_name.__name__)
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
            for c in self.draw_rotate:
                if c == 'x':
                    m = glm.rotate(m, glm.radians(self.transform.rotation.x), glm.vec3(1, 0, 0))
                elif c == 'y':
                    m = glm.rotate(m, glm.radians(self.transform.rotation.y), glm.vec3(0, 1, 0))
                elif c == 'z':
                    m = glm.rotate(m, glm.radians(self.transform.rotation.z), glm.vec3(0, 0, 1))
            m = glm.scale(m, self.transform.scale)
            model, view, projection = self.renderer(model=m, view=view, projection=projection)
            this_mesh_renderer.set_matrix('model', glm.value_ptr(model))
            this_mesh_renderer.set_matrix('view', glm.value_ptr(view))
            this_mesh_renderer.set_matrix('projection', glm.value_ptr(projection))
            this_mesh_renderer.draw(light_tuple=light, view_position=view_position)
            # this_mesh_renderer.un_use()
        if this_mesh_filter is not None:
            this_mesh_filter.draw()
