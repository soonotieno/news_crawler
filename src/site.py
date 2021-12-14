from crawler import Crawler
from selenium.webdriver.common.by import By
import time

naver_search_options = {
    "company": "naver",
    "access_url": "https://search.naver.com/search.naver?query=&where=news&ie=utf8&sm=nws_hty",
    "sort_type": "new",  # 관련도순:relation / 최신순:new / 오래된순:old
    "period_type": "daily",
    "xpath": {
        "sort_select_button": {
            "relation": "//*[@id='snb']/div[@class='api_group_option_filter _search_option_simple_wrap']/div/div[@class='option_area type_sort']/a[1]",
            "new": "//*[@id='snb']/div[@class='api_group_option_filter _search_option_simple_wrap']/div/div[@class='option_area type_sort']/a[2]",
            "old": "//*[@id='snb']/div[@class='api_group_option_filter _search_option_simple_wrap']/div/div[@class='option_area type_sort']/a[3]",
        },
        "option_button": "//*[@id='snb']/div[@class='api_group_option_filter _search_option_simple_wrap']/div/div[@class='option_filter']/a",
        "period_select_button": {
            "all": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[1]",
            "daily": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[3]",
            "weekly": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[4]",
            "one_month": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[5]",
            "two_month": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[6]",
            "three_month": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[7]",
            "yearly": "//*[@id='snb']/div[@class='api_group_option_sort _search_option_detail_wrap']/ul/li[@class='bx term']/div/div[@class='option']/a[8]",
        },
        "article_list_per_page": "//*[@id='main_pack']/section/div/div[@class='group_news']/ul/li",
        "next_page_button": "//*[@id='main_pack']/div[@class='api_sc_page_wrap']/div/a[@class='btn_next' and @aria-disabled='false']",
        "search_box": "//*[@id='nx_query']",
    }
}

google_search_options = {
    "company": "google",
    "access_url": "https://www.google.com/search?q=%22%22&source=lnms&tbm=nws&sa=X",
    "sort_type": "korean_web",  # 한국어 웹 : korean_web / 웹 검색 : web_search
    "period_type": "daily",
    "xpath": {
        "sort_select_button": {
            "normal_web": "//*[@id='lb']/div/g-menu/g-menu-item[1]/div/div",
            "korean_web": "//*[@id='lb']/div/g-menu/g-menu-item[2]/div/a",
        },
        "option_button": "//*[@id='hdtb-tls']",
        "period_select_button": {
            "all": "//*[@id='lb']/div/g-menu/g-menu-item[1]/div/div",
            "daily": "//*[@id='lb']/div/g-menu/g-menu-item[3]/div/a",
            "weekly": "//*[@id='lb']/div/g-menu/g-menu-item[4]/div/a",
            "monthly": "//*[@id='lb']/div/g-menu/g-menu-item[5]/div/a",
            "yearly": "//*[@id='lb']/div/g-menu/g-menu-item[6]/div/a",
        },
        "article_list_per_page": "//*[@id='rso']/div",
        "next_page_button": "//*[@id='pnnext']",
        "search_box": "//*[@id='tsf']/div[1]/div[1]/div[2]/div[2]/div[2]/input",
    }
}

search_keyword_list = ['애플카', '도지코인', '한국정보공학']


