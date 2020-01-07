
from scrapy import Request, Spider
import re
import redis


class MySpider(Spider):
    name = "spider_wlwz"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
               "Accept-Language": "zh-CN,zh;q=0.9"}

    start_url = "http://www.jsunion.net/Article/ShowClass2.asp?ClassID=18&SpecialID=0&page="
    detail = "http://www.jsunion.net/Article/ShowArticle2.asp?ArticleID="
    page = "&ArticlePage="
    all_episodes = []
    url_pattern = re.compile(
        '.*?ArticleID=(\d+).*?')
    p = re.compile(' 第(\w+)回 (.*?)')

    all_content = {}

    def __init__(self):
        #初始化redis连接
        self.db = redis.Redis(host='localhost', port=6379,
                              password="", decode_responses=True)

    def start_requests(self):
        for i in range(1, 6):
            yield Request(self.start_url+str(i), callback=self.parse)

    def parse(self, response):
        content = response.xpath(
            '//td[@height="200" and @valign="top"]/a').extract()
        for i in content:
            if("武林外传" in i):
                result = re.findall(self.url_pattern, i)
                yield Request(self.detail+result[0], callback=self.get_detail)

    def get_detail(self, response):
        url = response.url
        text = response.xpath(
            '//td[@height="200" and @valign="top"]/text()').extract()
        title = ""
        for i in text:
            tt = re.findall(self.p, i)
            if(len(tt) > 0):
                title = i
        page_content = response.xpath(
            "//p[@align='center']//a").extract()  # 长度为下面翻页数字 也就是页码数目
        for i in range(1, len(page_content)+1):
            request = Request(url+self.page+str(i), callback=self.get_text)
            request.meta['title'] = title
            request.meta['num'] = str(i)
            yield request

    def get_text(self, response):
        title = response.meta['title']
        num = response.meta['num']
        text = response.xpath(
            '//td[@height="200" and @valign="top"]/text()').extract()
        stt="\n"
        print(title)
        stt = stt.join(text)
        stt = num + stt
        self.db.lpush(title,stt)

#    if(title in self.all_content):
#         self.all_content[title] += stt
#     else:
#         self.all_content[title] = stt
