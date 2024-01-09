from model.contact import Contact
from model.group import Group
import random


def test_add_contact_to_group(app, db):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="new_contact_preconditions"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="group_preconditions"))
    all_contacts = app.contact.get_contact_list()
    all_groups = db.get_group_list()
    contact = random.choice(all_contacts)
    group = random.choice(all_groups)
    app.contact.add(contact.id, group.id)
    app.contact.go_to_home_page()
    app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()
    assert sorted(all_contacts_in_group, key=Contact.id_or_max) == sorted(app.orm.get_contacts_in_group(group), key=Contact.id_or_max)
