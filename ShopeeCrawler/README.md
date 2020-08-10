# Giới thiệu
Đây là một spider đơn giản sử dụng [Scrapy](https://scrapy.org/) và [Selenium](https://www.selenium.dev/) để thu thập dữ liệu text từ gần 1000 sản phẩm thời trang nam từ trang thương mại điện tử [Shopee](www.shopee.vn). 
# Những việc đã làm và giải thích mã nguồn
### Cài đặt Selenium
Vì trang [Shopee](www.shopee.vn) toàn bộ được chạy bằng script và dữ liệu được cập nhật khi em kéo chuột nên em không thể lấy được dữ liệu bằng cách thông thường mà phải dùng thêm [Selenium](https://www.selenium.dev/).
Em cài đặt [Selenium](https://www.selenium.dev/) vào Anaconda, sau đó tải thêm ```chromedriver.exe``` để có thể điều khiển được Chrome.
Trong ```middlewares.py```, em cài đặt một số thông số cho chrome: chạy ở chế độ headless, kích thước cửa sổ (1920x1080), không load dữ liệu ảnh
```
options = Options()
options.headless = True
options.add_argument("window-size=1920,1080")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
```
Ở bên dưới trong hàm ```process_request()``` em đã viết một số dòng lệnh để điều khiển chrome tự động load trang web, kéo chuột xuống dưới để có thể load thêm dữ liệu.
```
def process_request(self, request, spider):
        driver = webdriver.Chrome(PATH, chrome_options= options)
        driver.get(request.url)
        if "https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.78" in request.url:
            y = 2300
            x = 1
            while y <= 4800:
                driver.execute_script("window.scrollTo(0, "+str(y)+")")
                y += 1000  
                try:
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@class="row shopee-search-item-result__items"]/div[{}]/div/a/div/div[2]/div[1]/div'.format({x}))))
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")
                x+= 10
            body = driver.page_source
            abc = driver.current_url
            driver.close()
            return HtmlResponse(abc,body = body, encoding = 'utf8', request = request) 
        else: 
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "qaNIZv")))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")
            driver.execute_script("window.scrollTo(0, 1000)")
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="_2C2YFD"]/div[@class="kP-bM3"]')))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")
            body = driver.page_source
            abc = driver.current_url
            driver.close()
            return HtmlResponse(abc,body = body, encoding = 'utf8', request = request) 
```
### Lấy link sản phẩm
Em nhận thấy ở mục thời trang nam, các trang sản phẩm đều có dạng "https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.78?page=", em chỉ cần thay số đằng sau chữ "page" là sẽ tự động tải được sang trang mới nên em tạo ra vòng lặp lấy dữ liệu từ 119 trang:
```
def start_requests(self):
        base_url = "https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.78?page="
        for i in range(1,110):
            yield scrapy.Request(url = base_url+str(i), callback=self.parse_link)
``` 
Từ mỗi trang này, em lấy được link của các sản phẩm
```
def parse_link(self, response):
        for product in response.css("div.col-xs-2-4.shopee-search-item-result__item"):
            link = "https://shopee.vn/" + product.css("div a::attr(href)").get()
            yield scrapy.Request(url = link, callback=self.parse_product)
```
### Lấy dữ liệu sản phẩm
Dữ liệu thu được từ mỗi sản phẩm sẽ được lưu trong một dictionary và ghi vào file ```OUTPUT/shopee_content.json```
```
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
```

# Kết quả thu được  
Crawler này được em viết lúc đầu nhưng chạy thử thấy chậm quá nên chuyển sang tiki làm, vì vậy code vẫn chưa hoàn chỉnh và chạy vẫn còn khá chậm. Em cũng đã thử một số cách để tăng tốc độ crawl nhưng kết quả không khả quan lắm. Dưới đây là kết quả em thu được
  - Số lượng sản phẩm crawl được: 923 sản phẩm
  - Thông tin lấy được: Tên sản phẩm, giá tiền, danh mục  
  - Tốc độ crawl: ~ 20 sản phẩm/phút
