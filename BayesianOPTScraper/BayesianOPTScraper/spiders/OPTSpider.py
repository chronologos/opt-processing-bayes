import scrapy
from bs4 import BeautifulSoup
import csv

class OPTSpider(scrapy.Spider):
    name = 'OPTSpider'

    def start_requests(self):
        # url = "https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum=YSC1890060000"
        url_base = "https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum=YSC189006"
        for i in range(10):
            N = 4
            n = len(str(i))
            num_zeroes = N - n
            url = url_base + num_zeroes*"0" + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "result.csv"
        with open(filename, 'a') as csvfile:
            w = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            soup = BeautifulSoup(response.body, 'html.parser')
            print(soup.prettify())
            try:
                found = soup.find(class_="appointment-sec").find(class_="text-center")
            except AttributeError as e:
                print(e)
                return
            if not found:
                return
            print("result: {0},{1}".format(found.h1.string,found.p))
            w.writerow([found.h1.string, found.p])
        # self.log('Saved file %s' % filename)
