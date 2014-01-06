from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.exc import IntegrityError
import transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class SerialBase(object):
    def serialize(self):
        data = dict()
        table = self.__table__
        for column in table.columns:
            name = column.name
            try:
                pytype = column.type.python_type
            except NotImplementedError:
                print "NOTIMPLEMENTEDERROR", column.type
            value = getattr(self, name)
            if pytype is datetime:
                value = value.isoformat()
            data[name] = value
        return data
    
                
    


def initialize_sql(engine, popfuns):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    for popfun in popfuns:
        print "popfun", popfun.__name__
        try:
            popfun()
        except IntegrityError:
            transaction.abort()
