from OpenGLEngine.Built_inClass import *


class Material:
    def __init__(self, color: Color, ambient_strength: float, specular_strength: float, shininess: int):
        self.color = color
        self.ambientStrength = math_f.clamp(ambient_strength, 0, 1)
        self.specular_strength = math_f.clamp(specular_strength, 0, 1)
        self.shininess = shininess


DefaultMaterial = Material(color=DefaultColor.white, ambient_strength=0.1, specular_strength=0.5, shininess=5)
