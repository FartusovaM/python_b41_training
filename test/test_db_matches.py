from model.group import Group
from model.contact import Contact


def test_group_list(app, db):
    ui_list = app.group.get_group_list()

    def clean(group):
        return Group(id=group.id, name=group.name.strip())
    db_list = map(clean, db.get_group_list())
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)


def test_contacts_list(app, db):
    ui_list = app.contact.get_contact_list()

    def clean(contact):
        return Contact(id=contact.id, firstname=contact.firstname.strip(), lastname=contact.lastname.strip(), address=contact.address, home=contact.home, mobile=contact.mobile, work=contact.work, email=contact.email, email2=contact.email2, email3=contact.email3)

    db_list = map(clean, db.get_contact_list())
    print('db', sorted(db_list, key=Contact.id_or_max))
    assert sorted(ui_list, key=Contact.id_or_max) == sorted(db_list, key=Contact.id_or_max)
