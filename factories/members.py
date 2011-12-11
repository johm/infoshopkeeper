from factories.factory import factory

class add(factory):
    def __init__(self):
        factory.__init__(self, ["popups.members", "AddMemberPopup"])

class browse(factory):
    def __init__(self):
        factory.__init__(self, ["popups.members", "ShowMembersPopup"])
    
