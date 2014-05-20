from datetime import datetime
from random import randrange
import arrow
from models import *

start = datetime(2013, 11, 1, 12, 00)
end = datetime(2015, 5, 19, 12, 00)
CycleTime.create_table(fail_silently=True)
for r in arrow.Arrow.range('day', start, end):
    CycleTime.create(list_id="5361ee6f8f3465ab2ff70299", when=r.datetime, cycle_time=randrange(4, 20))
