from model.contact import Contact


def test_modify_contact_firstname(app):
    if app.contact.count() == 0:
        app.contact.create(Contact(firstname="new_preconditions"))
    app.contact.modify_first_contact(Contact(firstname="modify_contact_firstname"))
