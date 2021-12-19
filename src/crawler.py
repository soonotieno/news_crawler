import time
from selenium import webdriver


class Crawler:
    def __init__(self, search_options, search_keyword_list):
        self.webdriver = None
        self.index_position = 0
        self.search_keyword_list = search_keyword_list
        self.search_options = search_options
        self.xpath = search_options['xpath']

    def get_crawler_type(self):
        return self.search_options['crawler_type']

    def set_webdriver(self, webdriver):
        self.webdriver = webdriver

    def get_webdriver(self):
        return self.webdriver

    def make_webdriver(self):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument("--start-maximized")
        # driver_options.add_argument('headless') # headless mode
        chrome_driver = webdriver.Chrome('chromedriver.exe', options=driver_options)
        chrome_driver.implicitly_wait(10)
        chrome_driver.get(self.get_access_url())
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])
        self.set_webdriver(chrome_driver)
        return chrome_driver

    def get_access_url(self):
        return self.search_options['access_url']

    def get_sort_type(self):
        return self.search_options['sort_type']

    def get_period_type(self):
        return self.search_options['period_type']

    def get_xpath(self):
        return self.xpath

    def scrape_article_content(self, article_elements, search_keywords):
        pass

    def debug_article_scrape(self, article_info):
        pass

    def input_search_keywords(self, search_keywords, index_position):
        pass

    def make_indices_per_page(self):
        xpath = self.get_xpath()
        current_article_xpath = xpath['article_list_per_page']
        current_article_elements = self.find_elements_by_xpath(current_article_xpath)
        current_article_index = len(current_article_elements) - 1
        return current_article_index

    def find_elements_by_xpath(self, xpath):
        driver = self.get_webdriver()
        elements = driver.find_elements_by_xpath(xpath)
        return elements

    def scroll_up_to_end(self):
        driver = self.get_webdriver()
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        time.sleep(2)

    def scroll_down_to_end(self):
        driver = self.get_webdriver()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

    def click_next_page_button(self):
        next_page_button_element = self.get_next_page_button_elements()
        next_page_button_element.click()
        time.sleep(2)

    def get_next_page_button_elements(self):
        driver = self.get_webdriver()
        xpath = self.get_xpath()
        next_page_button_xpath = xpath['next_page_button']
        next_page_button_elements = driver.find_elements_by_xpath(next_page_button_xpath)
        if next_page_button_elements:
            return next_page_button_elements[0]
        else:
            return None

    def select_search_options(self):
        pass

    def increase_index(self):
        self.index_position += 1
        return self.index_position

    def get_article_info_per_page(self, search_keywords):
        pass

    def search_article_and_get_info(self, search_keywords):
        pass

    # [Start] NFT Crawler Functions -------------------------------------------
    def get_nft_info_and_set_period(self, index_position):
        pass

    def get_nft_info_per_page(self, search_keywords):
        pass
    # [End] NFT Crawler Functions -------------------------------------------

    def do_crawl(self):
        driver = self.make_webdriver()
        crawler_type = self.get_crawler_type()
        index_position = self.index_position
        if crawler_type == 'news_crawler':
            search_keywords = self.search_keyword_list
            self.select_search_options()
            self.input_search_keywords(search_keywords, index_position)
            result = self.search_article_and_get_info(search_keywords)
            print('result article list :', result)
        elif crawler_type == 'nft_crawler':
            self.select_search_options()
            self.scroll_down_to_end()
            result = self.get_nft_info_and_set_period(index_position)
            print('result article list :', result)
        else:
            pass
        driver.close()
