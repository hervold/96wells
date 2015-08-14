from flask import Flask
from n6wells.util.test import get_test_config
from n6wells.db import initdb, get_handle
from sqlalchemy.orm.exc import NoResultFound
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def get_obj( model_name, pk ):
    config = get_test_config()
    initdb(config['DB']['engine'])
    conn = get_handle()

    try:
        model = n6wells.db.__getattribute__(model_name)
    except AttributeError as e:
        return None, None

    try:
        obj = model.uniq_pk(pk)
    except NoResultFound:
        return model, None

    return model, obj


@app.route('/view/<model_name>/<int:pk>')
def get_dict(model_name, pk):

    model, obj = get_obj( model_name, pk )

    if model is None:
        return 'bad model', 404, None

    if obj is None:
        return 'bad pk', 404, None

    return json.dumps(obj.to_dict())


@app.route('/measure/<model_name>/<int:pk>')
def measure(model_name, pk):
    from n6wells.measure import Measurement

    model, obj = get_obj( model_name, pk )

    if model is None:
        return 'bad model', 404, None

    if obj is None:
        return 'bad pk', 404, None

    return json.dumps( Measurement.calc( model, obj ) )


if __name__ == "__main__":
    print('@@ __name__ =', __name__)
    app.run()
