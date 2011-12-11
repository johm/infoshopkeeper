from Report import Report

from objects.kind import Kind

class BestSellersReportByDate(Report):
    metadata={'name':'Best Sellers Report By Date','action':'bestsellersreportbydate'}
    do_total=False
    def query(self,args):
        begin_date=args.get('begin_date','1990-01-01')
        end_date=args.get('end_date','2030-01-01')
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
        select booktitle,count(book.id) as blah  from book,title where book.title_id=title.id and book.status='SOLD' and title.kind_id=%s and sold_when>=%s and sold_when<=ADDDATE(%s,INTERVAL 1 DAY)  group by title_id order by blah desc limit 100
        """,(args['kind'],begin_date,end_date))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results

    def format_results(self,results):
        return ["<tr><td>%s</td><td>%s</td></tr>" % (r[0],r[1])  for r in results]


    def _queryForm(self):
        val="<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select>"
        val =val+"""
                <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/>
        <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/>
        <script type='text/javascript'>
        Calendar.setup({
        inputField     :    'begin_date',   // id of the input field
        ifFormat       :    '%%Y-%%m-%%d',       // format of the input field
        showsTime      :    false,
    });
    Calendar.setup({
        inputField     :    'end_date',   // id of the input field
        ifFormat       :    '%%Y-%%m-%%d',       // format of the input field
        showsTime      :    false,
    });
        </script>
""" % (self.args.get("begin_date",""),self.args.get("end_date",""))
        return val
