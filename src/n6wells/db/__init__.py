print('@@ db.__init__')
from sqlalchemy import Column, ForeignKey, Table, \
    UniqueConstraint, PrimaryKeyConstraint, distinct, and_, or_, types, \
    Integer, BigInteger, String, Float, Boolean, DateTime, Time, Enum, \
    create_engine, MetaData

from sqlalchemy.orm import sessionmaker, scoped_session, backref, foreign, \
        reconstructor, synonym, relationship

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base, api
#from sqlalchemy.ext.declarative.api import DeclarativeMeta
#from .api_override import declarative_base, DeclarativeMeta
import importlib
import pkgutil

# sqlalchemy engine name, eg, sqlite:///:memory:
ENGINE_NAME = None

# actual db connection
engine = None

Session = None

class DeclarativeMeta(type):
    """
    the metaclass from which ORM model classes are derived
    """
    def __init__(cls, classname, bases, dict_):
        if '_decl_class_registry' not in cls.__dict__:
            api._as_declarative(cls, classname, cls.__dict__)
        type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        # this is the first attribute set:
        if key == '_sa_declared_attr_reg' and cls.__tablename__ in cls.metadata.tables:
            cls.metadata._remove_table(cls.__tablename__, cls.metadata.schema)
        api._add_attribute(cls, key, value)


Base = declarative_base(metaclass=DeclarativeMeta)

__all__ = ['BaseModel','Column', 'ForeignKey', 'Table',
           'UniqueConstraint', 'PrimaryKeyConstraint', 'distinct', 'and_', 'or_', 'types',
           'Integer','BigInteger','String','Float','Boolean','DateTime','Time',
           'ENGINE_NAME','initdb','get_handle','backref','foreign','reconstructor',
           'synonym','relationship']


# subclass of declarative base class with helper methods
class BaseModel(Base):
        """
        """
        __abstract__ = True

        @classmethod
        def uniq_pk(cls, pk):
            """
            """
            conn = get_handle()
            return conn.query(cls).filter(cls.pk == pk).one()

        @classmethod
        def uniq_name(cls, name):
            """
            """

        def to_dict(self):
                """
                generic implementation of function returning JSON-friendly
                dictionary representing object
                """
                d = {}
                for attr_name in dir(self.__class__):
                        class_attr = self.__class__.__dict__.get(attr_name)
                        if isinstance( class_attr, InstrumentedAttribute ):
                                attr = self.__getattribute__(attr_name)
                                try:
                                        d[attr_name] = attr.to_dict()
                                except AttributeError:
                                        d[attr_name] = attr
                return d

def walk_mods( basepath, seen=None, tables=None ):
    """
    recursively walk module tree in order to visit every ORM object

    similar to pkgutil.walk_packages, but I memoize based on filename
    in order to avoid re-importing, which can have unpleasant side-effects
    in SQLAlchemy land (ie, re-importing a declarative model is bad)
    """
    if seen is None:
        seen = set()
    if tables is None:
        tables = {}

    for importer, modname, ispkg in pkgutil.iter_modules(basepath):
        mod_loc = importer.find_module(modname)
        fname = mod_loc.get_filename()
        if fname in seen:
            continue
            
        seen.add( fname )

        mod = mod_loc.load_module(modname)
        for attr_name in dir(mod):
            attr = mod.__getattribute__(attr_name)
            if isinstance(attr, DeclarativeMeta):
                tables[attr_name] = attr

        if ispkg:
            walk_mods( mod.__path__, seen=seen, tables=tables )

    return tables


def register_tables( engine  ):
    """
    simply walk the package hierarchy, thus ensuring that declarative
    classes are registered

    currently, recursion is disabled, as it winds up walking everything
    thats ever imported, so make sure your models are exposed in the root
    package namespace (ie, n6wells.foo)
    """
    #tables = walk_mods('n6wells')
    tables = walk_mods( importlib.__import__('n6wells').__path__ )

    for tname, t in Base.metadata.tables.items():
        for fk in t.foreign_keys:
            fk.use_alter=True
            fk.constraint.use_alter=True

    Base.metadata.create_all(bind=engine)

    for tablename, cls in tables.items():
        print('@@ tablename:', tablename)
        globals()[tablename] = cls
        __all__.append( tablename )


def initdb( _ENGINE_NAME ) :
    """
    initialize database:

      1. create engine & session
      2. execute namespace hack that imports all subclasses of BaseModel,
         ie, all ORM objects, into this namespace

    """
    global engine
    global Session
    global ENGINE_NAME

    ENGINE_NAME = _ENGINE_NAME
    engine = create_engine(ENGINE_NAME, echo=False, pool_recycle=300)
    Session = sessionmaker(bind=engine)

    register_tables(engine)


def get_handle():
    return Session()
