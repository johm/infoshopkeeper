from popups.members import AddMemberPopup


def GenerateOnPress(frame_object,label):
    return lambda event : add_member(frame_object,event,label)



def add_member(frame_object,event,label):
    win = AddMemberPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



