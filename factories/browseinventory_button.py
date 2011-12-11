from popups.searchinventory import SearchInventoryPopup


def GenerateOnPress(frame_object,label):
    return lambda event : browse_inventory(frame_object,event,label)



def browse_inventory(frame_object,event,label):
    win = SearchInventoryPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



