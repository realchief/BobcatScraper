from scrapy.conf import settings
from scrapy import Request
import requests

import scrapy
from scrapy import Selector
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
            category = None
            subcategory = None
            specification_page = None
            features_page = None

            try:

                product_name = product_group.xpath(
                    './/div[contains(@class, "h5 dtm-") and contains(@class, "-lst-name")]/text()')[0].extract()
                product_name = str(product_name)
                product_name_info = product_name.split(' ')
                more_link = "https://www.bobcat.com/{category}/{subcategory}/models/{model}/{field}"

                if ('Skid-Steer Loader' in product_name) and ('Attachments' not in product_name):
                    category = 'Loaders'
                    subcategory = 'Skid-Steer'
                    model = product_name_info[1]

                    features_page = more_link.format(category="loaders", subcategory="skid-steer-loaders", model=model.lower(),
                                                     field="features")
                    specification_page = more_link.format(category="loaders", subcategory="skid-steer-loaders", model=model.lower(),
                                                     field="specs-options")
                    photo_video_page = more_link.format(category="loaders", subcategory="skid-steer-loaders", model=model.lower(),
                                                     field="photos-videos")
                    attachments_page = more_link.format(category="loaders", subcategory="skid-steer-loaders", model=model.lower(),
                                                     field="attachments-accessories")

                elif ('Compact Track Loader' in product_name) and ('Attachments' not in product_name):
                    category = 'Loaders'
                    subcategory = 'Compact Track'
                    model = product_name_info[1]

                    features_page = more_link.format(category="loaders", subcategory="compact-track-loaders", model=model.lower(),
                                                     field="features")
                    specification_page = more_link.format(category="loaders", subcategory="compact-track-loaders",
                                                          model=model.lower(),
                                                          field="specs-options")
                    photo_video_page = more_link.format(category="loaders", subcategory="compact-track-loaders",
                                                        model=model.lower(),
                                                        field="photos-videos")
                    attachments_page = more_link.format(category="loaders", subcategory="compact-track-loaders",
                                                        model=model.lower(),
                                                        field="attachments-accessories")

                elif ('Mini Track Loader' in product_name) and ('Attachments' not in product_name):
                    category = 'Loaders'
                    subcategory = 'Mini Track'
                    model = product_name_info[1]

                    features_page = more_link.format(category="loaders", subcategory="mini-track-loaders", model=model.lower(),
                                                     field="features")
                    specification_page = more_link.format(category="loaders", subcategory="mini-track-loaders",
                                                          model=model.lower(),
                                                          field="specs-options")
                    photo_video_page = more_link.format(category="loaders", subcategory="mini-track-loaders",
                                                        model=model.lower(),
                                                        field="photos-videos")
                    attachments_page = more_link.format(category="loaders", subcategory="mini-track-loaders",
                                                        model=model.lower(),
                                                        field="attachments-accessories")

                elif ('Compact Excavator' in product_name) and ('Attachments' not in product_name):
                    category = 'Compact Excavators'
                    subcategory = ''
                    model = product_name_info[1]

                    features_page = "https://www.bobcat.com/excavators/models/{model}/features".format(
                        model=model.lower())
                    specification_page = "https://www.bobcat.com/excavators/models/{model}/specs-options".format(
                        model=model.lower())
                    photo_video_page = 'https://www.bobcat.com/excavators/models/{model}/photos-videos'.format(
                        model=model.lower())
                    attachments_page = 'https://www.bobcat.com/excavators/models/{model}/attachments-accessories'.format(
                        model=model.lower())

                elif ('Utility Vehicle' in product_name) and ('Attachments' not in product_name):
                    category = 'Utility Vehicles'
                    subcategory = ''
                    model = product_name_info[1]

                    features_page = more_link.format(category="utility-products", subcategory="utv", model=model.lower(),
                                                     field="features")
                    specification_page = more_link.format(category="utility-products", subcategory="utv",
                                                          model=model.lower(),
                                                          field="specs-options")
                    photo_video_page = more_link.format(category="utility-products", subcategory="utv",
                                                        model=model.lower(),
                                                        field="photos-videos")
                    attachments_page = None

                elif ('Toolcat' in product_name) and ('Attachments' not in product_name):
                    category = 'Toolcats'
                    subcategory = ''
                    model = product_name_info[1]

                    features_page = "https://www.bobcat.com/loaders/skid-steer-loaders/models/{model}/features".format(
                        model=model.lower())
                    specification_page = "https://www.bobcat.com/loaders/skid-steer-loaders/models/{model}/specs-options".format(
                        model=model.lower())
                    photo_video_page = 'https://www.bobcat.com/loaders/skid-steer-loaders/models/{model}/photos-videos'.format(
                        model=model.lower())
                    attachments_page = 'https://www.bobcat.com/loaders/skid-steer-loaders/models/{model}/attachments-accessories'.format(
                        model=model.lower())

                elif ('Telehandler' in product_name) and ('Attachments' not in product_name):
                    category = 'Telehandlers'
                    subcategory = product_name_info[0]
                    model = product_name_info[1]

                    features_page = "https://www.bobcat.com/telehandlers/models/{model}/features".format(
                        model=model.lower())
                    specification_page = "https://www.bobcat.com/telehandlers/models/{model}/specs-options".format(
                        model=model.lower())
                    photo_video_page = 'https://www.bobcat.com/telehandlers/models/{model}/photos-videos'.format(
                        model=model.lower())
                    attachments_page = 'https://www.bobcat.com/telehandlers/models/{model}/attachments-accessories'.format(
                        model=model.lower())

                else:
                    product_name = None
                    category = None
                    subcategory = None
                    specification_page = None
                    features_page = None

            except:
                continue

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

            bobcat['Title'] = str(product_name)
            bobcat['Category'] = str(category)
            bobcat['SubCategory'] = str(subcategory)
            bobcat['Images'] = str(product_image)
            bobcat['Features'] = str(product_feature)
            if features_page:
                bobcat['Model'] = self.parse_model(features_page)
                bobcat['Description'] = self.parse_description(features_page)
            else:
                bobcat['Model'] = ""
                bobcat['Description'] = ""

            if features_page and specification_page:
                bobcat['Specification'] = self.parse_specification(specification_page, features_page)
            else:
                bobcat['Specification'] = None
            # bobcat['PhotoVideoGallery'] = self.parse_photovideogallery(photo_video_page)
            # bobcat['Attachments'] = self.parse_attachments(attachments_page)
            if product_name:
                yield bobcat

            else:
                continue

    def parse_description(self, features_page):
        description = None
        try:
            features_page_content = requests.get(features_page).content
            description = Selector(text=features_page_content).xpath('//div[@class="col-xs-12"]/p/text()').extract()
        except:
            print features_page
        return description[0] if description else ""

    def parse_model(self, features_page):
        model = None
        try:
            features_page_content = requests.get(features_page).content
            model = Selector(text=features_page_content).xpath('//div[@class="col-xs-12"]/h1/text()').extract()
        except:
            print features_page
        return model[0] if model else ""

    def parse_specification(self, specification_page, features_page):
        specification = None
        code = None
        specification_page_content = requests.get(specification_page).content
        div_list = Selector(text=specification_page_content).xpath('//div[@class="col-sm-6"]')
        for div in div_list:
            features_link = div.xpath('./h4/a/@href').extract()
            if features_link and (str(features_link[0]) == features_page):
                code_element = div.xpath('..//div[@class="product-overview"]/@ng-if').extract()
                if code_element:
                    code = str(code_element[0].split("'")[1])
            else:
                continue
        if code:
            request_url = 'https://cdn-proxy-gpim-com.dibhids.net/rest/proxy/globalpim/rest/enhancedProduct/catalog' \
                          '/CompactNA/version/Online/product/{code}?locale=en&i=12315&'.format(code=code)
            specification_values = requests.get(request_url).json()
            try:
                horse_power = str(specification_values['horsepower']['$'])
            except:
                horse_power = ''
            try:
                operating_weight = str(specification_values['operatingWeight']['$'])
            except:
                operating_weight = ''
            try:
                engine_cooling = str(specification_values['engineCooling'])
            except:
                engine_cooling = ''
            try:
                engine_fuel = str(specification_values['engineFuel'])
            except:
                engine_fuel = ''
            try:
                epa = str(specification_values['emissionsTier']['cAEnum'][0]['$'])
            except:
                epa = ''
            try:
                rated_OperatingCapacitySae = str(specification_values['ratedOperatingCapacitySae']['$'])
            except:
                rated_OperatingCapacitySae = ''
            try:
                tippingLoad = str(specification_values['tippingLoad']['$'])
            except:
                tippingLoad = ''
            try:
                travelSpeed = str(specification_values['travelSpeed']['$'])
            except:
                travelSpeed = ''

            specification = {
                'Horse Power': horse_power,
                'Operating Weight': operating_weight,
                'Engine Cooling': engine_cooling,
                'Engine Fuel': engine_fuel,
                'Emissions Tier(EPA)': epa,
                'Rated Operating Capacity(SAE)': rated_OperatingCapacitySae,
                'Tipping Load': tippingLoad,
                'Travel Speed': travelSpeed
            }

        return specification

    @staticmethod
    def _clean_text(text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        text = re.sub("&nbsp;", " ", text).strip()

        return re.sub(r'\s+', ' ', text)