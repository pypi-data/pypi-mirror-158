from Jarticle import JQ, F, A
from FDate import DATE
from FSON import DICT
from Q import Q
from Jarticle.jArticles import jArticles

"""
test = self.mcollection.aggregate(A.SORT_BY_DATE)
"""
class jpDate(jArticles):

    def add_pub_date(self):
        field_name = "pub_date"
        query = Q.FIELD_EXISTENCE(fieldName="pub_date", doesExist=False)
        results = self.base_query(query, limit=10000)
        newList = []
        for art in results:
            strDate = DICT.get("published_date", art, False)
            if not strDate:
                continue
            new_date = DATE.TO_DATETIME(strDate)
            art[field_name] = new_date
            newList.append(art)
        print(newList)
        self.replace_articles(newList)

    def by_date_range_test(self):
        less = "July 01 2022"
        greater = "December 25 2021"
        test = self.mcollection.aggregate(A.SORT_BY_DATE(greater, less))
        print(test)


    def get_last_day_not_empty(self):
        return self.get_articles_last_day_not_empty()

    def get_date_range_list(self, daysBack):
        daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
        tempListOfArticles = []
        for day in daysbacklist:
            tempArts = self.get_articles_by_date(day)
            tempListOfArticles.append(tempArts)
        return tempListOfArticles

    def get_articles_last_day_not_empty(self):
        startDate = self.get_now_date()
        last20Days = DATE.get_range_of_dates_by_day(startDate, daysBack=20)
        for date in last20Days:
            results = self.base_query(kwargs=JQ.DATE(date))
            if results:
                return results
        return False

    def get_articles_no_date(self, unlimited=False):
        if unlimited:
            return self.base_query_unlimited({"published_date": {"$eq": None}})
        return self.base_query({"published_date": {"$eq": None}})

    def get_articles_no_date_not_updated_today(self, unlimited=False):
        today = DATE.mongo_date_today_str()
        query1 = {"published_date": {"$eq": None}}
        query2 = Q.FIELD_EXISTENCE("updatedDate", False)
        query3 = Q.FIELD_NOT_EQUALS("updatedDate", today)
        masterQuery = Q.OR([Q.AND([query1, query2]), Q.AND([query1, query3])])
        if unlimited:
            return self.base_query_unlimited(masterQuery)
        return self.base_query(masterQuery)

    def get_articles_by_date(self, date, unlimited=False):
        if unlimited:
            return self.base_query_unlimited(kwargs=JQ.DATE(date))
        return self.base_query(kwargs=JQ.DATE(date))

    def get_articles_today(self):
        return self.base_query(kwargs=JQ.DATE(self.get_now_date()))

    def get_articles_by_date_source(self, date, source_term):
        query = JQ.SEARCH_FIELD_BY_DATE(date, F.SOURCE, source_term)
        return self.base_query(kwargs=query)

