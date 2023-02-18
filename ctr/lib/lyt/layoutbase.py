
class LayoutBase:
    layoutType: str = None
    layoutName: str = None
    
    children: list['LayoutBase'] = []
    parent: 'LayoutBase' = None

    rootPane: 'LayoutBase' = None

    def add_child(self, child):
        self.children.append(child)
    
    