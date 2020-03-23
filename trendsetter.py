from pytrends.request import TrendReq
import googletrans as gt
import pandas as pd
import datetime
import warnings
from json import JSONDecodeError


class Trendsetter():

    def __init__(self, timezone=1, language='en-US'):
        """
        Args:
            timezone: timezone in hours
            language: language of interface, not important
        """
        self.tz = -60*timezone
        self.countries = {
            'united_states': ['US', 'en'],
            'united_kingdom': ['GB', 'en'],
            'australia': ['AU', 'en'],
            'germany': ['DE', 'de'],
            'france': ['FR', 'fr'],
            'italy': ['IT', 'it'],
            'japan': ['JP', 'ja'],
            'saudi_arabia': ['SA', 'ar'],
            'egypt': ['EG', 'ar'],
            # 'china': ['CN', 'zh-cn'],
            # 'iran': ['IR', 'ar'],
            'brazil': ['BR', 'pt'],
            'india': ['IN', 'hi'],
            'israel': ['IL', 'iw'],
            # 'spain': ['ES', 'es'],
            'mexico': ['MX', 'es'],
            'russia': ['RU', 'ru'],
            'south_korea': ['KR', 'ko'],
            'taiwan': ['TW', 'zh-tw'],
            'hong_kong': ['HK', 'zh-tw'],
            'thailand': ['TH', 'th'],
            'turkey': ['TR', 'tr'],
            'vietnam': ['VN', 'vi'],
        }
        self.countrycodes = {v[0]: k for k, v in self.countries.items()}
        self.trends = TrendReq(hl=language, tz=self.tz)
        self.translator = gt.Translator(
            service_urls=["translate.google.com", "translate.google.co.kr",
                          "translate.google.at", "translate.google.de",
                          "translate.google.ru", "translate.google.ch",
                          "translate.google.fr", "translate.google.es"])

    def browse_categories(self, levels=list()):
        """browse categories by list of index
        Args:
            levels: list, eg. [4,2]

        Returns:
            dataframe with child categories
        """
        cat = self.trends.categories()
        for i in levels:
            cat = cat['children'][i]

        print(cat['name'], ", id =", cat['id'])
        if 'children' in cat.keys():
            children = pd.DataFrame.from_dict(cat['children'])
            # children.index = children['id']
            return children

    def get_trending(self, country='united_states'):
        """
        get currently and daily trends for implemented countries

        Args:
            country: country name or country code

        Returns:
            {'trending': list, 'today': list}

        Raises:
            ValueError if country not supported
        """

        if country not in self.countries:
            if country in self.countrycodes:
                country = self.countrycodes[country]
            else:
                raise ValueError("Country not supported.")

        self.trending = {'trending': list(self.trends.trending_searches(pn=country)[0]),
                         'today': list(self.trends.today_searches(pn=self.countries[country][0]))}

        if self.countries[country][1] != 'en':
            try:
                self.trending_en = {
                    k+'_en': list(map(lambda t: t.text,
                                      self.translator.translate(v, dest='en', src=self.countries[country][1])))
                    for k, v in self.trending.items()
                }
                self.trending.update(self.trending_en)
            except JSONDecodeError:
                warnings.warn("google translate API limit reached")

        return self.trending

    def get_related(self, kw, timeframe='now 7-d', category=0, location='', gtype=''):

        if isinstance(timeframe, list):
            tf_str = ' '.join(timeframe)
        else:
            tf_str = timeframe

        self.trends.build_payload([kw], cat=category, timeframe=tf_str, geo=location, gprop=gtype)
        related_topics = self.trends.related_topics()[kw]
        related_topics = related_topics['top'].append(related_topics['rising'], ignore_index=True, sort=False)

        return related_topics

    def get_interest(self, kwds, timeframe='now 7-d', category=0, location='', gtype=''):
        """

        Args:
            kwds: list of up to 5 keywords
            timeframe: supported google format. or [t_start, t_end]; for daily output: 'YYYY-mm-dd',
                       for hourly output: 'YYYY-mm-ddThh'
            category:
            location: supported google location or country code
            google_product:

        Returns:
            DataFrame
        """
        if isinstance(kwds, str):
            kwds = [kwds]

        if isinstance(timeframe, list):
            tf_str = ' '.join(timeframe)
        else:
            tf_str = timeframe
            timeframe = timeframe.split(' ')

        if 'T' in tf_str:  # hourly data
            format_str = '%Y-%m-%dT%H'
        else:  # daily data
            format_str = '%Y-%m-%d'

        # needs improvement:
        if any(s in tf_str for s in ['now', 'today', 'all']):
            self.trends.build_payload(kwds, cat=category, timeframe=tf_str, geo=location, gprop=gtype)
            self.interest = self.trends.interest_over_time()
        else:
            t_start = datetime.datetime.strptime(timeframe[0], format_str)
            t_end = datetime.datetime.strptime(timeframe[1], format_str)
            if 'T' in tf_str and t_end-t_start >= datetime.timedelta(days=8):
                self.interest = self.trends.get_historical_interest(kwds,
                                                                    year_start=t_start.year, year_end=t_end.year,
                                                                    month_start=t_start.month, month_end=t_end.month,
                                                                    day_start=t_start.day, day_end=t_end.day,
                                                                    hour_start=t_start.hour, hour_end=t_end.hour,
                                                                    cat=category, geo=location, gprop=gtype, sleep=60)
            else:
                self.trends.build_payload(kwds, cat=category, timeframe=tf_str, geo=location, gprop=gtype)
                self.interest = self.trends.interest_over_time()
        return self.interest
