import scrapy
from joseph_storage.items import Site
from urllib.parse import urlparse
import datetime

class SitesSpider(scrapy.Spider):
    name = "sites"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        parsed_response_uri = urlparse(response.url)
        parsed_request_uri = urlparse(response.request.url)
        hxs = scrapy.Selector(response)
        all_links = hxs.xpath('*//a/@href').extract()
        all_full_links = [ urlparse(response.urljoin(link)) for link in all_links ]
        outlink_domains = set([ full_link.hostname for full_link in all_full_links ])
        outlink_domains.discard(parsed_response_uri.hostname)
        description = None
        if len(response.xpath("//meta[@name='description']/@content")) > 0:
            response.xpath("//meta[@name='description']/@content")[0].extract()
        
        site = Site({
            'domain': parsed_response_uri.hostname,
            'redirect_domains': [parsed_request_uri.hostname],
            'title': response.css('title::text').extract_first(),
            'description': description,
            'html': response.body,
            'outlink_domains': list(outlink_domains),
            'last_updated': datetime.datetime.now()
        })
        yield site

        for full_link in all_full_links:
            if full_link.scheme != 'http' && full_link.scheme != 'https':
                continue
            link_to_crawl = '{uri.scheme}://{uri.netloc}/'.format(uri=full_link)
            yield scrapy.Request(link_to_crawl, callback=self.parse)