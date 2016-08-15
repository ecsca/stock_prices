import scrapy

class stockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["naver.com"]
    start_urls = [
            "http://finance.naver.com/item/main.nhn?code=002900"
            ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
