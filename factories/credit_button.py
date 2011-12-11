from components.item_merchandise import merchandise
from popups.credit import CreditPopup

def GenerateOnPress(frame_object,label):
    return lambda event : add_credit(frame_object,event,merchandise(label,taxable=0))

def add_credit(frame_object,event,m_item):
    win = CreditPopup(frame_object,m_item)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()


