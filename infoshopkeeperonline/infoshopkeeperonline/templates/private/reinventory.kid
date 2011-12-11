<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>

<h3>Search our in-store inventory</h3>
${searchform(action="/private/reinventory",value=values)}

<div py:if="the_titles!=False">
<h1>Search results</h1>
<div py:if="the_titles.count()>0">
<div py:if="the_titles.count()==1">1 result found</div>
<div py:if="the_titles.count()>1">${the_titles.count()} results found</div>
${titlelistwidget(the_titles,listtitle="",authorswidget=authorswidget)}
</div>
<div py:if="the_titles.count()==0">
Sorry, couldn't find anything.
</div>
</div>


  <!-- End of getting_started -->
</body>
</html>
