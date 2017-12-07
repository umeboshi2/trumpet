from sqlalchemy.orm.exc import NoResultFound
import transaction


class BaseManager(object):
    def __init__(self, session):
        self.session = session

    def set_session(self, session):
        self.session = session

    def _range_filter(self, query, column, start, end):
        query = query.filter(column >= start)
        query = query.filter(column <= end)
        return query

    @property
    def query(self):
        # return self.session.query(self.dbmodel)
        raise NotImplementedError("Override me")

    def get(self, id):
        return self.query.get(id)

    def all(self):
        return self.query.all()

    def delete_everything(self):
        self.query.delete()

    def delete_everything_tm(self):
        with transaction.manager:
            self.delete_everything()


class GetByNameManager(BaseManager):
    def get_by_name_query(self, name):
        return self.query.filter_by(name=name)

    def get_by_name(self, name):
        q = self.get_by_name_query(name)
        try:
            return q.one()
        except NoResultFound:
            return None
