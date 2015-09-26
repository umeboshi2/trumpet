from datetime import datetime, date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.exc import IntegrityError
import transaction

#from chert.alchemy import Base

def make_scoped_session():
    return scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

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
            
DBSession = make_scoped_session()


