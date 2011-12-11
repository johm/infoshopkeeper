from popups.members import ShowMembersPopup


def GenerateOnPress(frame_object,label):
    return lambda event : show_members(frame_object,event,label)



def show_members(frame_object,event,label):
    win = ShowMembersPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



