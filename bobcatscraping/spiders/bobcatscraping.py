from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
from lxml import html

import scrapy
from scrapy.item import Item, Field
import re


class SiteProductItem(Item):
    Title = Field()
    Images = Field()
    Features = Field()
    Category = Field()
    SubCategory = Field()
    Model = Field()
    Description = Field()
    Specification = Field()
    PhotoVideoGallery = Field()
    Attachments = Field()


class BobcatScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.bobcat.com']
    START_URL = 'https://www.bobcat.com/index'
    DOMAIN_URL = 'https://www.bobcat.com/'
    settings.overrides['ROBOTSTXT_OBEY'] = False
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/57.0.2987.133 Safari/537.36"}

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.parse_page,
                      dont_filter=True
                      )

    def parse_page(self, response):

        bobcat = SiteProductItem()

        product_group_list = response.xpath('//a[contains(@class, "product-item")]')
        for product_group in product_group_list:

            product_name = None
            try:

                product_name = product_group.xpath(
                    './/div[contains(@class, "h5 dtm-") and contains(@class, "-lst-name")]/text()')[0].extract()
                product_name = str(product_name)
                product_name_info = product_name.split(' ')
                if 'Skid-Steer Loader' in product_name:
                    category = 'Loader'
                    subcategory = 'Skid-Steer'
                    model = product_name_info[1]
                elif 'All-Wheel Steer Loader' in product_name:
                    category = 'Loader'
                    subcategory = 'All-Wheel Steer'
                    model = product_name_info[1]
                elif 'Compact Track Loader' in product_name:
                    category = 'Loader'
                    subcategory = 'Compact Track'
                    model = product_name_info[1]
                elif 'Mini Track Loader' in product_name:
                    category = 'Loader'
                    subcategory = 'Mini Track'
                    model = product_name_info[1]
                elif 'Compact Excavator' in product_name:
                    category = 'Compact Excavator'
                    subcategory = ''
                    model = product_name_info[1]
                elif 'Utility Vehicle' in product_name:
                    category = 'Utility Vehicle'
                    subcategory = ''
                    model = product_name_info[1]
                elif 'Toolcat' in product_name:
                    category = 'Toolcat'
                    subcategory = ''
                    model = product_name_info[1]
                elif 'Telehandler' in product_name:
                    category = 'Telehandler'
                    subcategory = product_name_info[0]
                    model = product_name_info[1]
                elif 'Attachments' in product_name:
                    category = 'Attachments'
                    subcategory = product_name.replace(' Attachments', '')
                    model = ''
                else:
                    category = None
                    subcategory = None
                    model = None

            except:
                pass

            product_image = None
            try:
                product_image = product_group.xpath('.//@data-src')[0].extract()
            except:
                pass

            product_feature = None
            try:
                product_feature = product_group.xpath('.//p/text()')[0].extract()
            except:
                pass

            bobcat['Title'] = product_name
            bobcat['Category'] = category
            bobcat['SubCategory'] = subcategory
            bobcat['Model'] = model
            bobcat['Images'] = product_image
            bobcat['Features'] = product_feature
            yield bobcat

    @staticmethod
    def _clean_text(text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        text = re.sub("&nbsp;", " ", text).strip()

        return re.sub(r'\s+', ' ', text)