from popups.consignment import ConsignmentPopup


def GenerateOnPress(frame_object,label):
    return lambda event : manage_consignment(frame_object,event,label)



def manage_consignment(frame_object,event,label):
    win = ConsignmentPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



