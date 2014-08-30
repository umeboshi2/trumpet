from pyramid.request import Request
from pyramid.decorator import reify


class AlchemyRequest(Request):
    @reify
    def db(self):
        maker = self.registry.settings['db.sessionmaker']
        session = maker()
        def close_session(request):
            if request.exception is not None:
                session.rollback()
            else:
                session.commit()
            session.close()
        self.add_finished_callback(close_session)
        return session
    
