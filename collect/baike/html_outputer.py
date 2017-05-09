class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)


    def output_html(self):
        fout = open("output.html",'w')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            print(data['title'],data['url'],data['summary'])
            fout.write("<tr>")
            try:
                fout.write("<td>" + data['title'] + "</td>")
                fout.write("<td>" + data['url'] + "</td>")
                fout.write("<td>" + data['summary'] + "</td>")
            except:
                continue
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()