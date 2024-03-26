# import scrapy

# class MySpider(scrapy.Spider):
#     name = 'myspider'
#     start_urls = ['https://playwright.dev/python/']

#     def parse(self, response):
#         # Parse the response here
#         # Example: extract the title of the page
#         title = response.css('title::text').get()
#         yield {
#             'title': title,
#         }

import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.americanunderwaterservices.com/']

    def parse(self, response):
        title = response.xpath('//title/text()').get()
        url = response.url
        content = response.body.decode(response.encoding)
        
        # Save source to a text file
        filename = f'{self.name}-{url.split("/")[-2]}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        yield {
            'title': title,
            'url': url,
            'filename': filename,
        }

# Run the spider
process = CrawlerProcess()
process.crawl(MySpider)
process.start()
