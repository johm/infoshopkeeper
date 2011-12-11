from factories.factory import factory

class browse(factory):
    def __init__(self):
        factory.__init__(self, ["popups.searchinventory", "SearchInventoryPopup"])
    
class add(factory):
    def __init__(self):
        factory.__init__(self, ["popups.inventory", "InventoryPopup"])
