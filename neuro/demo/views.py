# from django.shortcuts import render
from pprint import pprint

from neuro.demo.models import Posts
from neuro.demo.statistics import Statistic


def statistic():
    VK_token = ''
    params = {
        'owner_id': '161587060',
        'count': 10,
        'domain': 'aesteticrplace',
        'access_token': VK_token,
        'v': '5.131'
    }
    res_photos = Statistic.filter(Statistic.get_data(params))
    return res_photos


def import_data(res_photos):
    for set in res_photos:
        for photo in set:
            element = Posts(post_image=str(photo))
            element.save()


pprint(import_data(statistic()))

