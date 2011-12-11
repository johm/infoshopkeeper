from popups.genpdf import GenPdfPopup

def gen_pdf(frame_object,event,label):
    win = GenPdfPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()


def GenerateOnPress(frame_object,label):
    return lambda event : gen_pdf(frame_object,event,label)




