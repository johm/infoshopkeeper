<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>

<h1>Titles <span py:if="the_letter!=None">${the_letter}</span></h1>

<div py:if="the_titles!=False">
${titlelistwidget(the_titles,listtitle="",authorswidget=authorswidget)}
</div>

<ul py:if="the_titles==False">
<li py:for="l in alphabet">
<a href="http://redemmas.org/inventory/titles/${l}">${l}</a>
</li>
<li><a href="http://redemmas.org/inventory/titles/0-9">0-9</a></li>
</ul>




  <!-- End of getting_started -->
</body>
</html>
