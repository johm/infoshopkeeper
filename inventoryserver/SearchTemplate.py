#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Skeleton import Skeleton

##################################################
## MODULE CONSTANTS
try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.0.1'
__CHEETAH_versionTuple__ = (2, 0, 1, 'final', 0)
__CHEETAH_genTime__ = 1309384747.597472
__CHEETAH_genTimestamp__ = 'Wed Jun 29 17:59:07 2011'
__CHEETAH_src__ = 'SearchTemplate.html'
__CHEETAH_srcLastModified__ = 'Sat Aug 28 10:48:17 2010'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class SearchTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        Skeleton.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def pagetitle(self, **KWS):



        ## CHEETAH: generated from #def pagetitle at line 4, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''Search the inventory
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 8, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<h1>Inventory</h1>
<div class="showhide"><a  href="javascript:show_hide(\'search_form\')">Show/hide search form</a></div>
<br />
<form id="search_form" method="get" action="/search"
''')
        if not(VFFSL(SL,"empty",True)): # generated from line 13, col 1
            write('''style="visibility:hidden;display:none"
''')
        write('''>

<label class="textbox" for="title">Title</label> 
<input class="textbox" type="text" id="title" name="title" value="''')
        _v = VFFSL(SL,"title",True) # '$title' on line 19, col 67
        if _v is not None: write(_filter(_v, rawExpr='$title')) # from line 19, col 67.
        write('''" /><br />

<label class="textbox" for="author">Author</label> 
<input class="textbox" type="text" name="author" id="author" value="''')
        _v = VFFSL(SL,"author",True) # '$author' on line 22, col 69
        if _v is not None: write(_filter(_v, rawExpr='$author')) # from line 22, col 69.
        write('''" /><br />

<label class="textbox" for="author">Category</label> 
<input class="textbox" type="text" name="category" id="category" value="''')
        _v = VFFSL(SL,"category",True) # '$category' on line 25, col 73
        if _v is not None: write(_filter(_v, rawExpr='$category')) # from line 25, col 73.
        write('''" /><br />

<label class="textbox" for="publisher">Publisher</label> 
<input class="textbox" type="text" name="publisher" id="publisher" value="''')
        _v = VFFSL(SL,"publisher",True) # '$publisher' on line 28, col 75
        if _v is not None: write(_filter(_v, rawExpr='$publisher')) # from line 28, col 75.
        write('''" /><br />

<label class="textbox" for="distributor">Distributor</label> 
<input class="textbox" type="text" name="distributor" id="distributor" value="''')
        _v = VFFSL(SL,"distributor",True) # '$distributor' on line 31, col 79
        if _v is not None: write(_filter(_v, rawExpr='$distributor')) # from line 31, col 79.
        write('''" /><br />

<label class="textbox" for="owner">Owner</label> 
<input class="textbox" type="text" name="owner" id="owner" value="''')
        _v = VFFSL(SL,"owner",True) # '$owner' on line 34, col 67
        if _v is not None: write(_filter(_v, rawExpr='$owner')) # from line 34, col 67.
        write('''" /><br />


<label class="textbox" for="out_of_stock">Only return out of stock books?</label>

<fieldset id="out_of_stock">
no <input type="radio" name="out_of_stock" id="out_of_stock_no" value="no" 
''')
        if VFFSL(SL,"out_of_stock",True) == 'no': # generated from line 41, col 1
            write('''checked
''')
        write('''> 
yes<input type="radio" name="out_of_stock" id="out_of_stock_yes" value="yes"
''')
        if VFFSL(SL,"out_of_stock",True) == 'yes': # generated from line 46, col 1
            write('''checked
''')
        write('''>
</fieldset>

<br />


<label class="textbox" for="stock_less_than">This many or less in stock</label> 
<input class="textbox" type="text" name="stock_less_than" id="stock_less_than" value="''')
        _v = VFFSL(SL,"stock_less_than",True) # '$stock_less_than' on line 56, col 87
        if _v is not None: write(_filter(_v, rawExpr='$stock_less_than')) # from line 56, col 87.
        write('''" /><br />

<label class="textbox" for="stock_more_than">This many or more in stock</label> 
<input class="textbox" type="text" name="stock_more_than" id="stock_more_than" value="''')
        _v = VFFSL(SL,"stock_more_than",True) # '$stock_more_than' on line 59, col 87
        if _v is not None: write(_filter(_v, rawExpr='$stock_more_than')) # from line 59, col 87.
        write('''" /><br />

<label class="textbox" for="sold_more_than">This many or more sold</label> 
<input class="textbox" type="text" name="sold_more_than" id="sold_more_than"  value="''')
        _v = VFFSL(SL,"sold_more_than",True) # '$sold_more_than' on line 62, col 86
        if _v is not None: write(_filter(_v, rawExpr='$sold_more_than')) # from line 62, col 86.
        write('''" /><br />

<label class="textbox" for="sold_more_than">This many or less sold</label> 
<input class="textbox" type="text" name="sold_less_than" id="sold_less_than"  value="''')
        _v = VFFSL(SL,"sold_less_than",True) # '$sold_less_than' on line 65, col 86
        if _v is not None: write(_filter(_v, rawExpr='$sold_less_than')) # from line 65, col 86.
        write('''" /><br />

<label class="textbox" for="tag">Tag</label> 
<input class="textbox" type="text" id="tag" name="tag" value="''')
        _v = VFFSL(SL,"tag",True) # '$tag' on line 68, col 63
        if _v is not None: write(_filter(_v, rawExpr='$tag')) # from line 68, col 63.
        write('''" /><br />

<label class="textbox" for="kind">Kind</label> 

<select class="textbox" id="kind" name="kind">
''')
        for k in VFFSL(SL,"kinds",True): # generated from line 73, col 1
            write("""<option value='""")
            _v = VFFSL(SL,"k.id",True) # '$k.id' on line 74, col 16
            if _v is not None: write(_filter(_v, rawExpr='$k.id')) # from line 74, col 16.
            write("""' 
""")
            if "%s" %(VFFSL(SL,"k.id",True))==VFFSL(SL,"kind",True): # generated from line 75, col 1
                write('''selected="true" 
''')
            write('''>''')
            _v = VFFSL(SL,"k.kindName",True) # '$k.kindName' on line 78, col 2
            if _v is not None: write(_filter(_v, rawExpr='$k.kindName')) # from line 78, col 2.
            write('''</option>
''')
        write('''</select><br />



<input class="submit" type="submit">

<br />
</form>
<form action="/titlelist" method="get" >
<table class="sortable" id="unique_id" >
<tbody>
  <tr>
    <th>Mark</th>
    <th>Title</th>
    <th>Author</th>
    <th>Category</th>
    <th>Copies in Stock</th>
    <th>Copies Sold</th>
    <th>Distributor</th>
    <th>Publisher</th>
    <th>First Inventoried</th>
    <th>Latest Inventoried</th>
    <th>First Sold</th>
    <th>Last Sold</th>
  </tr>
''')
        for t in VFFSL(SL,"titles",True): # generated from line 105, col 1
            write('''  <tr>
    <td><input type="checkbox" name="titles" value="''')
            _v = VFFSL(SL,"t.id",True) # '$t.id' on line 107, col 53
            if _v is not None: write(_filter(_v, rawExpr='$t.id')) # from line 107, col 53.
            write('''" /></td>
    <td><a  href="/titleedit?id=''')
            _v = VFFSL(SL,"t.id",True) # '$t.id' on line 108, col 33
            if _v is not None: write(_filter(_v, rawExpr='$t.id')) # from line 108, col 33.
            write('''">''')
            _v = VFN(VFFSL(SL,"t",True),"safe",False)('booktitle') # "$t.safe('booktitle')" on line 108, col 40
            if _v is not None: write(_filter(_v, rawExpr="$t.safe('booktitle')")) # from line 108, col 40.
            write('''</a></td>
    <td>''')
            _v = VFFSL(SL,"t.authors_as_string",True) # '$t.authors_as_string' on line 109, col 9
            if _v is not None: write(_filter(_v, rawExpr='$t.authors_as_string')) # from line 109, col 9.
            write('''</td>
    <td>''')
            _v = VFFSL(SL,"t.categories_as_string",True) # '$t.categories_as_string' on line 110, col 9
            if _v is not None: write(_filter(_v, rawExpr='$t.categories_as_string')) # from line 110, col 9.
            write('''</td>
    <td>''')
            _v = VFN(VFFSL(SL,"t",True),"copies_in_status",False)("STOCK") # '${t.copies_in_status("STOCK")}' on line 111, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.copies_in_status("STOCK")}')) # from line 111, col 9.
            write('''</td>
    <td>''')
            _v = VFN(VFFSL(SL,"t",True),"copies_in_status",False)("SOLD") # '${t.copies_in_status("SOLD")}' on line 112, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.copies_in_status("SOLD")}')) # from line 112, col 9.
            write('''</td>
    <td>''')
            _v = VFN(VFFSL(SL,"t",True),"distributors_as_string",False)() # '${t.distributors_as_string()}' on line 113, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.distributors_as_string()}')) # from line 113, col 9.
            write('''</td>
    <td>''')
            _v = VFN(VFFSL(SL,"t",True),"safe",False)('publisher') # "${t.safe('publisher')}" on line 114, col 9
            if _v is not None: write(_filter(_v, rawExpr="${t.safe('publisher')}")) # from line 114, col 9.
            write('''</td>
    <td>''')
            _v = VFFSL(SL,"t.first_book_inventoried.inventoried_when",True) # '${t.first_book_inventoried.inventoried_when}' on line 115, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.first_book_inventoried.inventoried_when}')) # from line 115, col 9.
            write('''</td>
    <td>''')
            _v = VFFSL(SL,"t.last_book_inventoried.inventoried_when",True) # '${t.last_book_inventoried.inventoried_when}' on line 116, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.last_book_inventoried.inventoried_when}')) # from line 116, col 9.
            write('''</td>
    <td>''')
            _v = VFFSL(SL,"t.first_book_sold.sold_when",True) # '${t.first_book_sold.sold_when}' on line 117, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.first_book_sold.sold_when}')) # from line 117, col 9.
            write('''</td>
    <td>''')
            _v = VFFSL(SL,"t.last_book_sold.sold_when",True) # '${t.last_book_sold.sold_when}' on line 118, col 9
            if _v is not None: write(_filter(_v, rawExpr='${t.last_book_sold.sold_when}')) # from line 118, col 9.
            write('''</td>
  </tr>
''')
        write('''</tbody>
</table>
<br />
<input class="submit"  name="list" type="submit" value="get marked titles" /><br /><br />
<input class="submit"  name="delete" onclick="return confirm(\'Are you sure?\');" type="submit" value="delete marked titles" />
</form>

''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''

''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_SearchTemplate= 'writeBody'

## END CLASS DEFINITION

if not hasattr(SearchTemplate, '_initCheetahAttributes'):
    templateAPIClass = getattr(SearchTemplate, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(SearchTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=SearchTemplate()).run()

