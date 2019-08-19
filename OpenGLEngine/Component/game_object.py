import glm

from OpenGLEngine.Component.mesh_filter import MeshFilter
from OpenGLEngine.Component.mesh_renderer import MeshRenderer
from OpenGLEngine.Component.transform import Transform


class GameObject:
    def __init__(self, name='new GameObject', position=None, rotation=None, scale=None):
        self.name = name
        self.transfrom = Transform(self, position=position, rotation=rotation, scale=scale)
        self.component_list = [self.transfrom]

    def get_component(self, component_name):
        for component in self.component_list:
            if type(component) == component_name:
                return component
        raise RuntimeError('Component (' + component_name.__name__ + ') is not found in Object: ' + self.name)

    def add_component(self, component_name, *args, **kwargs):
        new_component = component_name(self, *args, **kwargs)
        self.component_list.append(new_component)

    def draw(self, view, projection, light):
        try:
            this_mesh_renderer = self.get_component(MeshRenderer)
        except RuntimeError:
            this_mesh_renderer = None
        try:
            this_mesh_filter = self.get_component(MeshFilter)
        except RuntimeError:
            this_mesh_filter = None

        if this_mesh_renderer is not None:
            this_mesh_renderer.use()

            m = glm.translate(glm.mat4(1), self.transfrom.position)
            # print(m)
            m = glm.rotate(m, glm.radians(self.transfrom.rotation.x), glm.vec3(1, 0, 0))
            m = glm.rotate(m, glm.radians(self.transfrom.rotation.y), glm.vec3(0, 1, 0))
            m = glm.rotate(m, glm.radians(self.transfrom.rotation.z), glm.vec3(0, 0, 1))
            # print(m)
            m = glm.scale(m, self.transfrom.scale)
            # print(m, '\n')
            this_mesh_renderer.set_matrix('model', glm.value_ptr(m))
            this_mesh_renderer.set_matrix('view', glm.value_ptr(view))
            this_mesh_renderer.set_matrix('projection', glm.value_ptr(projection))
            this_mesh_renderer.un_use()
        light_pos = list()
        light_color = list()
        for l in light:
            light_pos.append(l.transfrom.position)
            light_color.append(l.get_component(MeshRenderer).base_color.get_value())
        if this_mesh_renderer is not None:
            this_mesh_renderer.draw(light_pos=light_pos, light_color=light_color)
        if this_mesh_filter is not None:
            this_mesh_filter.draw()
