<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>

<h1>Authors<span py:if="the_letter!=None">${the_letter}</span></h1>


<ul py:if="the_authors!=False">
<li py:for="author in the_authors">
<a href="/author/${author.id}">${author.author_name}</a>
</li>
</ul>

<ul py:if="the_authors==False">
<li py:for="l in alphabet">
<a href="/authors/${l}">${l}</a>
</li>
</ul>




  <!-- End of getting_started -->
</body>
</html>
