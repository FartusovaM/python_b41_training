from model.contact import Contact
from model.group import Group
import random


def test_delete_contact_from_group(app, db, orm):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="new_contact_preconditions"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="group_preconditions"))
        app.contact.go_to_home_page()

    all_groups = db.get_group_list()
    group = random.choice(all_groups)
    app.contact.go_to_home_page()
    app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()

    if len(all_contacts_in_group) == 0:
        app.contact.go_to_home_page()
        contacts_without_group = orm.get_contacts_without_group()
        if len(contacts_without_group) == 0:
            app.contact.create(Contact(firstname="new_contact_without_group"))
            contacts_without_group = orm.get_contacts_without_group()
        contact = random.choice(contacts_without_group)
        app.contact.add_contact_to_group(contact.id, group.id)
        app.contact.select_group_in_filter(group.id)
        all_contacts_in_group = app.contact.find_elements_in_list()

    contact_in_group = random.choice(all_contacts_in_group)
    app.contact.select_contact_by_id(contact_in_group.id)
    app.contact.remove_from_group()

    app.contact.select_group_in_filter(group.id)

    is_contact_on_page = app.contact.is_contact_on_page(contact_in_group.id)
    group = orm.get_contact_in_group_by_id(group, contact_in_group.id)
    assert group is None and is_contact_on_page is False
