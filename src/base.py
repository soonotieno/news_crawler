import time
from crawler import Crawler
from selenium.webdriver.common.keys import Keys


# 뉴스 크롤러 베이스 클래스
class BaseNewsCrawler(Crawler):

    def debug_article_scrape(self, article_info):
        format = f"현재 인덱스 포지션 : {self.index_position}\n"
        format += f"검색 키워드 : {article_info['current_keyword']}\n"
        format += f"제목 : {article_info['title']}\n"
        format += f"내용 : {article_info['content']}\n"
        format += f"URL : {article_info['article_url']}\n"
        format += f"언론사 : {article_info['press']}\n"
        format += f"이미지 : {article_info['image']}\n"
        format += f"배포일 : {article_info['publication_date']}\n"
        format += f"-------------------------------------------------------------------------"
        return format

    def input_search_keywords(self, search_keywords, index_position):
        driver = self.get_webdriver()
        xpath = self.get_xpath()
        search_box_xpath = xpath['search_box']
        search_box_elements = driver.find_elements_by_xpath(search_box_xpath)
        search_box_elements[0].clear()
        search_box_elements[0].send_keys(search_keywords[index_position])
        search_box_elements[0].send_keys(Keys.ENTER)
        time.sleep(2)

    def search_article_and_get_info(self, search_keywords):
        result_all_article_list = []
        while True:
            button_next = self.get_next_page_button_elements()
            self.scroll_down_to_end()
            result_article_per_page = self.get_article_info_per_page(search_keywords)
            result_all_article_list.extend(result_article_per_page.copy())
            if button_next:
                self.click_next_page_button()
            else:
                current_keyword_index = self.increase_index()
                if current_keyword_index >= len(search_keywords):
                    self.scroll_up_to_end()
                    return result_all_article_list.copy()
                else:
                    self.scroll_up_to_end()
                    self.input_search_keywords(search_keywords, current_keyword_index)

    def get_article_info_per_page(self, search_keywords):
        xpath = self.get_xpath()
        article_list_xpath = xpath['article_list_per_page']
        article_elements = self.find_elements_by_xpath(article_list_xpath)
        result_article_list = self.scrape_article_content(article_elements, search_keywords)
        return result_article_list

    def scrape_article_content(self, article_elements, search_keywords):
        article_info = {}
        articles_info = []
        current_index_position = self.index_position
        for article in article_elements:
            article_info['current_keyword'] = search_keywords[current_index_position]
            article_info['title'] = self.get_article_title(article)
            article_info['content'] = self.get_article_content(article)
            article_info['article_url'] = self.get_article_url(article)
            article_info['press'] = self.get_article_press(article)
            article_info['image'] = self.get_article_img(article)
            article_info['publication_date'] = self.get_article_publication_date(article)
            print(self.debug_article_scrape(article_info))
            articles_info.append(article_info.copy())
        return articles_info.copy()

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


# NFT 크롤러 베이스 클래스
class BaseNftCrawler(Crawler):
    def debug_nft_scrape(self, nft_info):
        format = f"랭킹 : {nft_info['ranking']}\n"
        format += f"이름 : {nft_info['collection_name']}\n"
        format += f"아이콘 : {nft_info['collection_icon']}\n"
        format += f"거래량 : {nft_info['volume']}\n"
        format += f"증감률(하루) : {nft_info['percentage_daily']}\n"
        format += f"증감률(일주일) : {nft_info['percentage_weekly']}\n"
        format += f"fool_price : {nft_info['fool_price']}\n"
        format += f"owners : {nft_info['owners']}\n"
        format += f"items : {nft_info['items']}\n"
        format += f"-------------------------------------------------------------------------"
        return format

    def get_nft_info_and_set_period(self, period_index_position):
        return self.get_nft_info_per_page(period_index_position)

    def get_nft_info_per_page(self, period_index_position):
        xpath = self.get_xpath()
        nft_list_xpath = xpath['nft_list_per_page']
        nft_elements = self.find_elements_by_xpath(nft_list_xpath)
        result_article_list = self.scrape_nft_content(nft_elements, period_index_position)
        return result_article_list

    def scrape_nft_content(self, nft_elements, period_index_position):
        nft_info = {}
        nfts_info = []
        for nft_element in nft_elements:
            nft_info['ranking'] = self.get_nft_ranking(nft_element)
            nft_info['collection_name'] = self.get_nft_collection_name(nft_element)
            nft_info['collection_icon'] = self.get_nft_collection_icon(nft_element)
            nft_info['volume'] = ""  # self.get_nft_volume(nft_element)
            nft_info['percentage_daily'] = ""  # self.get_percentage_daily(nft_element)
            nft_info['percentage_weekly'] = ""  # self.get_percentage_weekly(nft_element)
            nft_info['fool_price'] = ""  # self.self.get_nft_fool_price(nft_element)
            nft_info['owners'] = ""  # self.self.get_nft_owners(nft_element)
            nft_info['items'] = ""  # self.self.get_nft_items(nft_element)
            print(self.debug_nft_scrape(nft_info))
            nfts_info.append(nft_info.copy())
        return nfts_info.copy()

    def get_nft_ranking(self, nft_element):
        pass

    def get_nft_collection_name(self, nft_element):
        pass

    def get_nft_collection_icon(self, nft_element):
        pass

    def get_nft_volume(self, nft_element):
        pass

    def get_percentage_daily(self, nft_element):
        pass

    def get_percentage_weekly(self, nft_element):
        pass

    def get_nft_fool_price(self, nft_element):
        pass

    def get_nft_owners(self, nft_element):
        pass

    def get_nft_items(self, nft_element):
        pass

    def select_search_options(self):
        pass

