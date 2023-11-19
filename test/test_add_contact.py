# -*- coding: utf-8 -*-
from model.contact import Contact
from fixture.application import Application
import pytest


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_add_contact(app):
    app.login(usermane="admin", password="secret")
    app.create_contact(Contact(firstname="test", middlename="test", lastname="test", nickname="test", title="test", company="test", address="test", home="test", mobile="test", work="test", fax="test", email="test", email2="test", email3="test", homepage="test", byear="1900", ayear="2000", address2="test", phone2="test", notes="test", bday="1", bmonth="February", amonth="February", aday="1"))
    app.logout()


def test_add_empty_contact(app):
    app.login(usermane="admin", password="secret")
    app.create_contact(Contact(firstname="", middlename="", lastname="", nickname="", title="", company="", address="", home="", mobile="", work="", fax="", email="", email2="", email3="", homepage="", byear="", ayear="", address2="", phone2="", notes="", bday="1", bmonth="February", amonth="February", aday="1"))
    app.logout()
