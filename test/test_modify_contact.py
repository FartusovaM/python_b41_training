import time

from model.contact import Contact
import random


def test_modify_contact_firstname(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="new_preconditions"))
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    edited_contact = Contact(firstname="new_firstname", lastname="new_lastname")
    app.contact.modify_contact_by_id(contact.id, edited_contact)
    new_contacts = db.get_contact_list()
    contact_index = old_contacts.index(contact)
    old_contacts[contact_index] = edited_contact
    assert len(old_contacts) == len(new_contacts)
    assert new_contacts == old_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)