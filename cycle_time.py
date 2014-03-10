import requests
import grequests
import numpy as np
from dateutil.parser import parse

list_id = "52f2905117e567e02021b8b8"
app_key = "d55e4d19715539f767d6aead66698b02"
app_token = "883856e4130c37c1c49f4ffece87b4c60277330166642db73e46dd334adf4487"
list_url = "https://api.trello.com/1/lists/{}?fields=name&cards=open&card_fields=name&key={}&token={}"
action_url = "https://api.trello.com/1/cards/{}/actions?filter=updateCard:idList&fields=date&member_fields=initials&key={}&token={}"


def get_list_data(list_id):
    u = list_url.format(list_id, app_key, app_token)
    return requests.get(u).json()


def get_history_for_cards(cards):
    urls = [action_url.format(card.get('id'), app_key, app_token)
            for card in cards]
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)


def get_cycle_time(card_history, units='days'):
    dates = (x.get('date') for x in card_history.json())
    date_objects = sorted([parse(date) for date in dates])
    return getattr((date_objects[-1] - date_objects[0]), units)


def main():
    cards = get_list_data(list_id)
    card_histories = get_history_for_cards(cards.get('cards'))
    cycle_time = np.mean([get_cycle_time(card_history) for card_history in
                          card_histories])
    print "Cycle time is {} {}".format(cycle_time, 'days')


if __name__ == '__main__':
    main()
