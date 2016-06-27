# encoding: utf-8

import types
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative.api import DeclarativeMeta


not_dunder = lambda name: not name.startswith('__')


class ManagedQuery(Query):
    """Managed Query object"""

    def __init__(self, entities, *args, **kwargs):
        entity = entities[0]
        if isinstance(entity, DeclarativeMeta):
            if hasattr(entity, '__manager__'):
                manager_cls = entity.__manager__
                for fname in filter(not_dunder, dir(manager_cls)):
                    fn = getattr(manager_cls, fname)
                    setattr(self, fname, types.MethodType(fn, self))
        super(ManagedQuery, self).__init__(entities, *args, **kwargs)
