from scrapy import signals
from itemadapter import is_item, ItemAdapter
from time import sleep

from scrapy.http import HtmlResponse


class News163ItemDownloaderMiddleware:

    def process_request(self, request, spider):

        return None
    # 4.通过中间件完成动态数据的获取
    def process_response(self, request, response, spider):
        bro = spider.bro
        if request.url in spider.modules_url:
            print("走的是解析的地址")
            bro.get(request.url)
            sleep(3)
            page_text = bro.page_source
            n_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return n_response
        else:
            return response

    def process_exception(self, request, exception, spider):

        pass
