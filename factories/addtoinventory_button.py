from popups.inventory import InventoryPopup


def GenerateOnPress(frame_object,label):
    return lambda event : inventory_merchandise(frame_object,event,label)



def inventory_merchandise(frame_object,event,label):
    win = InventoryPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



