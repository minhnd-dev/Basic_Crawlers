import scrapy
import json
OUTPUT = "../../OUTPUT/tiki_data.txt"
class TikiSpider(scrapy.Spider):
    name = 'tiki'
    start_urls = ['https://www.tiki.vn/']
    order_number = 0
    def parse(self, response):
        for category in response.css("ul.Navigation__Wrapper-knnw0g-0.jJSxyD li"):
            url = category.css("a::attr(href)").get()
            yield scrapy.Request(url=url, callback = self.parse_product_lists)

    def parse_product_lists(self, response):
        if response.status == 200:
            for product in response.css("div.product-box-list div"):
                url = product.css("a::attr(href)").get()
                if isinstance(url, str):
                    yield scrapy.Request(url="https://tiki.vn" + url, callback = self.parse_product)
            next_url = response.css("a.next::attr(href)").get()
            if isinstance(next_url, str):
                yield scrapy.Request(url="https://tiki.vn" + next_url, callback=self.parse_product_lists)
    def parse_product(self, response):
        if response.status == 200:
            product_detail = {
                "STT":self.order_number,
                "URL":response.url,
                "Ten SP" : response.css("h1.title ::text").get(),
                "Gia tien" : ' '.join(response.css("p.price ::text").getall()),
                "Cua hang": response.css("div.seller-info div a::text").get(),
                "Chuyen muc":  response.css("div.breadcrumb a::text").getall()[1:],
                "Mo ta SP":  '\n'.join(response.css("div.group.border-top ul ::text").getall()),
                "Chi tiet SP": {
                    info.css("td ::text").get() : info.css("td:nth-child(2) ::text").get()
                        for info in response.css("div.content.has-table table tbody tr")
                }
            }
            with open(OUTPUT, "a", encoding="utf8") as f:
                f.write(json.dumps(product_detail, indent = 4, ensure_ascii=False))
            self.order_number += 1