# 구글 뉴스 크롤러!
class GetGoogleNewsCrawler(Crawler):

    def get_article_title(self, article):
        article_title = article.find_element(By.XPATH,
                                             "./g-card/div/div/a/div/div[@class='iRPxbe']/div[@class='mCBkyc tNxQIb y355M JIFdL JQe2Ld nDgy9d']").text
        return article_title

    def get_article_content(self, article):
        article_content = article.find_element(By.XPATH,
                                               "./g-card/div/div/a/div/div[@class='iRPxbe']/div[@class='GI74Re nDgy9d']").text
        return article_content

    def get_article_url(self, article):
        article_url = article.find_element(By.XPATH, "./g-card/div/div/a").get_attribute('href')
        return article_url

    def get_article_img(self, article):
        article_img = article.find_element(By.XPATH,
                                           "./g-card/div/div/a/div/div[@class='FAkayc']/div/g-img/img").get_attribute(
            'src')
        return article_img

    def get_article_press(self, article):
        article_press = article.find_element(By.XPATH,
                                             "./g-card/div/div/a/div/div[@class='iRPxbe']/div[@class='CEMjEf NUnG9d']/span").text
        return article_press

    def get_article_publication_date(self, article):
        article_publication_date = article.find_element(By.XPATH,
                                                        "./g-card/div/div/a/div/div[@class='iRPxbe']/div[@class='ZE0LJd']/p/span").text
        return article_publication_date

    def select_search_options(self):
        driver = self.get_webdriver()
        sort_type = self.get_sort_type()
        period_type = self.get_period_type()
        xpath = self.get_xpath()
        sort_select_button_xpath = xpath['sort_select_button']
        period_select_button_xpath = xpath['period_select_button']
        option_button_elements = driver.find_elements(By.XPATH, xpath['option_button'])
        option_button_elements[0].click()
        time.sleep(2)
        web_search_button_elements = driver.find_element(By.XPATH, "//*[@id='hdtbMenus']/span[1]/g-popup/div[1]/div/div/div")
        web_search_button_elements.click()
        time.sleep(1)
        sort_type_select_button_elements = driver.find_elements(By.XPATH, sort_select_button_xpath[sort_type])
        sort_type_select_button_elements[0].click()
        time.sleep(2)
        web_search_button_elements = driver.find_element(By.XPATH, "//*[@id='hdtbMenus']/span[2]/g-popup/div[1]/div/div/div")
        web_search_button_elements.click()
        time.sleep(1)
        period_type_select_button_elements = driver.find_elements(By.XPATH, period_select_button_xpath[period_type])
        period_type_select_button_elements[0].click()
        time.sleep(2)


# 네이버 뉴스 크롤러!
class GetNaverNewsCrawler(Crawler):

    def get_article_title(self, article):
        article_title = article.find_element(By.XPATH, "./div/div/a").get_attribute('title')
        return article_title

    def get_article_content(self, article):
        article_content = article.find_element(By.XPATH, "./div/div/div[@class='news_dsc']/div/a").text
        return article_content

    def get_article_url(self, article):
        article_url = article.find_element(By.XPATH, "./div/div/a").get_attribute('href')
        return article_url

    def get_article_img(self, article):
        article_img = article.find_element(By.XPATH, "./div/a/img").get_attribute('src')
        return article_img

    def get_article_press(self, article):
        article_press = article.find_element(By.XPATH, "./div/div/div[@class='news_info']/div["
                                                       "@class='info_group']/a").text
        return article_press

    def get_article_publication_date(self, article):
        article_publication_date = article.find_element(By.XPATH, "./div/div/div[@class='news_info']/div["
                                                                  "@class='info_group']/span").text
        return article_publication_date

    def select_search_options(self):
        driver = self.get_webdriver()
        sort_type = self.get_sort_type()
        period_type = self.get_period_type()
        xpath = self.get_xpath()
        sort_type_xpath = xpath['sort_select_button']
        period_type_xpath = xpath['period_select_button']
        sort_type_select_button_elements = driver.find_elements(By.XPATH, sort_type_xpath[sort_type])
        sort_type_select_button_elements[0].click()
        time.sleep(2)
        option_button_elements = driver.find_elements(By.XPATH, xpath['option_button'])
        option_button_elements[0].click()
        time.sleep(2)
        period_type_select_button_elements = driver.find_elements(By.XPATH, period_type_xpath[period_type])
        period_type_select_button_elements[0].click()
        time.sleep(2)


def news_crawl():
    crawler = GetNaverNewsCrawler(search_keyword_list=search_keyword_list, search_options=naver_search_options)
    product_list = crawler.do_crawl()
    print(product_list)

    # crawler = GetGoogleNewsCrawler(search_keyword_list=search_keyword_list, search_options=google_search_options)
    # product_list = crawler.do_crawl()
    # print(product_list)


if __name__ == '__main__':
    news_crawl()
