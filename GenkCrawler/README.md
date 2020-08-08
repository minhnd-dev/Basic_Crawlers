# Giới thiệu
Đây là một spider đơn giản sử dụng [Scrapy](https://scrapy.org/) để lấy dữ liệu text từ hơn 10.000 bài báo từ trang báo [Genk](www.genk.vn). 
# Những việc đã làm và giải thích mã nguồn
### Lấy link các bài báo  
Đầu tiên, em vào trang của của [Genk](https://genk.vn) để lấy link của các bài báo. Tuy nhiên, trang web này không có nút "Xem thêm" để lấy link sang trang tiếp theo mà trang này tự động tải thêm dữ liệu đến vô hạn. Em phát hiện ra mỗi khi kéo đến cuối trang, trang web sẽ gửi request đến [địa chỉ](https://genk.vn/ajax-home/page-2/20200727153712189__20200725211234502__20200714155940046__20200728113853189__20200728150434174.chn) này. Trang web này chứa đường dẫn tới các bài báo sẽ xuất hiện sau khi kéo đến cuối trang. Như vậy, em chỉ cần tạo vòng lặp thay thế số page trong địa chỉ kia là có thể lấy được rất nhiều link dẫn đến các bài báo khác nhau, trong bài này, em lấy 1000 link.
```
def start_requests(self):
        base_url = "https://genk.vn/ajax-home/page-{}/20200727153712189__20200725211234502__20200714155940046__20200728113853189__20200728150434174.chn"
        for i in range(1000):
            yield scrapy.Request(url = base_url.format(i), callback = self.parse_link)
```
### Lấy dữ liệu ra từ mỗi bài báo.  
Dữ liệu thu được từ bài báo sẽ được lưu trong một từ điển sau đó được ghi lại trong file ```OUTPUT/genk_content.txt```
```
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
```
# Kết quả thu được  
  - Số lượng bài báo lấy được: 12937 bài báo  
  - Dữ liệu thu được: Đường link bài báo, tiêu đề, tóm tắt, nội dung, thời gian, nguồn báo, tác giả, tags, chuyên mục  
  - Tốc độ crawl trung bình: ~2500 bài/phút  