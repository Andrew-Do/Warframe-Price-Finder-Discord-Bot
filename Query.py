from datetime import datetime
from bs4 import BeautifulSoup

import requests
import numpy
import json
import operator

class Query:
    def __init__(self, name, _isSetItem=False):
        Query.name = name

        Query._ERROR = False
        Query._isSet = False
        Query.setNames = []
        Query._isSetItem = _isSetItem

        Query._isMod = False
        Query.maxRank = 0

        Query.loaded_json = {}
        Query.focus = {}

        Query.sell2Days = []
        Query.sell30Days = []
        Query.sell2DaysMaxed = []
        Query.sell30DaysMaxed = []
        Query.dealOnline = []
        Query.dealOnlineMaxed = []

        Query.quotes = []
        Query.now = datetime.now()

    def quote(self):
        self.scrapeData()
        if not Query._ERROR:
            self.identify()
            self.filterData()
            self.processData()

    def scrapeData(self):
        r = self.query()
        if not Query._ERROR:
            soup = BeautifulSoup(r.text, "html.parser")
            Query.loaded_json = json.loads(soup.find("script", id="application-state").text.strip())
            Query.focus = Query.loaded_json['payload']['orders']

    def identify(self):
        if Query._isSetItem:
            return
        else:
            if 'mod_rank' in list(Query.focus)[0]:
                Query._isMod = True

                for node in Query.focus:
                    if node['mod_rank'] > Query.maxRank:
                        Query.maxRank = node['mod_rank']
                        if Query.maxRank == 10:
                            break
            else:
                temp = Query.loaded_json['include']['item']['items_in_set']
                for node in temp:
                    if not node['set_root']:
                        Query.setNames.append(node['en']['item_name'])

    def filterData(self):
        for node in Query.focus:
            if node['platform'] == 'pc':
                if node['order_type'] == 'sell':
                    age = (Query.now - datetime.strptime(node['last_update'].split('T')[0], '%Y-%m-%d') ).days
                    if age <= 15:
                        if Query._isMod:
                            if node['mod_rank'] == 0:
                                if age <= 2:
                                    Query.sell2Days.append(node['platinum'])
                                Query.sell30Days.append(node['platinum'])
                            elif node['mod_rank'] == Query.maxRank:
                                if age <= 2:
                                    Query.sell2DaysMaxed.append(node['platinum'])
                                Query.sell30DaysMaxed.append(node['platinum'])
                        else:
                            if age <= 2:
                                Query.sell2Days.append(node['platinum'])
                            Query.sell30Days.append(node['platinum'])

                if not node['user']['status'] == 'offline':
                    if Query._isMod:
                        if node['mod_rank'] == 0:
                            Query.dealOnline.append(node)
                        elif node['mod_rank'] == Query.maxRank:
                            Query.dealOnlineMaxed.append(node)
                    else:
                        Query.dealOnline.append(node)


    def processData(self):
        prices = [Query.sell2Days, Query.sell30Days]
        if Query._isMod:
            prices = [Query.sell2Days, Query.sell30Days, Query.sell2DaysMaxed, Query.sell30DaysMaxed]

        for price in prices:
            elements = numpy.array(price)
            mean = numpy.mean(elements, axis=0)
            sd = numpy.std(elements, axis=0)
            final_list = [x for x in price if (x > mean - 1 * sd)]
            final_list = [x for x in final_list if (x < mean + 1 * sd)]

            Query.quotes.append(numpy.amax(final_list).item())
            Query.quotes.append(int(numpy.median(final_list)))
            Query.quotes.append(numpy.amin(final_list).item())

        Query.dealOnline.sort(key=operator.itemgetter('platinum'))
        Query.dealOnlineMaxed.sort(key=operator.itemgetter('platinum'))



    def query(self):
        url = 'https://warframe.market/items/' + Query.name.lower().replace(' ', '_')
        urlTest = [url + '_set', url]

        for u in urlTest:
            r = requests.get(u, allow_redirects=False)
            if r.status_code != 404:
                if 'set' in u:
                    Query._isSet = True
                return r
        Query._ERROR = True