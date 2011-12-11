<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>


</head>
<body>
<div style="float:right;width:250px;">
${titlelistwidget(same_author,listtitle="By the same author(s)",authorswidget=authorswidget)}
</div>
<h1 class="title">${thetitle.booktitle}</h1>
<h2>by ${authorswidget.display(thetitle)}</h2>
<h2>Red Emma's Price: $$${thetitle.highest_price_book().listprice}</h2>
<form action="/add_to_cart"><input type="hidden" name="title_id" value="${thetitle.id}" /><input type="submit" value="Add to cart"/></form>
<h3>Rate this book</h3>
<ul class="ratings">
<span py:if="len(thetitle.ratings)==0">No ratings for this book yet.</span>
<li py:for="rating in thetitle.ratings">
<ul class="rating fourstar">
	<li class="one"><a href="#" title="1 Star">1</a></li>
	<li class="two"><a href="#" title="2 Stars">2</a></li>
	<li class="three"><a href="#" title="3 Stars">3</a></li>
	<li class="four"><a href="#" title="4 Stars">4</a></li>
	<li class="five"><a href="#" title="5 Stars">5</a></li>
</ul>
${rating.rater} gave this book a ${rating.score}/5
<div>${rating.comments}</div>
</li>
</ul>
${ratingsform(action="/submit_rating",update="ratings",target_dom="ratings",before='getElement(\'loading\').innerHTML=\'Submitting...\';',
       on_complete='getElement(\'loading\'  ).innerHTML=\'Rating submitted!\';', value=dict(title=thetitle.id))}
<span id="loading"></span>




  <!-- End of getting_started -->
</body>
</html>
