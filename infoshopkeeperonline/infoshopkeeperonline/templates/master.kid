<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>


    <link rel="stylesheet" href="http://redemmas.org/css/redemmas.css" />
    <script type="text/javascript" src="http://redemmas.org/js/prototype.js"></script>
    <script type="text/javascript" src="http://redemmas.org/js/scriptaculous.js"></script>

<link rel="alternate" type="application/rss+xml" title="Event Updates" href="http://redemmas.org/feeds/events" />
<link rel="alternate" type="application/rss+xml" title="News Updates" href="http://redemmas.org/feeds/news" />
<link rel="alternate" type="application/rss+xml" title="Book Updates" href="http://redemmas.org/feeds/books" />
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
    <style type="text/css">
        #pageLogin
        {
            font-size: 10px;
            font-family: verdana;
            text-align: right;
        }
    </style>
    <style type="text/css" media="screen">
@import "http://redemmas.org/inventory/static/css/style.css";

<!--[if gte IE 5.5000]>
<script language="JavaScript" type="text/javascript">
function correctPNG() // correctly handle PNG transparency in Win IE 5.5 or higher.
   {
   for(var i=0; i<document.images.length; i++)
      {
        var img = document.images[i]
	  var imgName = img.src.toUpperCase()
	      if (imgName.substring(imgName.length-3, imgName.length) == "PNG")
	                 {
			   var imgID = (img.id) ? "id='" + img.id + "' " : ""
			    var imgClass = (img.className) ? "class='" + img.className + "' " : ""
			        var imgTitle = (img.title) ? "title='" + img.title + "' " : "title='" + img.alt + "' "
				     var imgStyle = "display:inline-block;" + img.style.cssText 
				           if (img.align == "left") imgStyle = "float:left;" + imgStyle
					          if (img.align == "right") imgStyle = "float:right;" + imgStyle
						          if (img.parentElement.href) imgStyle = "cursor:hand;" + imgStyle
							   var strNewHTML = "<span " + imgID + imgClass + imgTitle
							     + " style=\"" + "width:" + img.width + "px; height:" + img.height + "px;" + imgStyle + ";"
							            + "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader"
								            + "(src=\'" + img.src + "\', sizingMethod='scale');\"></span>" 
									     img.outerHTML = strNewHTML
									       i = i-1
									              }
      }
   }
window.attachEvent("onload", correctPNG);
</script>
<![endif]-->


<script  src="http://redemmas.org/js/browser_detect.js" type="text/javascript"></script>
<script  src="http://redemmas.org/js/redemmas.js" type="text/javascript"></script>


</style>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()" onload="stretch();makemouseovers()" onresize="stretch()">
    <div py:if="tg.config('identity.on') and not defined('logging_in')" id="pageLogin">
        <span py:if="tg.identity.anonymous">
            <a href="${tg.url('/inventory/login')}">Login</a>
        </span>
        <span py:if="not tg.identity.anonymous">
            Welcome ${tg.identity.user.display_name}.
            <a href="${tg.url('/inventory/logout')}">Logout</a>
        </span>
    </div>
    <div id="main">
<h1 id="logo"><a href="http://redemmas.org/"><img src="http://redemmas.org/img/redemmas.png" /></a></h1>
<h2 id="tagline"><img src="http://redemmas.org/img/tagline.png" /></h2>
<BR style="clear:both" />
<table id="topnav">
<tr>
<td><a class="makemouseover" href="http://redemmas.org/section/about"><img src="http://redemmas.org/img/about.png" alt="about" /></a></td>
<td><a class="makemouseover" href="http://redemmas.org/books"><img src="http://redemmas.org/img/books.png" alt="books"/></a></td>
<td><a class="makemouseover" href="http://redemmas.org/events"><img src="http://redemmas.org/img/events.png" alt="events"/></a></td>
<td><a class="makemouseover" href="http://redemmas.org/news"><img src="http://redemmas.org/img/news.png" alt="news"/></a></td>
<td><a class="makemouseover" href="http://redemmas.org/links"><img src="http://redemmas.org/img/links.png" alt="links"/></a></td>
<td><a class="makemouseover" href="http://redemmas.org/bookfair/"><img src="http://redemmas.org/img/bookfair.png" alt="bookfair"/></a></td>
<td><a class="makemouseover" href="http://redemmas.org/section/about/support"><img src="http://redemmas.org/img/support.png" alt="support"/></a></td>
</tr>
</table>

<BR style="clear:both" />


    <div id="header">&nbsp;</div>
    <h1><a href="http://redemmas.org/inventory/storefront">Search</a>  | <a href="http://redemmas.org/inventory/titles">Titles</a> | <a href="http://redemmas.org/inventory/authors">Authors</a> | <a href="http://redemmas.org/inventory/sections">Sections</a></h1>
    <div id="main_content">
    <div id="status_block" class="flash" py:if="value_of('tg_flash', None)" py:content="tg_flash"></div>

    <div py:replace="[item.text]+item[:]"/>

    <!-- End of main_content -->
    </div>

<BR style="clear:both" />
<BR style="clear:both" />
<div id="colophon">
<div id="address">800 St. Paul St. * Baltimore, MD 21202 * (410) 230-0450 * info@redemmas.org</div>
<div id="hours">Red Emma's is open Monday through Saturday from 10AM-10PM, and Sunday from 10AM-6PM.  Our weekly collective meetings are Sunday at 7PM, and are open to anyone interested in the project.</div>
</div>
<div id="bottomnav">
<ul>
<li><a href="http://redemmas.org/books">books</a></li>
<li><a href="http://redemmas.org/events">events</a></li>
<li><a href="http://redemmas.org/news">news</a></li>
<li><a href="http://redemmas.org/section/about/menu">cafe</a></li>
<li><a href="http://redemmas.org/section/store">store</a></li>
<li><a href="http://redemmas.org/links">baltimore resources</a></li>
</ul>
</div>
</div>
</body>

</html>
