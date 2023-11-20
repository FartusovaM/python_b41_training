from model.contact import Contact


def test_update_first_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.update_first_contact(Contact(firstname="upt", middlename="upt", lastname="upt", nickname="upt", title="upt", company="upt", address="upt", home="upt", mobile="upt", work="upt", fax="upt", email="upt", email2="upt", email3="upt", homepage="upt", byear="1900", ayear="2000", address2="upt", phone2="upt", notes="upt", bday="1", bmonth="February", amonth="February", aday="1"))
    app.session.logout()
