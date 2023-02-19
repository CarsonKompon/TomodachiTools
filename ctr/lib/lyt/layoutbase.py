from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.usd1 import Usd1

class LayoutBase:
    type: str = None
    name: str = None
    
    children: list['LayoutBase'] = []
    parent: 'LayoutBase' = None

    rootPane: 'LayoutBase' = None

    userData: list[Usd1] = []

    def __init__(self):
        self.children = []
        self.userData = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def add_user_data(self, user_data):
        self.userData.append(user_data)

    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("type", self.type)
        j.add("name", self.name)
        j.add("children", self.children)
        
        if self.parent is not None:
            j.add("parent", self.parent.name)
        else:
            j.add("parent", None)

        j.add("rootPane", self.rootPane)
        j.add("userData", self.userData)
        return j.serialize()
