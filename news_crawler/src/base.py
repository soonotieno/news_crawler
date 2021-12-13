from crawlers.crawler import Crawler
import time
from selenium.webdriver.common.keys import Keys


class BaseCrawler(Crawler):

    def get_article_info(self):
        driver = self.get_webdriver()
        xpath = self.get_xpath()
        article_info = {}
        articles_info = []
        article_list_xpath = xpath['article_list_per_page']
        article_elements = self.find_elements_by_xpath(article_list_xpath)
        print('article_elements 몇개? :', len(article_elements))
        for article in article_elements:
            article_info['article_url'] = "url info"
            article_info['press'] = "press info"
            article_info['image'] = "image info"
            article_info['title'] = "title info"
            article_info['content'] = "content info"
            article_info['publication_date'] = "publication_date info"
            articles_info.append(article_info.copy())
        return articles_info.copy()


    def select_search_options(self, driver):
        sort_type = self.get_sort_type()
        period_type = self.get_period_type()
        xpath = self.get_xpath()
        sort_type_xpath = xpath['sort_select_button']
        period_type_xpath = xpath['period_select_button']
        sort_type_select_button_elements = driver.find_elements_by_xpath(sort_type_xpath[sort_type])
        sort_type_select_button_elements[0].click()
        time.sleep(2)
        option_button_elements = driver.find_elements_by_xpath(xpath['option_button'])
        option_button_elements[0].click()
        time.sleep(2)
        period_type_select_button_elements = driver.find_elements_by_xpath(period_type_xpath[period_type])
        period_type_select_button_elements[0].click()
        time.sleep(2)

    # def get_article_info(self):
    #     driver = self.get_webdriver()
    #     xpath = self.get_xpath()
    #     article_info = {}
    #     articles_info = []
    #     article_list_xpath = xpath['article_list_per_page']
    #     article_elements = self.find_elements_by_xpath(article_list_xpath)
    #     for article in article_elements:
    #         article_info['url'] = article.find_element_by_xpath("./div/div/a").get_attribute('href')
    #         article_info['press'] = article.find_element_by_xpath(
    #             "./div/div/div[@class='news_info']/div[@class='info_group']/a/span").text
    #         article_info['image'] = article.find_element_by_xpath("./div/a/img").get_attribute('src')
    #         article_info['title'] = article.find_element_by_xpath("./div/div/a").get_attribute('title')
    #         article_info['content'] = article.find_element_by_xpath("./div/div/div[@class='news_dsc']/div/a").text
    #         article_info['publication_date'] = article.find_element_by_xpath(
    #             "./div/div/div[@class='news_info']/div[@class='info_group']/span").text
    #         articles_info.append(article_info.copy())
    #     return articles_info.copy()
