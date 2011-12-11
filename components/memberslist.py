from time import time,asctime,localtime,sleep
import types,string

import amazon
from etc import amazon_license_key
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from objects.member import Member
from upc import upc2isbn


class MembersList:
    def __init__(self):
        x=1
       
    def get(self, id):
        member = Member.get(id)
        print member
        
        return member

    

    def addToMembers(self,first_name,last_name,phone,e_mail,paid):
        if paid:
            paid="true"
        else:
            paid="false"
        b=Member(first_name=first_name.encode("ascii", "backslashreplace"), 
                        last_name=last_name.encode("ascii", "backslashreplace"),
                        phone=phone,
                        e_mail=e_mail,
                        paid=paid)
        return b.id        

    def searchMembers(self,queryTerms):
        keys=queryTerms.keys()
        condition = "1=1 "
        for key, value in queryTerms.iteritems():
            condition = condition + "AND %s LIKE \'%%%s%%\'" % (key, value)
        members = Member.select(condition)
        
        results={}
        i=1
        for m in members:
            results[i]=(m.first_name.decode("unicode_escape"),
                        m.last_name.decode("unicode_escape"),
                        m.phone,
                        m.e_mail,
                        m.paid)
            i=i+1                

        return results

    
