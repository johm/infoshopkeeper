<?python 
import operator
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<script type="text/javascript" src="/static/javascript/behaviour.js" />
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
<style type="text/css">
body {font-size:11px;}
h1 {font-size:14px;}
h2 {font-size:12px;}
ul.inline li {float:left}
ul.inline li  {font-size:10px;width:150px;overflow:hidden;}
.copylist {float:right;}
</style>

</head>
<body>
<script type="text/javascript">
var xmlhttp;

function persistsection(section,activate)
{
xmlhttp=null;
// code for Mozilla, etc.
if (window.XMLHttpRequest)
  {
  xmlhttp=new XMLHttpRequest();
  }
// code for IE
else if (window.ActiveXObject)
  {
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
if (xmlhttp!=null)
  {
   xmlhttp.open("GET","/private/persistsection?section="+section+";activate="+activate,true);
  xmlhttp.send(null);
  }

}



var myrules = {
		'.titlepersistenceform input' : function(element){
			element.onclick = function(){
				persistsection(this.value,this.checked);
				for (i=0;i&lt;document.titleform.sections.length;i++){
					s=document.titleform.sections[i];
					if (s.value==this.value){
						s.checked=this.checked;
						}
						 	
					
				}	
			}
		}
	};
	
	Behaviour.register(myrules);
</script>
<div style="float:right;border:1px solid black;">${searchform(action="/private/reinventory",value=searchvalues)}</div>

<h1 class="title">${thetitle.booktitle}</h1>
<h2>Author: ${authorswidget.display(thetitle)}</h2>
<h2>Publisher: ${thetitle.publisher}</h2>
<h2>Ordered from: 
<ul style="display:inline">
<li style="display:inline" py:for="distributor in set([b.distributor.upper() for b in thetitle.books])">${distributor} </li>
</ul>
</h2>
<div class="copylist">
<h3>Copies:</h3>
<ul>
<li py:for="book in sorted(thetitle.books,key=lambda x:x.status,reverse=True)">
$$${book.listprice} ${book.status} 
<span py:if="book.status=='STOCK'">
${["Confirmed %s " % t.when_tagged for t in book.tags if t.tagkey=='confirmation' and t.tagcategory.description=='inventory']}
<a py:if="len([t for t in book.tags if t.tagkey=='confirmation' and t.tagcategory.description=='inventory' and '%s' % t.when_tagged==today])==0"  href="/private/confirm?book=${book.id};title=${thetitle.id}">CONFIRM</a></span>
</li>
</ul>
</div>
<div class="titleform">${titleform(action="/private/edit_title",value=dict(title_id=thetitle.id,preferred_distributor=thetitle.get_unique_tag(category='distribution',key="preferred"),sections=sections))}	
</div>
<div class="titlepersistenceform">${titlepersistenceform(action="/private/persist",value=dict(sections=[]))}	
</div>
</body>
</html>
