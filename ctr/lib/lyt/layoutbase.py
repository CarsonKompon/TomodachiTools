from ctr.lib.lyt.usd1 import Usd1

class LayoutBase:
    layoutType: str = None
    layoutName: str = None
    
    children: list['LayoutBase'] = []
    parent: 'LayoutBase' = None

    rootPane: 'LayoutBase' = None

    userData: list[Usd1] = []

    def add_child(self, child):
        self.children.append(child)
    
    def add_user_data(self, user_data):
        self.userData.append(user_data)

    def __str__(self) -> str:
        string = "{"
        string += f"layoutType: {self.layoutType},"
        string += f"layoutName: {self.layoutName},"
        if self.parent is not None:
            string += f"parent: {self.parent.name},"
        else:
            string += f"parent: None,"
        if self.rootPane is not None:
            string += f"rootPane: {self.rootPane.name},"
        else:
            string += f"rootPane: None,"

        string += f"userData: ["
        for data in self.userData:
            string += f"{data},"
        string += "],"

        string += f"children: ["
        for child in self.children:
            string += f"{child.name},"
        string += "]}"
        
        return string
    
