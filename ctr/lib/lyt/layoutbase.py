
class LayoutBase:
    layoutType: str = None
    layoutName: str = None
    
    children: list['LayoutBase'] = []
    parent: 'LayoutBase' = None

    rootPane: 'LayoutBase' = None

    def add_child(self, child):
        self.children.append(child)

    def __str__(self) -> str:
        string = "{"
        string += f"layoutType: {self.layoutType},"
        string += f"layoutName: {self.layoutName},"
        if self.parent is not None:
            string += f"parent: {self.parent.name},"
        else:
            string += f"parent: None,"
        string += f"children: ["
        for child in self.children:
            string += f"{child.name},"
        string += "]}"
        return string
    
