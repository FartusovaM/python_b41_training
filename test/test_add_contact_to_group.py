from model.contact import Contact
from model.group import Group
import random


def test_add_contact_to_group(app, db, orm):
    app.contact.go_to_home_page()
    contacts_without_group = orm.get_contacts_without_group()

    if len(contacts_without_group) == 0:
        app.contact.create(Contact(firstname="new_contact_without_group"))
        contacts_without_group = orm.get_contacts_without_group()
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="group_preconditions"))
        app.contact.go_to_home_page()

    all_groups = db.get_group_list()
    contact = random.choice(contacts_without_group)
    group = random.choice(all_groups)

    app.contact.add_contact_to_group(contact.id, group.id)
    app.contact.select_group_in_filter(group.id)

    all_contacts_in_group = app.contact.find_elements_in_list()
    contact_from_ui = next((x for x in all_contacts_in_group if x.id == contact.id), None)

    assert contact_from_ui is not None

    contact_from_group = orm.get_contact_in_group_by_id(group, contact_from_ui.id)
    assert contact_from_ui == contact_from_group
