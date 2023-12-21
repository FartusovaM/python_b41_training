import re
import random


def test_contacts_comparison_on_home_page(app):
    contact_list_from_home_page = app.contact.get_contact_list()
    index = random.randrange(len(contact_list_from_home_page))
    contact_from_home_page = contact_list_from_home_page[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.lastname == contact_from_edit_page.lastname
    assert contact_from_home_page.firstname == contact_from_edit_page.firstname
    assert contact_from_home_page.address == contact_from_edit_page.address
    assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)


def clear(s):
    return re.sub("[() -]", "", s)


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
