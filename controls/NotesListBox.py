from wxPython.wx import *

from wrappingListBox import wrappingListBox

from components import db

class NotesListBox(wrappingListBox):
    def initialize(self,parent):
        self.parent=parent
        self.populate()

    def populate(self):
        self.conn=db.connect()
        cursor=self.conn.cursor()
        cursor.execute("SELECT * from notes order by whenEntered desc limit 100")
        rows=cursor.fetchall()
        for r in rows:
            when="%s" % (r[2])
            msg=r[0].replace("\n","\r\n")
            
            self.Append(msg)

            self.Append("-- %s, %s" % (r[1],when[5:len(when)-3]))
            self.Append("----------------------------")
            

    def addmessage(self,event):
        msg=self.parent.messageTextCtrl.GetValue()
        author=self.parent.messageAuthorTextCtrl.GetValue()

        if len(msg)>0:
            cursor=self.conn.cursor()
            cursor.execute("INSERT INTO notes VALUES(%s,%s,NOW())",(msg,author))
            self.parent.messageTextCtrl.Clear()
            self.Clear()
            self.populate()
