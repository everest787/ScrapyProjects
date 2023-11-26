import scrapy
from scrapy_splash import SplashRequest


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]

    def start_requests(self):
        keywords = ["Software"]
        location = "Canada"

        baseURL = f"https://www.linkedin.com/jobs/search?keywords={keywords[0]}&location={location}&f_TPR=r86400"
    
        url = baseURL
        yield SplashRequest(url, self.parse, args={'wait': 0.5})
    
    def parse(self, response):
        for jobs in response.css(".base-card"):
            urls = jobs.css("a::attr(href)").getall()

            yield {
                "links": urls,
                #"title": jobs.xpath(".//*[contains(@class, 'base-search-card__title')]").get(),
                #"company": jobs.xpath(".//*[contains(@class, 'base-search-card__subtitle')]").get(),
                #"location": jobs.xpath(".//*[contains(@class, 'job-search-card__location')]").get(),
            }
