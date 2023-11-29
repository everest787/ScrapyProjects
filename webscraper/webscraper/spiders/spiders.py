import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import json
import random


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        keywords = ["Software"]
        location = "Canada"

        baseURL = f"https://www.linkedin.com/jobs/search?keywords={keywords[0]}&location={location}&f_TPR=r86400"
        #baseURL = "https://www.w3schools.com"
        url = baseURL

        yield SplashRequest(url, self.parse, args={'wait': 0.5})
    
    def parse(self, response):
        for jobs in response.css(".base-card"):
            urls = jobs.css("a::attr(href)").getall()

            yield {
                "links": urls,
                "title": jobs.css(".base-search-card__title").get(),
                "company": jobs.css(".base-search-card__subtitle").get(),
                "location": jobs.css(".job-search-card__location").get(),
            }

class ProxySpider(scrapy.Spider):
    name = "proxy"

    def start_requests(self):
        url = "https://api.proxyscrape.com/proxytable.php?nf=true&country=all"

        yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        rawProxyList = json.loads(response.text)
        proxyList = []
        for proxy in rawProxyList["http"].items():
            proxyAddress = proxy[0]
            proxyValues = proxy[1]
            if proxyValues["anonymity"]==3:
                proxyList.append(proxyAddress)
        with open("../proxies.txt", "w") as outfile:
            for item in proxyList:
                outfile.write("%s\n" % item)




process = CrawlerProcess(get_project_settings())

process.crawl(ProxySpider)
process.crawl(LinkedinSpider)
process.start()