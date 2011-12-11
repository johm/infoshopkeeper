<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
<script type="text/javascript" src="/static/javascript/jquery.js" />
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
  $('.tag_for_reorder').click(function() {	
   var me=$(this);
   var title_id=$(this).attr("id");
   $.get("/private/reordertag",{title_id:title_id},
         function(data){
	me.after("${tg.identity.user.user_name} wants to reorder ");
   });
});
});



</script>
</head>
<body>

<ul>
<li py:for="title in titles">
<a class="title" href="javascript:void(0)">${title.booktitle}</a> by ${title.authors_as_string()}
<div style="margin-left:30px;margin-bottom:20px;">${title.copies_in_status("SOLD")} copies sold  <a href="javascript:void(0);" class="tag_for_reorder" id="${title.id}">Tag for reorder</a> <span py:for="tag in title.get_tags(category='inventory',key='reorder')"> ${tag.tagvalue} wants to reorder</span></div>
</li>
</ul>


  <!-- End of getting_started -->
</body>
</html>
