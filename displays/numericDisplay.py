from string import rjust

class numberbox:
    
    def __init__(self,numberdisplay):
        self.value=0
        self.width=20
        self.value_as_string= "0" 
        self.numberdisplay=numberdisplay
        self.numberdisplay.SetValue(rjust(self.value_as_string,self.width))
        self.decimal=0    
        self.decimal_place=0
    
    def decimal_point(self):
        if not(self.decimal):
            self.decimal=1
            self.value_as_string = self.value_as_string + "."        
            self.numberdisplay.SetValue(rjust(self.value_as_string,self.width))
        
    def number_clear(self):
        self.decimal=0
        self.decimal_place=0
        self.value=0
        self.value_as_string= "0" 
        self.numberdisplay.SetValue(rjust(self.value_as_string,self.width))
        
        
    def number_push(self,c):
        if self.decimal:
            if self.decimal_place < 2:    
                self.value_as_string= self.value_as_string+c
                self.value=float(self.value_as_string)
                self.decimal_place = self.decimal_place + 1
        else:
            if not(self.value == 0 and c == "0" ):     
                if self.value==0:
                    self.value_as_string=c
                else:
                    self.value_as_string = self.value_as_string+c
                self.value=float(self.value_as_string)
        
        self.numberdisplay.SetValue(rjust(self.value_as_string,self.width))