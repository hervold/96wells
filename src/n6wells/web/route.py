from flask import Flask
from n6wells.util.test import get_test_config
from n6wells.db import initdb, get_handle
from sqlalchemy.orm.exc import NoResultFound
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/view/<model_name>/<int:pk>')
def show_post(model_name, pk):
    config = get_test_config()
    initdb(config['DB']['engine'])

    import n6wells.db

    conn = get_handle()

    from n6wells.db import Sample, SampleType
    st = SampleType(name='test')
    s = Sample(name='foo', sample_type=st)

    try:
        model = n6wells.db.__getattribute__(model_name)
    except AttributeError as e:
        return 'bad model', 404, None

    try:
        obj = model.uniq_pk(pk)
    except NoResultFound:
        return 'bad pk', 404, None

    return json.dumps(obj.to_dict())


if __name__ == "__main__":
    print('@@ __name__ =', __name__)
    app.run()
