from crawlers.crawler import Crawler

naver_search_options = {
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
        "next_page_button": "//*[@id='main_pack']/div[@class='api_sc_page_wrap']/div/a[@class='btn_next']",
        "search_box": "//*[@id='nx_query']",
    }
}

google_search_options = {
    "access_url": "https://www.google.com/search?q=%22%22&source=lnms&tbm=nws&sa=X",
    "sort_type": "korean_web",  # 관련도순:relation / 최신순:new / 오래된순:old
    "period_type": "daily",
    "xpath": {
        "sort_select_button": {
            "normal_web": "",
            "korean_web": "",
        },
        "option_button": "//*[@id='hdtb-tls']",
        "period_select_button": {
            "all": "",
            "daily": "",
            "weekly": "",
            "monthly": "",
            "yearly": "",
        },
        "article_list_per_page": "//*[@id='rso']/div",
        "next_page_button": "//*[@id='pnnext']",
        "search_box": "//*[@id='tsf']/div[1]/div[1]/div[2]/div[2]/div[2]/input",
    }
}

search_keyword_list = ['애플카', '도지코인', '한국정보공학']


class GetNaverNewsCrawler(Crawler):
    pass


def news_crawl():
    crawler = GetNaverNewsCrawler(search_keyword_list=search_keyword_list, search_options=naver_search_options)
    product_list = crawler.do_crawl()
    print(product_list)


if __name__ == '__main__':
    news_crawl()
