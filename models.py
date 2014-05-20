from datetime import datetime
from peewee import *

db = SqliteDatabase('cycletimes.db')


class CycleTime(Model):
    list_id = CharField()
    when = DateTimeField()
    cycle_time = FloatField()

    def to_csv(self):
        return "{}, {}".format(self.when.strftime('%d/%m/%y'), self.cycle_time)
