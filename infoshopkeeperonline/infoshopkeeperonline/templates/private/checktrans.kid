<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Red Emma's Store</title>
</head>
<body>

<table>
<tr py:for="t in transactions">
<td>${t.date}</td>
<td>${t.action}</td>
<td>${t.info}</td>
<td>${t.amount}</td>
</tr>
</table>


  <!-- End of getting_started -->
</body>
</html>
