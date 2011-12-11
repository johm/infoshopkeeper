<div xmlns:py="http://purl.org/kid/ns#" class="titlelist">
  <h3 >${listtitle} 
        <span py:if="(not tg.identity.anonymous) and 'editlink' in locals()">
	<a href="${editlink}">Edit</a>
	</span>
  </h3>

  <ul>
    <li style="clear:left;margin-bottom:10px;min-height:70px;" py:for="title in value">	
    <img src="http://covers.openlibrary.org/b/isbn/${title.isbn}-S.jpg" style="vertical-align:middle;float:left;display:inline;margin:3px;border: solid 1px #990000;"/>
    	   <span style="vertical-align:middle;" py:if="len(title.books)>0">
        <b><i><a href="http://redemmas.org/inventory/title/${title.id}">${title.booktitle}</a></i></b>
	by 
	${authorswidget.display(title)}
	$$${title.highest_price_book().listprice}
      </span>
    </li>
  </ul>
</div>