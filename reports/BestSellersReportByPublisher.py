from Report import Report

from objects.kind import Kind

class BestSellersReportByPublisher(Report):
    metadata={'name':'Best Sellers Report By Publisher','action':'bestsellersreportbypublisher'}
    do_total=False
    def query(self,args):
        which_publisher=args.get('publisher','')
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
        select booktitle,count(book.id) as blah  from book,title where book.title_id=title.id and book.status='SOLD' and title.kind_id=%s and title.publisher LIKE %s group by title_id order by blah desc limit 100
        """,(args['kind'],"%"+which_publisher+"%"))
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
                <label class='textbox' for='publisher'>Publisher</label><input type='text' class='textbox' name='publisher' id='publisher' value='%s'/>
       
""" % (self.args.get("publisher",""))
        return val
