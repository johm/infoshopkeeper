<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>
<div class="same_author" style="float:right;width:250px;">
${titlelistwidget(new_titles,listtitle="New titles",authorswidget=authorswidget)}
</div>


<h3>Search our in-store inventory</h3>
${searchform(action="http://redemmas.org/inventory/search")}

<ul>
<li><a href="http://redemmas.org/inventory/titles">Browse by Title</a></li>
<li><a href="http://redemmas.org/inventory/authors">Browse by Author</a></li>
<li><a href="http://redemmas.org/inventory/sections">Browse by Section</a></li>
</ul>
<div class="same_author" style="float:left;width:250px;">
${titlelistwidget(best_sellers,listtitle="Best Sellers",authorswidget=authorswidget)}
</div>
  <!-- End of getting_started -->
</body>
</html>
