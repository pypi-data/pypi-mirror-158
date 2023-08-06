from Jarticle.jProvider.jDate import jpDate
from Jarticle.jProvider.jCategories import jpCat
from Jarticle.jProvider.jSocial import jpSocial
from Jarticle.jProvider.jSearch import jpSearch

ARTICLES_COLLECTION = "articles"

"""
This is a Full Interface for ARTICLES collection in MongoDB.
- It will auto initialize connection to DB/Collection.
- You use this class direction.
Usage:
    - jp = jPro()
    - jp.get_article_count()
"""

class jPro(jpSearch, jpDate, jpCat, jpSocial):

    def __init__(self):
        self.construct_mcollection(ARTICLES_COLLECTION)

    def get_article_count(self):
        return self.get_document_count()

    def get_search(self, searchTerm):
        return self.search_all(search_term=searchTerm)

    def get_articles_by_key_value(self, kwargs):
        return self.base_query(kwargs=kwargs)

    def get_no_published_date(self, unlimited=False):
        return self.get_articles_no_date(unlimited=unlimited)

    def get_no_published_date_not_updated_today(self, unlimited=False):
        return self.get_articles_no_date_not_updated_today(unlimited=unlimited)

    def get_ready_to_enhance(self):
        temp = self.get_no_category_last_7_days()
        if temp:
            return temp
        temp2 = self.get_no_category_by_1000()
        if temp2:
            return temp2
        return False



if __name__ == '__main__':
    t = jPro()
    p = t.add_pub_date()
    # p = t.by_date_range_test()
    print(p)