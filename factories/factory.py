class factory:
    def __init__(self, classes = None, additional = False):
	self.additional = additional
	self.load = classes
    
    def GenerateOnPress(self, frame_object, label):
        if self.additional != False:
  	    return lambda event: self.makeWindow(frame_object, event, label, self.additional)
	else: 
  	    return lambda event: self.makeWindow(frame_object, event, label)

    def makeWindow(self, frame_object, event, label, m_item = None):
	classToLoad = __import__(self.load[0], globals(), locals(), [self.load[1]])
	if m_item != None:
	    win = getattr(classToLoad, self.load[1])(frame_object, m_item)
	else: 
	    win = getattr(classToLoad, self.load[1])(frame_object)
	win.CenterOnScreen()
	win.ShowModal()
	win.Destroy()
        
