import scrapy
import json
class WebsosanhSpider(scrapy.Spider):
    name = 'websosanh'
    start_urls = ['https://websosanh.vn/dien-thoai-iphone-8-256gb/1382199930/so-sanh.htm']
    def parse(self, response):
        product_id = "1382199930"
        base_url = "https://websosanh.vn/Compare/GetCompareMerchantBox?rootProductId={}&regionId=0&pageIndex={}&sortType=1&pageSize=10"
        # for i in range(1,2):
        real_url = base_url.format(product_id, 1)
        yield scrapy.Request(url = base_url.format(product_id,1), callback=self.parse_xyz)
    def parse_xyz(self, response):
        str = response.text
        with open("test_data.json", "a", encoding="utf8") as f:
            f.write(json.dumps(str, indent = 4, ensure_ascii=False))
