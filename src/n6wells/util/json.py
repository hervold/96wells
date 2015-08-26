import json as root_json
from datetime import datetime
from json import JSONEncoder


class EncoderPlus(JSONEncoder):
    def default(self, x):
        return str(x) \
            if isinstance(x, datetime) \
               else super(EncoderPlus,self).default(x)

def dumps(x):
    print('@@ in dumps')
    try:
        s = root_json.dumps(x, cls=EncoderPlus)
    except Exception as e:
        print('@@ foo:', e)
        return ''
    else:
        print('@@ dumps good:', s)
        return s
