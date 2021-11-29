# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CvescrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # site URL
    url = scrapy.Field()
    # Vulnerability Name
    # Title = scrapy.Field()
    # source site. ExploitDB, vulners or vulmon
    site = "Vulmon"
    # tags that include CVE, CPE, and so on
    tags = scrapy.Field()
    # feature extracted from html
    VulnSummary = scrapy.Field()
    