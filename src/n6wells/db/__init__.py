print('@@ db.__init__')
from sqlalchemy import Column, ForeignKey, Table, \
    UniqueConstraint, PrimaryKeyConstraint, distinct, and_, or_, types, \
    Integer, BigInteger, String, Float, Boolean, DateTime, Time, Enum, Text, \
    create_engine, MetaData, \
    func as sql_func

from sqlalchemy.orm import sessionmaker, scoped_session, backref, foreign, \
        reconstructor, synonym, relationship

from sqlalchemy.orm.collections import InstrumentedList

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base, api
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
        if '__tablename__' not in dict_ or dict_['__tablename__'] not in cls.metadata.tables:
            if '_decl_class_registry' not in cls.__dict__:
                api._as_declarative(cls, classname, cls.__dict__)
            type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        api._add_attribute(cls, key, value)

Base = declarative_base(metaclass=DeclarativeMeta)

__all__ = ['BaseModel','Column', 'ForeignKey', 'Table',
           'UniqueConstraint', 'PrimaryKeyConstraint', 'distinct', 'and_', 'or_', 'types',
           'Integer','BigInteger','String','Float','Boolean','DateTime','Time','Text',
           'ENGINE_NAME','initdb','destroydb','backref','foreign','reconstructor',
           'NoResultFound','MultipleResultsFound',
           'synonym','relationship','sql_func',
           'DB','committer','querier']


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
            conn = get_handle()
            return conn.query(cls).filter(cls.name == name).one()

        def to_dict(self, seen=None):
                """
                generic implementation of function returning JSON-friendly
                dictionary representing object
                """
                if seen is None:
                    seen = set([self])
                elif self in seen:
                    return {'pk': self.pk,
                            '__class__': self.__class__.__name__}
                d = {'__class__': self.__class__.__name__}
                for attr_name in dir(self.__class__):
                        class_attr = self.__class__.__dict__.get(attr_name)
                        if isinstance( class_attr, InstrumentedAttribute ):
                                attr = self.__getattribute__(attr_name)
                                seen.add(attr)

                                l = []
                                try:
                                    if isinstance(attr,str):
                                        raise TypeError()
                                    for x in attr:
                                        try:
                                            l.append( x.to_dict(seen=seen) )
                                        except AttributeError:
                                            l.append( x )
                                except TypeError:
                                    try:
                                        d[attr_name] = attr.to_dict( seen=seen )
                                    except AttributeError:
                                        d[attr_name] = attr
                                else:
                                    d[attr_name] = l

                return d

def walk_mods( basepath ):
    """
    recursively walk module tree in order to visit every ORM object, while
    enforcing one class per table name restriction

    returns dict mapping class_name -> class
    """
    tables, tablename_check = {}, {}
    print('@@ walk_mods')
    for importer, modname, ispkg in pkgutil.walk_packages(basepath):
        mod_loc = importer.find_module(modname)
        fname = mod_loc.get_filename()

        mod = mod_loc.load_module(modname)
        for attr_name in dir(mod):
            attr = mod.__getattribute__(attr_name)
            if isinstance(attr, DeclarativeMeta):
                try:
                    tablename = attr.__tablename__
                except AttributeError:
                    # DeclarativeMeta base class and abstract base classes don't have
                    # tablenames
                    pass
                else:
                    tables[attr_name] = attr

                    if tablename in tablename_check:
                        assert tablename_check[tablename] == attr_name, \
                            'table name %s associated with multiple classes (%s and %s)' \
                            % (tablename, tablename_check[tablename], attr_name)
                    else:
                       tablename_check[tablename] = attr_name

    print('@@ tables:', tables)
    return tables


def register_tables( engine  ):
    """
    simply walk the package hierarchy, thus ensuring that declarative
    classes are registered

    currently, recursion is disabled, as it winds up walking everything
    thats ever imported, so make sure your models are exposed in the root
    package namespace (ie, n6wells.foo)
    """
    tables = walk_mods( importlib.__import__('n6wells').__path__ )
    for tname, t in Base.metadata.tables.items():
        for fk in t.foreign_keys:
            fk.use_alter=True
            fk.constraint.use_alter=True

    Base.metadata.create_all(bind=engine)

    for tablename, cls in tables.items():
        print('@@ tablename=%s, cls=%s' % (tablename, cls))
        globals()[tablename] = cls
        __all__.append( tablename )


def destroydb(_ENGINE_NAME):
    global ENGINE_NAME
    global Session

    assert ENGINE_NAME is None
    assert Session is None

    assert 'test' in _ENGINE_NAME

    engine = create_engine(_ENGINE_NAME, echo=False, pool_recycle=300)
    tables = walk_mods( importlib.__import__('n6wells').__path__ )
    Base.metadata.drop_all(bind=engine)


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

    if ENGINE_NAME is None:
        # we only want to do this once

        ENGINE_NAME = _ENGINE_NAME
        engine = create_engine(ENGINE_NAME, echo=False, pool_recycle=300)

        Session = sessionmaker(bind=engine)
        register_tables(engine)


class _DB:
    """
    wrap session object to enable lshift syntax
    """
    session = None
    read_only = True
    #__metaclass__ = MetaDB

    def __init__(self, session, read_only=True ):
        self.session = session
        self.read_only = read_only

    '''
    # FIXME: I'd much rather put the << syntax here
    @staticmethod
    def __lshift__():
        return db.commit()
    '''

    def __getattr__(self, k):
        if self.read_only and k != 'query':
            raise AttributeError('session in read-only mode does not support '+k)
        return self.session.__getattribute__(k)


def get_handle( read_only=True ):
     return _DB( Session(), read_only=read_only )

# FIXME: for the solution to this in Python2, see:
#   http://stackoverflow.com/questions/3301220/staticmethod-or-classmethod-decoration-on-magic-methods
# however, that doesn't seem to work in python3
class DB_typ:
    def __lshift__(self, db):
        db.commit()
DB = DB_typ()


def committer(f):
    def g(*args, **kwargs):
        db = get_handle(read_only=False)
        l = [db] + list(args)
        x = f( *l, **kwargs)
        return db
    return g


def querier(f):
    def g(*args, **kwargs):
        l = [get_handle(read_only=True)] + list(args)
        return f( *l, **kwargs)
    return g
