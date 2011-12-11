#!/usr/bin/env python
# isbn.py
# Code for messing with ISBN numbers
# Especially stuff for converting between ISBN-10 and ISBN-13
# Copyright (C) 2007 Darren J Wilkinson
# Free GPL code
# Last updated: 14/8/2007

import sys,re

__doc__="""Code for messing with ISBN numbers. Stuff for validating ISBN-10 and
ISBN-13 numbers, computing check digits and converting from one format
to the other.

This code doesn't know anything about proper hyphenation of ISBNs. Nor does
it know anything about the real "validity" of ISBNs - it just validates on
the basis of the check-digit.

Some examples:

>>> import isbn
>>> isbn.isValid("1-58488-540-8")
True
>>> isbn.isValid("1-58488-540-5")
False
>>> isbn.isValid("978-158488-540-5")
True
>>> isbn.isI10("978-158488-540-5")
False
>>> isbn.isI13("978-158488-540-5")
True
>>> isbn.convert("1-58488-540-8")
'9781584885405'
>>> isbn.convert("978-158488-540-5")
'1584885408'
>>> isbn.isbn_strip("978-158488-540-5")
'9781584885405'
>>> isbn.check("1-58488-540")
'8'
>>> isbn.toI13("1-58488-540-8")
'9781584885405'
>>> isbn.toI13("978-158488-540-5")
'9781584885405'
>>> isbn.url("amazon","978-158488-540-5")
'http://www.amazon.com/exec/obidos/ASIN/1584885408'


The code is very simple pure python code in a single source file. Please
read the source code file (isbn.py) for further information about how
it works.

Please send bug reports, bug fixes, etc. to:
darrenjwilkinson@btinternet.com
Free GPL code, Copyright (C) 2007 Darren J Wilkinson
http://www.staff.ncl.ac.uk/d.j.wilkinson/
"""

def isbn_strip(isbn):
    """Strip whitespace, hyphens, etc. from an ISBN number and return
the result."""
    short=re.sub("\W","",isbn)
    return re.sub("\D","X",short)

def convert(isbn):
    """Convert an ISBN-10 to ISBN-13 or vice-versa."""
    short=isbn_strip(isbn)
    if (isValid(short)==False):
        raise "Invalid ISBN"
    if len(short)==10:
        stem="978"+short[:-1]
        return stem+check(stem)
    else:
        if short[:3]=="978":
            stem=short[3:-1]
            return stem+check(stem)
        else:
            raise "ISBN not convertible"

def isValid(isbn):
    """Check the validity of an ISBN. Works for either ISBN-10 or ISBN-13."""
    short=isbn_strip(isbn)
    if len(short)==10:
        return isI10(short)
    elif len(short)==13:
        return isI13(short)
    else:
        return False

def check(stem):
    """Compute the check digit for the stem of an ISBN. Works with either
    the first 9 digits of an ISBN-10 or the first 12 digits of an ISBN-13."""
    short=isbn_strip(stem)
    if len(short)==9:
        return checkI10(short)
    elif len(short)==12:
        return checkI13(short)
    else:
        return False

def checkI10(stem):
    """Computes the ISBN-10 check digit based on the first 9 digits of a
stripped ISBN-10 number."""
    chars=list(stem)
    sum=0
    digit=10
    for char in chars:
        sum+=digit*int(char)
        digit-=1
    check=11-(sum%11)
    if check==10:
        return "X"
    elif check==11:
        return "0"
    else:
        return str(check)

def isI10(isbn):
    """Checks the validity of an ISBN-10 number."""
    short=isbn_strip(isbn)
    if (len(short)!=10):
        return False
    chars=list(short)
    sum=0
    digit=10
    for char in chars:
        if (char=='X' or char=='x'):
            char="10"
        sum+=digit*int(char)
        digit-=1
    remainder=sum%11
    if remainder==0:
        return True
    else:
        return False

def checkI13(stem):
    """Compute the ISBN-13 check digit based on the first 12 digits of a
    stripped ISBN-13 number. """
    chars=list(stem)
    sum=0
    count=0
    for char in chars:
        if (count%2==0):
            sum+=int(char)
        else:
            sum+=3*int(char)
        count+=1
    check=10-(sum%10)
    if check==10:
        return "0"
    else:
        return str(check)

def isI13(isbn):
    """Checks the validity of an ISBN-13 number."""
    short=isbn_strip(isbn)
    if (len(short)!=13):
        return False
    chars=list(short)
    sum=0
    count=0
    for char in chars:
        if (count%2==0):
            sum+=int(char)
        else:
            sum+=3*int(char)
        count+=1
    remainder=sum%10
    if remainder==0:
        return True
    else:
        return False

def toI10(isbn):
    """Converts supplied ISBN (either ISBN-10 or ISBN-13) to a stripped
ISBN-10."""
    if (isValid(isbn)==False):
        raise "Invalid ISBN"
    if isI10(isbn):
        return isbn_strip(isbn)
    else:
        return convert(isbn)

def toI13(isbn):
    """Converts supplied ISBN (either ISBN-10 or ISBN-13) to a stripped
ISBN-13."""
    if (isValid(isbn)==False):
        raise "Invalid ISBN"
    if isI13(isbn):
        return isbn_strip(isbn)
    else:
        return convert(isbn)

def url(type,isbn):
    """Returns a URL for a book, corresponding to the "type" and the "isbn"
provided. This function is likely to go out-of-date quickly, and is
provided mainly as an example of a potential use-case for the module.
Currently allowed types are "google-books" (the default if the type is
not recognised), "amazon", "amazon-uk", "blackwells".
"""
    short=toI10(isbn)
    if type=="amazon":
        return "http://www.amazon.com/o/ASIN/"+short
    elif type=="amazon-uk":
        return "http://www.amazon.co.uk/o/ASIN/"+short
    elif type=="blackwells":
        return "http://bookshop.blackwell.co.uk/jsp/welcome.jsp?action=search&type=isbn&term="+short
    else:
        return "http://books.google.com/books?vid="+short




if __name__=='__main__':
    isbn="1-58488-540-8"
    # isbn="978-158488-540-5"
    print isbn
    if isValid(isbn):
        print "isbn ok"
    else:
        print "isbn BAD"
    print convert(isbn)
    print """

For help/information, do "python", "import isbn", "help(isbn)".

"""


# eof

