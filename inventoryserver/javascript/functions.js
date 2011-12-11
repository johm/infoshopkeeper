
function popup(url){
	window.open(url,'newWindow','scrollbars=yes,status=no,toolbar=no');
	return void(0);
}

function popupNamed(url,name){
	window.open(url,name,'scrollbars=yes,status=no,toolbar=no');
	return void(0);
}


function show_hide(id) {
  if (document.getElementById('search_form').style.visibility=='hidden'){
    document.getElementById('search_form').style.visibility='visible';
    document.getElementById('search_form').style.display='block';
  }
 else{
    document.getElementById('search_form').style.visibility='hidden';
    document.getElementById('search_form').style.display='none';
 }
}


 
  function show_hide_column(col_no, do_show) {

    var stl;
    if (do_show) stl = 'block'
    else         stl = 'none';

    var tbl  = document.getElementById('id_of_table');
    var rows = tbl.getElementsByTagName('tr');

    for (var row=0; row<rows.length;row++) {
      var cels = rows[row].getElementsByTagName('td')
      cels[col_no].style.display=stl;
    }
  }
