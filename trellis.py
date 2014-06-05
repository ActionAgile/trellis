import requests
import grequests

import numpy as np
from dateutil.parser import parse

import settings


class Trellis(object):
    """
        Main class that does the API thingummy.
        We want to do it direct as we'll be making lots of calls
        around card history, so need to be able to make them in parallel.
    """

    def __init__(self, app_key, app_token, board_id):
        self.app_key = app_key
        self.app_token = app_token
        self.board_id = board_id

    def get_lists(self):
        url = settings.BOARD_URL.format(self.board_id, self.app_key,
                                        self.app_token)
        return requests.get(url).json()

    def _get_list_id_from_name(self, name):
        try:
            return [li.get('id') for li in self.get_lists()
                    if li.get('name') == name][0]
        except IndexError:
            pass

    def get_list_data(self, list_id):
        u = settings.LIST_URL.format(list_id, self.app_key, self.app_token)
        return requests.get(u).json()

    def _get_history_for_cards(self, cards):
        urls = [settings.ACTION_URL.format(card.get('id'), self.app_key,
                                           self.app_token)
                for card in cards]
        rs = (grequests.get(u) for u in urls)
        return grequests.map(rs)

    def _get_cycle_time(self, card_history, units='days'):
        dates = (x.get('date') for x in card_history.json())
        date_objects = sorted([parse(date) for date in dates])
        return getattr((date_objects[-1] - date_objects[0]), units)

    def cycle_time(self, cards):
        card_histories = self._get_history_for_cards(cards.get('cards'))
        cycle_time = np.mean([self._get_cycle_time(card_history)
                              for card_history in card_histories])
        return cycle_time

    def __repr__(self):
        return "<Trellis: {}>".format(self.app_token)
