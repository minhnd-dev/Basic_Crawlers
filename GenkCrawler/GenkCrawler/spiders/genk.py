import scrapy
import json

OUTPUT_DIRECTORY = "../../OUTPUT/genk_content.json"
class GenkSpider(scrapy.Spider):
    name = 'genk'
    order_number = 0
    def start_requests(self):
        base_url = "https://genk.vn/ajax-home/page-{}/20200727153712189__20200725211234502__20200714155940046__20200728113853189__20200728150434174.chn"
        for i in range(1000):
            yield scrapy.Request(url = base_url.format(i), callback = self.parse_link)
    def parse_link(self, response):
        for article in response.css("h4.knswli-title"):
            link = "https://genk.vn"+article.css("a::attr(href)").get()
            yield scrapy.Request(url = link, callback = self.parse_content)
    def parse_content(self, response):
        article = {
            "STT":        self.order_number,
            "Duong link": response.url,
            "Tieu_de:":   response.css("h1.kbwc-title.clearfix::text").get().strip(),
            "Tom_tat":    response.css("h2.knc-sapo::text").get().strip(),
            "Noi_dung":   "\n".join(paragraphs.get().strip() 
                                for paragraphs in response.css("div.knc-content p ::text")),
            "Thoi_gian":  response.css("span.kbwcm-time::attr(title)").get(),
            "Nguon":      response.css("span.kbwcm-source a::text").get(),
            "Tag_gia":    response.css("span.kbwcm-author::text").get(),
            "Tags":       [tag.css("a strong::text").get() for tag in response.css("li.kli")],
            "Chuyen_muc": response.css("li.gbrcwli.active strong a span::text").get()
        }
        self.order_number+=1
        with open(OUTPUT_DIRECTORY, "a", encoding='utf8') as content_file:
            content_file.write(json.dumps(article, indent = 4,ensure_ascii=False))
