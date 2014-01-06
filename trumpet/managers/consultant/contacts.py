import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc


from trumpet.models.consultant import Contact
from trumpet.models.consultant import ClientContact, GlobalContact
from trumpet.models.consultant import GroupContact, UserContact

import vobject

from trumpet.managers.util import parse_vcard_object, make_vcard


class ContactManager(object):
    def __init__(self, session):
        self.session = session
        self.base = Contact
        
    def query(self):
        return self.session.query(Contact)

    def get(self, id):
        return self.query().get(id)

    def add_contact(self, user_id, firstname, lastname=None, email=None,
                    phone=None):
        with transaction.manager:
            c = Contact(firstname, lastname, email, phone)
            self.session.add(c)
            c = self.session.merge(c)
            uc = UserContact()
            uc.contact_id = c.id
            uc.user_id = user_id
            self.session.add(uc)
        return self.session.merge(c)
    
    def update(self, contact, **kw):
        with transaction.manager:
            for key in kw:
                setattr(contact, key, kw[key])
            contact = self.session.merge(contact)
        return contact

    def delete(self, id):
        with transaction.manager:
            contact = self.get(id)
            if contact is not None:
                self.session.delete(contact)

    def all(self):
        return self.query().all()

    
    def make_global(self, id):
        with transaction.manager:
            c = GlobalContact(id)
            self.session.add(c)
        return self.session.merge(c)

    def make_user_contact(self, contact_id, user_id):
        with transaction.manager:
            c = UserContact()
            c.contact_id = contact_id
            c.user_id = user_id
            self.session.add(c)
        return self.session.merge(c)

    def make_group_contact(self, contact_id, group_id):
        with transaction.manager:
            c = UserContact()
            c.contact_id = contact_id
            c.group_id = group_id
            self.session.add(c)
        return self.session.merge(c)

    def get_global_query(self):
        q = self.session.query(Contact)
        return q.filter(Contact.id == GlobalContact.id)
        
    def get_all_global(self):
        q = self.get_global_query()
        return q.all()

    def get_by_user_query(self, user_id):
        q = self.session.query(Contact)
        q = q.filter(Contact.id == UserContact.contact_id)
        q = q.filter(UserContact.user_id == user_id)
        return q

    def get_by_user(self, user_id):
        q = self.get_by_user_query(user_id)
        return q.all()

    def get_by_group(self, group_id):
        q = self.session.query(Contact)
        q = q.filter(Contact.id == GroupContact.contact_id)
        q = q.filter(GroupContact.group_id == group_id)
        return q.all()

    def add_user_contact(self, user_id, firstname,
                         lastname=None, email=None, phone=None):
        c = self.add(firstname, lastname=lastname, email=email,
                     phone=phone)
        return self.make_user_contact(c.id, user_id)
        
    def delete_user_contact(self, user_id, contact_id):
        with transaction.manager:
            uc = self.session.query(UserContact).get((contact_id, user_id))
            if uc is not None:
                self.session.delete(uc)

                

    def export_contact(self, contact_id):
        c = self.get(id)
        vcf = make_vcard(c)
        return vcf


    def export_contacts(self, user_id=None):
        cards = list()
        q = self.query()
        if user_id is not None:
            q = q.filter(UserContact.user_id == user_id)
        for c in q.all():
            cards.append(make_vcard(c))
        return cards
        
    def export_user_contacts(self, user_id):
        return self.export_contacts(user_id=user_id)
    
    def export_all_contacts(self):
        return self.export_contacts(user_id=None)

    def import_contacts(self, user_id, stream):
        count = 0
        excluded = []
        for card in vobject.readComponents(stream):
            cfields = parse_vcard_object(card)
            try:
                self.add_user_contact(*cfields)
                count += 1
            except IntegrityError:
                excluded.append(card)
        return count, excluded
    
    

    
        
    
        
    
