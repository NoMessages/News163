import scrapy
from selenium import webdriver
from News163Item.items import News163ItemItem

# pip install pywin32
# pip install scrapy

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    modules_url = []
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='D:\PY\chromedriver.exe')
    # 1.解析网址
    def parse(self, response):
        page_text = response.text
        li_list = response.xpath('//div[@class="index_head"]/div[2]/div/ul/li/a/@href').extract()

        page_index = [2,3,5,6]
        for index in page_index:
            print(li_list[index])
            news_uri = li_list[index]
            self.modules_url.append(news_uri)

        for news_uri in self.modules_url:
            yield scrapy.Request(news_uri, callback=self.parse_news)
    # 2.解析详情页
    def parse_news(self, response):

        # 获取所有的a标签内容
        all_news_url = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div/div/div[1]/h3/a/@href').extract()
        titles = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div/div/div[1]/h3/a/text()').extract()
        for index,news_detail_url in enumerate(all_news_url):
            title = titles[index]
            item = News163ItemItem()
            item['title'] = title
            yield scrapy.Request(news_detail_url, callback=self.parse_detail, meta={'item': item})
    # 3.通过中间件处理数据
    # 4.开启下载DOWNLOAD
    # 5.处理返回的数据
    def parse_detail(self, response):
        content = response.xpath('//*[@id="content"]/div[2]/p/text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()