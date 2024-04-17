from datetime import datetime

from django.core.management.base import BaseCommand
import requests as requests
from dateutil.relativedelta import relativedelta
from numpy import mean


class Statistic(BaseCommand):
    def get_data(self, params):
        URL = 'https://api.vk.com/method/wall.get'
        res = requests.get(URL, params=params).json()
        list_of_posts = []
        for inf in res['response']['items']:
            dict_for_post = {}
            dict_for_post['likes'] = inf['likes']['count']
            dict_for_post['views'] = inf['views']['count']
            list_of_photos = []
            post = []
            for d in inf['attachments']:
                if 'photo' in d.keys():
                    dict_for_post['create_date'] = datetime.fromtimestamp(d['photo']['date']).strftime('%Y-%m-%d')
                    for size in d['photo']['sizes']:
                        if size['type'] == 'x':
                            list_of_photos.append(size['url'])
            post.append(list_of_photos)
            post.append(dict_for_post)
            list_of_posts.append(post)
        return list_of_posts

    def filter(self, list_of_posts):
        relations = []
        date_gap = datetime.now() - relativedelta(years=1)
        date_gap.strftime('%Y-%m-%d')
        res_photos = []
        for post in list_of_posts:
            relation = post[1]['likes'] / post[1]['views']
            post.append(relation)
            relations.append(relation)
        avarage_ind = mean(relations)
        for post in list_of_posts:
            if post[2] > avarage_ind and post[1]['create_date'] > str(date_gap):
                res_photos.append(post[0])
        return res_photos
