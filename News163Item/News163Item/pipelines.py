# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class News163ItemPipeline:
    fp = None

    def open_spider(self, spider):
        print("开始爬虫")
        # 需要使用全局变量赋值
        self.fp = open('./news163item.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 3. 解析管道数据
        title = item['title']
        content = item['content']

        content = title + "\n" + content
        self.fp.write(content)
        # 4.开启管道
        return item

    def close_spider(self, spider):
        print("结束爬虫")
        self.fp.close()
