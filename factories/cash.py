from components.item_merchandise import merchandise
from factories.factory import factory

class pitchin(factory):
    def __init__(self):
        factory.__init__(self, ["popups.cashout", "CashPitchInPopup"])

class giveout(factory):
    def __init__(self):
        factory.__init__(self, ["popups.cashout", "CashPayoutPopup"])

class deposit(factory):
    def __init__(self):
        factory.__init__(self, ["popups.cashout", "CashDepositPopup"])

class credit(factory):
    def __init__(self):
        factory.__init__(self, ["popups.credit", "CreditPopup"], merchandise("Credit", taxable=0) )
    
    
    
    
