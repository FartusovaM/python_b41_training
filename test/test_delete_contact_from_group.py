from model.contact import Contact
from model.group import Group
import time
import random


def test_delete_contact_from_group(app, db):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="new_contact_preconditions"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="group_preconditions"))
        app.contact.go_to_home_page()
    all_groups = db.get_group_list()
    all_contacts = app.contact.get_contact_list()
    contact = random.choice(all_contacts)
    group = random.choice(all_groups)
    app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()
    if len(all_contacts_in_group) == 0:
        app.contact.go_to_home_page()
        app.contact.add_contact_to_group(contact.id, group.id)
        app.contact.go_to_home_page()
        app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()
    contact_in_group = random.choice(all_contacts_in_group)
    app.contact.select_contact_by_id(contact_in_group.id)
    app.contact.remove_from_group()
    app.contact.go_to_home_page()
    app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()
    assert sorted(all_contacts_in_group, key=Contact.id_or_max) == sorted(app.orm.get_contacts_in_group(group),
                                                                          key=Contact.id_or_max)
