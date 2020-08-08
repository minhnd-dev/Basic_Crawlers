import scrapy
import json 

OUTPUT_DIRECTORY =  "../../OUTPUT/shopee_content.json"
class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    order_number = 0
    def start_requests(self):
        base_url = "https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.78?page="
        for i in range(1,110):
            yield scrapy.Request(url = base_url+str(i), callback=self.parse_link)
    def parse_link(self, response):
        for product in response.css("div.col-xs-2-4.shopee-search-item-result__item"):
            link = "https://shopee.vn/" + product.css("div a::attr(href)").get()
            yield scrapy.Request(url = link, callback=self.parse_product)
    def parse_product(self, response):
        product = {
            "STT": self.order_number,
            "Ten SP": response.css("div.qaNIZv span::text").get(),
            "Ten cua hang": response.css("div._3Lybjn::text").get(),
            "Gia tien": response.css("div._3n5NQx::text").get(),
            "Danh muc":[category.get()
                for category in response.xpath('//*[@class="product-detail page-product__detail"]/div[1]/div[2]/div/div/a/text()')
            ],
            "Mo ta SP":response.xpath('//*[@class="product-detail page-product__detail"]/div[2]/div[2]/div/span/text()').get(),
            "Thuong hieu": response.xpath('//*[@class="kIo6pj"]/a/text()').get()
        }
        #Lay thong them thong tin chi tiet sp: chat lieu, kho hang, gui tu,....
        product_details = {
            item.css("label::text").get() : item.css("div::text").get() for item in response.css("div.kIo6pj")
        }
        del product_details["Danh Mục"]
        del product_details["Thương hiệu"]
        
        full_content = product.copy()
        full_content.update(product_details)
        
        with open(OUTPUT_DIRECTORY, "a", encoding='utf8') as content_file:
            content_file.write(json.dumps(full_content, indent = 4,ensure_ascii=False))
        self.order_number += 1