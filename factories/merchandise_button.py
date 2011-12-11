from components.item_merchandise import merchandise
from popups.merchandise import MerchandisePopup

def GenerateOnPress(frame_object,label):
    return lambda event : add_merchandise(frame_object,event,merchandise(label))

def add_merchandise(frame_object,event,m_item):
    win = MerchandisePopup(frame_object,m_item)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()


