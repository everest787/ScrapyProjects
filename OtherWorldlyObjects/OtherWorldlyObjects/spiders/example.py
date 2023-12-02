import scrapy
from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def start_requests(self):
        baseURL = "https://www.example.com"
        url = baseURL

        yield SeleniumRequest(url, self.parse, wait_time=10)

    def parse(self, response):
        pass