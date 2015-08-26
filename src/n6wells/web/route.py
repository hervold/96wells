from flask import Flask
from n6wells.util.test import get_test_config
from n6wells.db import initdb, get_handle
from sqlalchemy.orm.exc import NoResultFound
from n6wells.util import json
import n6wells.db
# for testing purposes (?)
from n6wells.container import fixtures
from n6wells.util.test import get_test_config


app = Flask(__name__)

def print_exc(f):
    def g(*args, **kwargs):
        print('@@ in dec')
        try:
            f(*args, **kwargs)
        except Exception as e:
            print('exception!!!')
            print(e)
            raise
    return g

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
        conn = get_handle()
        try:
            pks = [x.pk for x in conn.query(model)]
        except Exception as e:
            print(e)
        return 'bad pk %d; found %s' % (pk,pks), 404, None

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



def create():
    from n6wells.container import fixtures, Container, ContainerType, ContainerInst
    from n6wells.xaction import Xaction
    from n6wells.sample import Sample, SampleType, Plating

    config = get_test_config()
    initdb(config['DB']['engine'])

    fixtures.load()

    conn = get_handle()
    xaction = Xaction()
    typ1, typC = SampleType(name='patient'), SampleType(name='control')
    s1, s2 = Sample(sample_type=typ1), Sample(sample_type=typC)
    plate96_t = conn.query(ContainerType).filter(ContainerType.name=='Plate-96_well').one()
    plate = ContainerInst( name='my_plate', type=plate96_t )
    well1 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A01').one()
    well2 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A02').one()
    p1 = Plating( plate=plate, well=well1, sample=s1, xaction=xaction )
    p2 = Plating( plate=plate, well=well2, sample=s2, xaction=xaction )
    conn.add( p1 )
    conn.add( p2 )
    conn.commit()
    return plate

if __name__ == "__main__":
    create()
    app.run()
