import glm

from OpenGLEngine.Component.camera import Camera
from OpenGLEngine.Component.transform import Transform


class GameObject:
    def __init__(self, name='new GameObject', position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0)):
        self.name = name
        self.transfrom = Transform(self, position=position, rotation=rotation)
        self.component_list = [self.transfrom]

    def get_component(self, component_name):
        for component in self.component_list:
            if type(component) == component_name:
                return component
        raise RuntimeError('Component (' + component_name.__name__ + ') is not found in Object: ' + self.name)

    def add_component(self, component_name, *args, **kwargs):
        new_component = component_name(self, *args, **kwargs)
        self.component_list.append(new_component)
