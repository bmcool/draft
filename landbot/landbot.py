#-*- encoding: utf-8 -*-

from splinter import Browser
import time
import random

class LandBot:
    def __init__(self):
        self.browser = None
        self.url = "http://lvr.land.moi.gov.tw/N11/homePage.action"
        # home_page, search_page
        self.current_page = None
        self.current_city = None
        self.current_area = None
        self.current_number = None

    def run(self):
        while True:
            try:
                self.browser = Browser('chrome')
                self.browser.visit(self.url)
                self.update_current_page()
                self.into_search_page()
                self.city_area_for()
            except Exception, e:
                self.browser.quit()
                print "Stop at %s_%s_%s" % (self.current_city, self.current_area, self.current_number)

    def into_search_page(self):
        while self.current_page != "search_page":
            if not self.browser.is_text_present(u'驗證碼'):
                self.browser.find_by_id('land').click()
            self.update_current_page()
            time.sleep(0.5)

    def city_area_for(self):
        cities = [option.value for option in self.browser.find_by_id('Qry_city').find_by_tag('option')[1:]]
        for city in cities:
            self.browser.find_by_id('Qry_city').select(city)
            self.current_city = city

            areas = [option.value for option in self.browser.find_by_id('Qry_area_office').find_by_tag('option')[1:]]
            for area in areas:
                self.browser.find_by_id('Qry_area_office').select(area)
                self.current_area = area

                self.browser.find_by_id('search_1').click()

                self.number_for()

    def number_for(self):
        numbers = [option.value for option in self.browser.find_by_id('page_tol').find_by_tag('option')]
        for number in numbers:
            self.browser.find_by_id('page_tol').find_by_value(number).click()

            while self.browser.is_text_present("資料換頁顯示中"):
                time.sleep(0.5)
            self.current_number = number

            self.save_current_html_to_file()
            time.sleep(random.randint(10, 20))

    def save_current_html_to_file(self):
        filename = "%s_%s_%s.html" % (self.current_city, self.current_area, self.current_number)
        f = open(filename, "w")
        f.write(self.browser.html.encode('utf-8'))
        f.close()
        print "created %s" % filename

    def update_current_page(self):
        if self.browser.title == u'內政部:::不動產交易實價查詢服務網':
            self.current_page = "home_page"
        elif self.browser.title == u'不動產交易實價查詢服務網':
            self.current_page = "search_page"
        else:
            self.current_page = "unknown"

bot = LandBot()
bot.run()
