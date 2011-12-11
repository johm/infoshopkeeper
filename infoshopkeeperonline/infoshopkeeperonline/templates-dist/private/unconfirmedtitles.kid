<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>


<ul>
<li py:for="title in titles">
<a href="">${title.booktitle}</a>
<ul id="${title.id}" style="display:hidden">
<li py:for="b in [b for b in title.books if b.status=='STOCK']">${b.listprice}</li>
</ul>
</li>
</ul>

  <!-- End of getting_started -->
</body>
</html>
