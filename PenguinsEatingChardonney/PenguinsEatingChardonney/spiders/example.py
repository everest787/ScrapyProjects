import scrapy
import PIL.Image as Image

from scrapy_playwright.page import PageMethod

#install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')


class ExampleSpider(scrapy.Spider):
    name = "example"

    def start_requests(self):
        url = "https://www.whatismyip.com/"
        # GET request
        yield scrapy.Request(url, meta=dict(
			playwright = True,
			playwright_include_page = True, 
            playwright_page_methods = [
                PageMethod("screenshot", path="example.png", full_page=True),
                PageMethod('wait_for_selector', '.the-ipv4')
            ],
      		errback=self.errback,
		))


    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        screenshot = await page.screenshot(path="example.png", full_page=True)
        return {"url": response.url, "ip": response.css("#ip-info").get()}
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()