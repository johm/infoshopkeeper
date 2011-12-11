<div xmlns:py="http://purl.org/kid/ns#" class="titlelist">
  <h3 >${listtitle}</h3>
  <ul>
    <li py:for="title in value">
      <span py:if="len(title.books)>0">
        <a href="/title/${title.id}">${title.booktitle}</a>
	by 
	${authorswidget.display(title)}
	$$${title.highest_price_book().listprice}
      </span>
    </li>
  </ul>
</div>