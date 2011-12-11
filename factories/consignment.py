from factories.factory import factory

class pay(factory):
    def __init__(self):
        factory.__init__(self, ["popups.consignment", "ConsignmentPopup"] )

