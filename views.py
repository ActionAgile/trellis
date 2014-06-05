import models


def panic_json(options):
    import json
    data = []
    for ctr in models.CycleTime.select().where(models.CycleTime.list_id
                                               == options.list):
        data.append({"title": ctr.when.strftime('%d/%m/%y'),
                     'value': ctr.cycle_time})

    d = {"graph": {
            "title": options.title,
            "type": "line",
            "color": "orange",
            "refreshEveryNSeconds" : 120,
            "datasequences": [
                { "title": options.title,
                    "datapoints": data,
                }
            ]}
        }

    with open(options.outputfile, 'wb') as json_file:
        json_file.write(json.dumps(d, indent=4, sort_keys=True))