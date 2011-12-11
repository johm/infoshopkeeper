<span xmlns:py="http://purl.org/kid/ns#" class="authors" py:for="i,author in enumerate(value.author)">
  <span py:if="i+1==len(value.author) and len(value.author)>1">and </span><a href="/author/${author.id}">${author.author_name}</a><span py:if="i+1!=len(value.author) and len(value.author)!=2">,</span>
</span>