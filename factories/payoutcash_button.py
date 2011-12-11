from popups.cashout import CashPayoutPopup


def GenerateOnPress(frame_object,label):
    return lambda event : cash_payout(frame_object,event,label)



def cash_payout(frame_object,event,label):
    win = CashPayoutPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



