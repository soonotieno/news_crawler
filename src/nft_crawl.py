from crawler import Crawler
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from base import BaseNftCrawler
import time

# [OpenSea] NFT_crawler Options
opensea_search_options = {
    "crawler_type": "nft_crawler",
    "site_name": "opensea",
    "access_url": "https://opensea.io/rankings",
    "paging_type": "all_page",
    "paging_options": {
        "all_page": 0,
        "one_page": 1
    },
    "sort_type": "new",  # 전체:all / 신규:new / 음악:music / 예술:art ...etc
    "period_type": "daily",
    "xpath": {
        "sort_button": "//*[@id='main']/div/div[1]/div/div/div[2]/button",
        "sort_select_button": {
            "all": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[1]/button",
            "new": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[2]/button",
            "art": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[3]/button",
            "music": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[4]/button",
            "domain_names": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[5]/button",
            "virtual_worlds": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[6]/button",
            "trading_cards": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[7]/button",
            "collectibles": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[8]/button",
            "sports": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[9]/button",
            "utility": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[10]/button",
        },
        "period_button": "//*[@id='main']/div/div[1]/div/div/div[1]/button",
        "period_select_button": {
            "daily": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[1]/button",
            "weekly": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[2]/button",
            "monthly": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[3]/button",
            "all": "//*[contains(@id, 'tippy-')]/div/div/div/ul/li[4]/button",
        },
        "nft_list_per_page": "//*[@id='main']/div/div[2]/div/div[2]/div",
        "next_page_button": "//*[@id='main']/div/div[3]/button[2]",
        "search_box": "//*[@id='__next']/div[1]/div[1]/nav/div[2]/div/div/div/input",
    }
}

search_keyword_list = []


# OpenSea NFT Top 100 크롤러!
class GetOpenseaRankingCrawler(BaseNftCrawler):

    def select_search_options(self):
        driver = self.get_webdriver()
        sort_type = self.get_sort_type()
        period_type = self.get_period_type()
        xpath = self.get_xpath()
        sort_button_xpath = xpath['sort_button']
        period_button_xpath = xpath['period_button']
        sort_select_button_xpath = xpath['sort_select_button']
        period_select_button_xpath = xpath['period_select_button']
        time.sleep(2)
        period_button_elements = driver.find_elements(By.XPATH, period_button_xpath)
        period_button_elements[0].click()
        time.sleep(2)
        period_select_button_elements = driver.find_elements(By.XPATH, period_select_button_xpath[period_type])
        period_select_button_elements[0].click()
        time.sleep(2)
        sort_button_elements = driver.find_elements(By.XPATH, sort_button_xpath)
        sort_button_elements[0].click()
        time.sleep(2)
        sort_select_button_elements = driver.find_elements(By.XPATH, sort_select_button_xpath[sort_type])
        sort_select_button_elements[0].click()
        time.sleep(2)

    def get_nft_ranking(self, nft_element):
        ranking = nft_element.find_element(By.XPATH, "./a/div/div[1]/span/div").text
        return ranking

    def get_nft_collection_name(self, nft_element):
        collection_name = nft_element.find_element(By.XPATH, "./a/div/div[3]/span/div").text
        return collection_name

    def get_nft_collection_icon(self, nft_element):
        try:
            collection_icon = nft_element.find_element(By.XPATH, "./a/div/div[2]/div[1]/div/img").get_attribute('src')
            return collection_icon
        except NoSuchElementException:
            return "NoSuchElement"

    def get_nft_volume(self, nft_element):
        return ""

    def get_percentage_daily(self, nft_element):
        return ""

    def get_percentage_weekly(self, nft_element):
        return ""

    def get_nft_fool_price(self, nft_element):
        return ""

    def get_nft_owners(self, nft_element):
        return ""

    def get_nft_items(self, nft_element):
        return ""


def nft_crawl():
    crawler = GetOpenseaRankingCrawler(search_keyword_list=search_keyword_list, search_options=opensea_search_options)
    product_list = crawler.do_crawl()
    print(product_list)


if __name__ == '__main__':
    nft_crawl()
