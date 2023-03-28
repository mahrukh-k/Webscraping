from scrapy.spiders import Spider
from scrapy import Request

# Note: install XPath Chrome Extension. Open extension. Hover over website element, copy XPath, paste it here in .xpath()

# To Run:
# Go to the bo_business folder, and from there, run in terminal:
# scrapy crawl bo_business_2 -O results.csv 2> trace 
# python -m scrapy runspider spiders/bospider_jamie.py -O results.csv 2> trace
# results are stored in results.csv
# trace is stored in trace

class bo_business_2(Spider):
    name = 'bo_business_2'
    base =  "https://thesoulpitt.com/diversitydirectory/?s="
    start_urls = [base] 

    def parse(self, response):
        # For each listing link listed on the page
        for listing in response.css("a[rel='bookmark']::attr(href)"):
            
            # Give me the link
            url = listing.get()     # Probably will raise an error, consider using extract_first() instead of get()
            yield Request(url, callback = self.parse_page)

        # Get next page. 
        try: # Try block finds next page if there's a previous AND a next page option
            next_page = response.css("div.browse a::attr(href)")[1].get()
        except: # Finds next page for first page
            next_page = response.css("div.browse a::attr(href)").get()
        
        # If it exists, follow it and do it again!
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def parse_page(self, response):
        type = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[0]
        name = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[1]
        address = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[2]
        email = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[3]
        phone = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[4]
        website = response.xpath(".//div[@class='entry']/p[1]/text()").extract()[5]
        category = response.xpath(".//p[@class='postinfo']/a[1]/text()").extract()
        yield {
            'type' : type,
            'name' : name,
            'address' : address,
            'email' : email,
            'phone' : phone,
            'website' : website,
            'category' : category
        }