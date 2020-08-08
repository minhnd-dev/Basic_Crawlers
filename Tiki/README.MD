# Giới thiệu
Đây là một spider đơn giản sử dụng [Scrapy](https://scrapy.org/) để thu thập dữ liệu text từ hơn 5.000 sản phẩm từ trang thương mại điện tử [Tiki](www.tiki.vn). 
# Những việc đã làm và giải thích mã nguồn
### Lấy link các sản phẩm
Trang web tiki cấm bot crawl dữ liệu từ trang này nên việc đầu tiên là thay đổi user agent bằng cách thêm dòng code trong file ```settings.py``` 
```
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT =  "Mozilla/5.0" 
```
Sau khi đổi user agent thì việc crawl dữ liệu từ trang này không quá khó khăn.
Đầu tiên, em lấy link danh mục các sản phẩm
```
def parse(self, response):
        for category in response.css("ul.Navigation__Wrapper-knnw0g-0.jJSxyD li"):
            url = category.css("a::attr(href)").get()
            yield scrapy.Request(url=url, callback = self.parse_product_lists)
```
Trang danh mục sản phẩm chứa đường dẫn tới các sản phẩm nằm trong danh mục đó. Nếu danh mục có quá nhiều sản phẩm, các sản phẩm được chia ra các trang, mỗi trang chứa khoảng vài chục sản phẩm. Trong đoạn code dưới đấy, em lấy link tất cả sản phẩm có trong trang, sau đó tìm đường dẫn tới trang tiếp theo (nếu có).
```
def parse_product_lists(self, response):
        if response.status == 200:
            # Lấy link các sản phẩm trong danh mục
            for product in response.css("div.product-box-list div"):
                url = product.css("a::attr(href)").get()
                if isinstance(url, str):
                    yield scrapy.Request(url="https://tiki.vn" + url, callback = self.parse_product)
            # Sang trang tiếp theo của danh mục đó (nếu có)
            next_url = response.css("a.next::attr(href)").get()
            if isinstance(next_url, str):
                yield scrapy.Request(url="https://tiki.vn" + next_url, callback=self.parse_product_lists)
```
### Lấy dữ liệu sản phẩm
Dữ liệu thu được từ mỗi sản phẩm sẽ được lưu trong một dictionary rồi được ghi vào file ```OUTPUT/tiki_data.txt```
```
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
```

# Kết quả thu được  
Sau khi chạy crawler một lúc rồi tắt đi, đây là kết quả em thu được:
  - Số lượng sản phẩm thu được 5993 sản phẩm
  - Dữ liệu thu được: Đường dẫn sản phẩm, tên, giá tiền, cửa hàng, chuyên mục, mô tả sản phẩm, chi tiết sản phẩm
  - Tốc độ crawl trung bình: ~1200 bài/phút  