class Component_Manager:
    def __init__(self, game_object):
        self.game_object = game_object

    def get_component(self, component_name):
        return self.game_object.get_component(component_name)
