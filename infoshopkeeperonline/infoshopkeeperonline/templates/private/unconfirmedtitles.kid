<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
<script type="text/javascript" src="http://redemmas.org/js/behaviour.js" />
<script type="text/javascript" src="http://jqueryjs.googlecode.com/files/jquery-1.3.1.min.js" />
<script type="text/javascript">
function getSelText()
{
    var txt = '';
     if (window.getSelection)
    {
        txt = window.getSelection();
             }
    else if (document.getSelection)
    {
        txt = document.getSelection();
            }
    else if (document.selection)
    {
        txt = document.selection.createRange().text;
            }
    else return;
    return txt;
}

$(document).ready(function () {
  $('ul ul').hide();
  $('a.title').click(function() {
    $(this).siblings('ul').toggle('fast');
  });
  $('.confirm').click(function() {	
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"CONFIRM"},
         function(data){
			 me.parent("span").before("STOCK Confirmed in this session");
			 me.parent("span").remove();


   });
});

  $('.sold').click(function() {
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"SOLD"},
   function(data){
   me.parent("span").before("SOLD");			 
   me.parent("span").remove();
   });
});


  $('.stolen').click(function() {
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"STOLEN"},
   function(data){
   me.parent("span").before("STOLEN");			 
   me.parent("span").remove();
   });
});


  $('.returned').click(function() {
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"RETURNED"},
         function(data){
			 me.parent("span").before("RETURNED");
			 me.parent("span").remove();


   });
});

  $('.thrownout').click(function() {
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"THROWNOUT"},
         function(data){
			 me.parent("span").before("THROWNOUT");
			 me.parent("span").remove();


   });
});


  $('.lost').click(function() {
   var me=$(this);
   var book_id=$(this).parents(".book:first").attr("id");
   $.get("/private/statustag",{book_id:book_id,status:"LOST"},
         function(data){
			 me.parent("span").before("LOST");
			 me.parent("span").remove();


   });
});
});



</script>
</head>
<body>
<a href='javascript:var x=open("/private/checktrans?what="+getSelText(),"match");'>look for transactions matching selected text</a> <br />
<a href='javascript:var x=open("/private/reinventory?title="+getSelText(),"match");'>look for books matching selected text</a>

<ul>
<li py:for="title in titles">
<a class="title" href="javascript:void(0)">${title.booktitle}</a> by ${title.authors_as_string()} [<a href="/private/title/${title.id}">adjust</a>]
<ul >
${title.booktitle} <a href='javascript:var x=open("/private/checktrans?what="+getSelText(),"match");'>t's</a> <a href='javascript:var x=open("/private/reinventory?title="+getSelText(),"match");'>b's</a>
<li class="book" id="${b.id}" py:for="b in [b for b in title.books if (b.status=='STOCK' or b.status=='UNKNOWN')  and not(b.has_tag('inventory','confirmation11'))]">${b.listprice} from ${b.distributor} ${b.inventoried_when}
<span id="${b.id}options">
${b.status}
<a class="confirm" href="javascript:void(0)">CONFIRM</a> |  
<a class="sold" href="javascript:void(0)">MARK AS SOLD </a> |
<a class="stolen" href="javascript:void(0)">MARK AS STOLEN </a> |
<a class="lost" href="javascript:void(0)">MARK AS LOST </a> |
<a class="returned" href="javascript:void(0)">MARK AS RETURNED</a> |
<a class="thrownout" href="javascript:void(0)">MARK AS THROWNOUT</a> 
</span>
</li>
<li class="book" id="${b.id}" py:for="b in [b for b in title.books if b.status=='STOCK' and b.has_tag('inventory','confirmation11')]">${b.listprice} from ${b.distributor} STOCK Confirmed on ${b.get_tags(category="inventory",key="confirmation11")[0].when_tagged}</li>
<li class="book" id="${b.id}" py:for="b in [b for b in title.books if b.status!='STOCK']">${b.listprice} from ${b.distributor} ${b.status} 
<span py:if="b.status=='SOLD'">${b.sold_when}</span>
</li>
</ul>
</li>
</ul>

  <!-- End of getting_started -->
</body>
</html>
