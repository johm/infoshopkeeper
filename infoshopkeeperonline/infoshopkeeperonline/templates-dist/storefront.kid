<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>

<h3>Search our in-store inventory</h3>
${searchform(action="/search")}

<ul>
<li><a href="/titles">Browse by Title</a></li>
<li><a href="/authors">Browse by Author</a></li>
</ul>

  <!-- End of getting_started -->
</body>
</html>
