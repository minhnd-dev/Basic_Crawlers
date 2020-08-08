# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.headless = True
options.add_argument("window-size=1920,1080")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
PATH = "C:\\Users\\Admin\\Documents\\Học tập\\6.Lab\\ShopeeCrawler\\ShopeeCrawler\\chromedriver.exe"
class ShopeecrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ShopeecrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

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

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
