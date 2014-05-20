from optparse import OptionParser

import requests
import grequests

import numpy as np
from dateutil.parser import parse

import trello

import settings
import webbrowser

import models


def print_lists_in_board(board_id):
    u = settings.BOARD_URL.format(board_id, settings.APP_KEY,
                                  settings.APP_TOKEN)
    lists = requests.get(u).json()
    for li in lists:
        print "{} - {}".format(li.get('name'), li.get("id"))


def count_cards_not_done_on_board(board_id, done_list_id):
    pass


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


def cycle_time(cards):
    card_histories = get_history_for_cards(cards.get('cards'))
    cycle_time = np.mean([get_cycle_time(card_history) for card_history in
                  card_histories])
    return cycle_time

def panic_csv(options):
    import csv
    with open(options.outputfile, 'wb') as csvfile:
        w = csv.writer(csvfile)
        w.writerow([options.title, 'Cycle Time'])
        for ctr in models.CycleTime.select().where(models.CycleTime.list_id == options.list):
            w.writerow(ctr.to_csv().split(','))

def panic_json(options):
    import json
    data = []
    for ctr in models.CycleTime.select().where(models.CycleTime.list_id == options.list):
        data.append({"title": ctr.when.strftime('%d/%m/%y'), 'value':ctr.cycle_time})


    d = {"graph": {
                "title": options.title,
                "type": "line",
                "color": "orange",
                "refreshEveryNSeconds" : 120,
                "datasequences": [
                    { "title": options.title,
                      "datapoints": data,
                    }
                ]
            }
        }
    with open(options.outputfile, 'wb') as json_file:
        json_file.write(json.dumps(d, indent=4, sort_keys=True))


def main(options):
    models.CycleTime.create_table(fail_silently=True)

    if options.board:
        print print_lists_in_board(options.board)
        exit()

    elif options.list and "," in options.list:
        for li in options.list.split(","):
            cards = get_list_data(li)
            print_cycle_time(cards)
    elif options.token:
        t = trello.TrelloApi(settings.APP_KEY)
        webbrowser.open(t.get_token_url('cycle_time', expires='30days', write_access=False))
        exit()
    else:
        cards = get_list_data(options.list)
        ct = cycle_time(cards)
        print ct
        if options.save:
            models.CycleTime.create(list_id=options.list, cycle_time=ct)
        if options.outputfile:
            panic_json(options)


def runner():
    parser = OptionParser()
    parser.add_option('-b', '--board',
                      help="The board ID to use")
    parser.add_option('-l', '--list',
                      help="The list ID to use (or comma separated list)")
    parser.add_option('-a', '--all',
                      help="Get a list of all boards.")
    parser.add_option('-t', '--token',
                      help="New application token (overrides one in settings.py)")
    parser.add_option('-s', '--save', default=True, action='store_true')
    parser.add_option('-o', '--outputfile', default="cycletime.csv")
    parser.add_option('--title', default='Cycle Time')
    (options, args) = parser.parse_args()
    main(options)
