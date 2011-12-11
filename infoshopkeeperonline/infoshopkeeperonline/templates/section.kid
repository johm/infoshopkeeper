<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store: Browse by sections</title>
</head>
<body>

<h1>${the_section.sectionName}</h1>
<p>
${the_section.sectionDescription}
</p>

${titlelistwidget(in_this_section,listtitle=the_section.sectionName,authorswidget=authorswidget,editlink="/inventory/private/section/%s" % the_section.id)}


</body>
</html>
