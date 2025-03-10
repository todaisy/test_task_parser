from celery import Celery
from parser import parser_html, parser_xml

app = Celery('tasks', broker='redis://localhost:6379/0')


class HtmlParserTask(app.Task):
    name = 'html_parser'

    def run_html(self, url):
        links = parser_html(url)

        for link in links:
            app.send_task('xml_parser', args=(link,))


class XmlParserTask(app.Task):
    name = 'xml_parser'

    def run_xml(self, url):
        parser_xml(url)


app.register_task(HtmlParserTask())
app.register_task(XmlParserTask())


if __name__ == '__main__':
    HtmlParserTask().apply_async(args=('https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1',))
    HtmlParserTask().apply_async(args=('https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2',))


# celery -A main worker --loglevel=info
