import scrapy
import requests
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cveScraping.items import CvescrapingItem
import time

class VulmonspiderSpider(scrapy.Spider):
    name = 'vulmonspider'
    allowed_domains = ['vulmon.com']
    start_urls = ['https://vulmon.com/searchpage?q=%2A&sortby=bydate&page={0}'.format(i) for i in range(1,256)]
        
    def start_requests(self):
        for i in range(len(self.start_urls)):         
            yield scrapy.Request(self.start_urls[i], self.parse,
                # args={'wait':0.5},
            )
            
    def parse(self, response):
        print("start_url : ", response.url)
        for url in response.css('.item a::attr(href)').extract():
            # スクレイピング間隔を落とす
            time.sleep(1.0)
            # urlの先頭に　https://vulmon.com/ を付け加えたuriとする
            uri = response.urljoin(url)
            # そのuriに対してスクレイピングを行う
            # yield SeleniumRequest(url=uri, callback=self.parse_detail)
            options = Options()

            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')

            driver = webdriver.Chrome(chrome_options=options)
            try:
                driver.get(uri)
                u = driver.current_url
                cve = driver.find_element_by_css_selector('h1')
                summary = driver.find_element_by_css_selector('.content_overview')
                print("URL : ", u)
                print("CVE : ",cve.text)
                print("VulnerabilitySummary : ", summary.text)
                yield CvescrapingItem(
                    url = u,
                    tags = cve.text,
                    VulnSummary = summary.text,
                 )
            except:
                print('driver get error')
                pass
            finally:
                driver.quit()
            

    # def parse_detail(self, response):
    #     time.sleep(0.5)
    #     # print(response.text)
    #     print("CVE", response.xpath('//h1/text()'))
