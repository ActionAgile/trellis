from optparse import OptionParser

import requests
import grequests

import numpy as np
from dateutil.parser import parse

import trello

import settings
import webbrowser


def print_lists_in_board(board_id):
    u = settings.BOARD_URL.format(board_id, settings.APP_KEY,
                                  settings.APP_TOKEN)
    lists = requests.get(u).json()
    for li in lists:
        print "{} - {}".format(li.get('name'), li.get("id"))


def get_list_data(list_id):
    u = settings.LIST_URL.format(list_id, settings.APP_KEY, settings.APP_TOKEN)
    return requests.get(u).json()


def get_history_for_cards(cards):
    urls = [settings.ACTION_URL.format(card.get('id'), settings.APP_KEY,
                                       settings.APP_TOKEN)
            for card in cards]
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)


def get_cycle_time(card_history, units='days'):
    dates = (x.get('date') for x in card_history.json())
    date_objects = sorted([parse(date) for date in dates])
    return getattr((date_objects[-1] - date_objects[0]), units)


def print_cycle_time(cards):
    card_histories = get_history_for_cards(cards.get('cards'))
    cycle_time = np.mean([get_cycle_time(card_history) for card_history in
                  card_histories])
    print "Cycle time is {} {}".format(cycle_time, 'days')


def main():
    if options.board:
        print print_lists_in_board(options.board)
        exit()

    elif options.list and "," in options.list:
        for li in options.list.split(","):
            cards = get_list_data(li)
            print_cycle_time(cards)
    elif options.key:
        t = trello.TrelloApi(settings.APP_KEY)
        webbrowser.open(t.get_token_url('cycle_time', expires='30days', write_access=False))
        exit()
    else:
        cards = get_list_data(options.list)
        print_cycle_time(cards)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-b', '--board',
                      help="The board ID to use")
    parser.add_option('-l', '--list',
                      help="The list ID to use (or comma separated list)")
    parser.add_option('-a', '--all',
                      help="Get a list of all boards.")
    parser.add_option('-k', '--key',
                      help="Application key (overrides one in settings.py)")
    (options, args) = parser.parse_args()
    main()
