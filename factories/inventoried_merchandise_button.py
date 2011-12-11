from popups.inventoriedmerchandise import InventoriedMerchandisePopup
from components.item_inventoried_merchandise import inventoried_merchandise

def GenerateOnPress(frame_object,label):
    return lambda event : add_inventoried_merchandise(frame_object,event,inventoried_merchandise(label,frame_object))



def add_inventoried_merchandise(frame_object,event,m_item):
    win = InventoriedMerchandisePopup(frame_object,m_item,frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



