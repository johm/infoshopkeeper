<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
<script type="text/javascript" src="/static/javascript/jquery.js" />
</head>
<body>

<ul>
<li py:for="title in titles">
<a class="title" href="/inventory/private/title/${title.id}">${title.booktitle}</a> by ${title.authors_as_string()}
</li>
</ul>


  <!-- End of getting_started -->
</body>
</html>
