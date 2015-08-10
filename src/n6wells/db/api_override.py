"""
cut, pasted, and modified code from sqlalchemy.ext.declarative.api

everything here is a giant hack, but it seems to work
"""
import weakref
from sqlalchemy.ext.declarative import api # DeclarativeMeta, declarative_base


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


def declarative_base(bind=None, metadata=None, mapper=None, cls=object,
                     name='Base', constructor=api._declarative_constructor,
                     class_registry=None):
    """
    """
    lcl_metadata = api.MetaData()
    if bind:
        lcl_metadata.bind = bind

    if class_registry is None:
        class_registry = weakref.WeakValueDictionary()

    bases = not isinstance(cls, tuple) and (cls,) or cls
    class_dict = dict(_decl_class_registry=class_registry,
                      metadata=lcl_metadata)

    if constructor:
        class_dict['__init__'] = constructor
    if mapper:
        class_dict['__mapper_cls__'] = mapper

    return DeclarativeMeta(name, bases, class_dict)



