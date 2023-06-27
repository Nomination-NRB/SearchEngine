# -*- coding: utf-8 -*-
from index_module import IndexModule
from recommendation_module import RecommendationModule
from datetime import *
import urllib.request


def get_max_page(root):
    response = urllib.request.urlopen(root)
    html = str(response.read())
    html = html[html.find('var maxPage ='):]
    html = html[:html.find(';')]
    max_page = int(html[html.find('=') + 1:])
    return max_page


if __name__ == "__main__":
    print('-----start time: %s-----' % (datetime.today()))

    # 构建索引
    print('-----start indexing time: %s-----' % (datetime.today()))
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()

    # 推荐阅读
    print('-----start recommending time: %s-----' % (datetime.today()))
    rm = RecommendationModule('../config.ini', 'utf-8')
    rm.find_k_nearest(5, 25)
    print('-----finish time: %s-----' % (datetime.today()))
