from celery import Celery
from parser import parser_html, parser_xml

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.update(
    task_always_eager=False,
    task_eager_propagates=True
)


class HtmlParserTask(app.Task):
    name = 'html_parser'

    def run(self, url):
        links = parser_html(url)

        for link in links:
            app.send_task('xml_parser', args=[link])  # for redis, asynchronous
            #  app.tasks['xml_parser'].apply(args=[link])  # for task_always_eager=True, synchronous


class XmlParserTask(app.Task):
    name = 'xml_parser'

    def run(self, url):
        parser_xml(url)


app.register_task(HtmlParserTask())
app.register_task(XmlParserTask())


if __name__ == '__main__':
    urls = [
        'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1',
        'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2'
    ]
    for url in urls:
        app.tasks['html_parser'].delay(url)

# celery -A main worker --loglevel=info
