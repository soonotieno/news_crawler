import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler:
    def __init__(self, search_keyword_list, search_options):
        self.webdriver = None
        self.keyword_index_position = 0
        self.search_keyword_list = search_keyword_list
        self.search_options = search_options
        self.xpath = search_options['xpath']

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

    def get_article_info(self):
        xpath = self.get_xpath()
        article_list_xpath = xpath['article_list_per_page']
        article_elements = self.find_elements_by_xpath(article_list_xpath)
        result_article_list = self.scrape_article_content(article_elements)
        return result_article_list

    def scrape_article_content(self, article_elements):
        article_info = {}
        articles_info = []
        for article in article_elements:
            article_info['title'] = self.get_article_title(article)
            article_info['content'] = self.get_article_content(article)
            article_info['article_url'] = self.get_article_url(article)
            article_info['press'] = self.get_article_press(article)
            article_info['image'] = self.get_article_img(article)
            article_info['publication_date'] = self.get_article_publication_date(article)
            print(self.debug_article_scrape(article_info))
            articles_info.append(article_info.copy())
        return articles_info.copy()

    def debug_article_scrape(self, article_info):
        format = f"제목 : {article_info['title']}\n"
        format += f"내용 : {article_info['content']}\n"
        format += f"URL : {article_info['article_url']}\n"
        format += f"언론사 : {article_info['press']}\n"
        format += f"이미지 : {article_info['image']}\n"
        format += f"배포일 : {article_info['publication_date']}\n"
        format += f"-------------------------------------------------------------------------"
        return format

    # [start] it is going to be overridden --------------------

    def get_article_title(self, article):
        pass

    def get_article_content(self, article):
        pass

    def get_article_url(self, article):
        pass

    def get_article_press(self, article):
        pass

    def get_article_img(self, article):
        pass

    def get_article_publication_date(self, article):
        pass

    def select_search_options(self):
        pass

    # [end] it is going to be overridden --------------------

    def input_search_keywords(self, search_keywords, keyword_index_position):
        driver = self.get_webdriver()
        xpath = self.get_xpath()
        search_box_xpath = xpath['search_box']
        search_box_elements = driver.find_elements_by_xpath(search_box_xpath)
        search_box_elements[0].clear()
        search_box_elements[0].send_keys(search_keywords[keyword_index_position])
        search_box_elements[0].send_keys(Keys.ENTER)
        time.sleep(2)

    def make_article_indices_per_page(self):
        xpath = self.get_xpath()
        current_article_xpath = xpath['article_list_per_page']
        current_article_elements = self.find_elements_by_xpath(current_article_xpath)
        current_article_index = len(current_article_elements) - 1
        return current_article_index

    def find_elements_by_xpath(self, xpath):
        driver = self.get_webdriver()
        elements = driver.find_elements_by_xpath(xpath)
        return elements

    def scroll_down_to_end(self):
        driver = self.get_webdriver()
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        time.sleep(2)

    def scroll_up_to_end(self):
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
            return []

    def increase_keyword_index(self):
        self.keyword_index_position += 1
        return self.keyword_index_position

    def search_article_and_get_info(self, search_keywords):
        result_all_article_list = []
        while True:
            button_next = self.get_next_page_button_elements()
            self.scroll_down_to_end()
            result_article_per_page = self.get_article_info()
            result_all_article_list.extend(result_article_per_page.copy())
            if button_next:
                if button_next.get_attribute('aria-disabled') == 'false':
                    self.click_next_page_button()
                else:
                    current_keyword_index = self.increase_keyword_index()
                    self.scroll_up_to_end()
                    if current_keyword_index >= len(search_keywords):
                        return result_all_article_list.copy()
                    else:
                        self.input_search_keywords(search_keywords, current_keyword_index)
                        continue
            else:
                current_keyword_index = self.increase_keyword_index()
                self.scroll_up_to_end()
                if current_keyword_index >= len(search_keywords):
                    return result_all_article_list.copy()
                else:
                    self.input_search_keywords(search_keywords, current_keyword_index)
                    continue

    def do_crawl(self):
        driver = self.make_webdriver()
        search_keywords = self.search_keyword_list
        keyword_index_position = self.keyword_index_position
        self.select_search_options()
        self.input_search_keywords(search_keywords, keyword_index_position)
        result = self.search_article_and_get_info(search_keywords)
        print('result article list :', result)
        driver.close()
