import re
import random
from model.contact import Contact


def test_contacts_comparison_on_home_page(app, db):
    ui_list = app.contact.get_contact_list()
    db_list = db.get_contact_list()
    assert sorted(ui_list, key=Contact.id_or_max) == sorted(db_list, key=Contact.id_or_max)


def clear(s):
    return re.sub(r"\n", r":", s)


def merge_phones_like_on_home_page(contact):
    array = list(filter(lambda x: x != "" and x is not None,
                                map(lambda x: clear(x), [contact.home, contact.mobile, contact.work, contact.secondaryphone])))
    if len(array) > 0:
        return '\n'.join(array)
    else:
        return ''


def merge_emails_like_on_home_page(contact):
    array = list(filter(lambda x: x != "" and x is not None, [contact.email, contact.email2, contact.email3]))
    if len(array) > 0:
        return '\n'.join(array)
    else:
        return ''