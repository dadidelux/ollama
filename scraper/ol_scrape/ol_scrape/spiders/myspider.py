# import scrapy
# from scrapy.crawler import CrawlerProcess
# from bs4 import BeautifulSoup
import os
import json

# class MySpider(scrapy.Spider):
#     name = 'myspider'
#     start_urls = ['https://www.americanunderwaterservices.com/']

#     def parse(self, response):
#         url = response.url

#         title = response.xpath('//title/text()').get()
#         url = response.url
#         content = response.body.decode(response.encoding)

#         # Save source to a text file
#         filename = f'{self.name}-{url.split("/")[-2]}+ "_all".txt'
#         with open(filename , 'w', encoding='utf-8') as f:
#             f.write(content)


#         soup = BeautifulSoup(response.body, 'html.parser')

#         # Extract title
#         title = soup.title.string if soup.title else ''

#         # Extract all textual information
#         texts = soup.stripped_strings
#         all_text = ' '.join(texts)

#         # Save source to a text file
#         filename = f'{self.name}-{url.split("/")[-2]}.txt'
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(all_text)

#         # Prepare data to be saved
#         data = {
#             'title': title,
#             'url': url,
#             'filename': filename,
#             'text': all_text,
#         }

#         # Save data to another text file in the data-scraped folder
#         data_folder = '../data-scraped'
#         os.makedirs(data_folder, exist_ok=True)
#         data_filename = os.path.join(data_folder, f'{self.name}-{url.split("/")[-2]}.json')
#         with open(data_filename, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=4)

#         yield data

# # Run the spider
# process = CrawlerProcess()
# process.crawl(MySpider)
# process.start()

import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import os

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.prim.com/']

    def parse(self, response):
        # Save the homepage in the 'menu' subfolder
        self.parse_page(response, 'menu')

        # Find all navigation links
        nav_links = response.css('nav a::attr(href)').getall()
        for link in nav_links:
            # Join the relative URL with the base to form an absolute URL
            absolute_url = urljoin(response.url, link)
            # Pass the 'menu' subfolder to the callback for menu pages
            yield scrapy.Request(absolute_url, callback=self.parse_page, cb_kwargs={'subfolder': 'menu'})

    def parse_page(self, response, subfolder):
        # This function is used to save the HTML content of the response
        url = response.url

        # Create a safe file name
        filename = f"{self.name}-{response.url.split('/')[-2]}.html"
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        if not filename.endswith('.html'):
            filename += '.html'

        # Determine the folder path based on the subfolder
        folder_path = os.path.join('menu', subfolder) if subfolder else 'menu'
        os.makedirs(folder_path, exist_ok=True)

        # Save HTML content to file in the specified folder
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Output for debugging
        yield {
            'url': url,
            'filename': file_path
        }

# Run the spider
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json',
})
process.crawl(MySpider)
process.start()
