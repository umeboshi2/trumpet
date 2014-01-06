import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc


from trumpet.models.consultant import Client

class ClientManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(Client)

    def get(self, id):
        return self.query().get(id)

    def add(self, name, contact_id, address=None, description=None):
        with transaction.manager:
            c = Client(name, contact_id, address, description)
            self.session.add(c)
        return self.session.merge(c)

    def update(self, client, **kw):
        with transaction.manager:
            for key in kw:
                if key == 'contact':
                    client.contact_id = kw[key]
                else:
                    setattr(client, key, kw[key])
            client = self.session.merge(client)
        return client

    def delete(self, id):
        with transaction.manager:
            client = self.get(id)
            if client is not None:
                self.session.delete(client)

    def all(self):
        return self.query().all()

    
