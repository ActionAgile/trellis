from datetime import datetime
from peewee import CharField, DateTimeField, FloatField, SqliteDatabase

db = SqliteDatabase('snapshots.db')


class Snapshot(db.Model):
    board_id = CharField()
    when = DateTimeField(default=datetime.now)
    cycle_time = FloatField()
    revenue = FloatField()
    spend = FloatField()
