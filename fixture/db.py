import pymysql.cursors
from model.group import Group
from model.contact import Contact
import re


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, user=user, password=password, database=name, autocommit=True)

    def get_group_list(self):
        cursor = self.connection.cursor()
        list = []
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        cursor = self.connection.cursor()
        contact_list = []
        try:
            cursor.execute("select id, firstname, lastname, address, home, mobile, work, email, email2, email3, phone2 from addressbook where deprecated='0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstname, lastname, address, home, mobile, work, email, email2, email3, phone2) = row
                emails = list(filter(lambda x: x != "" and x is not None, [email, email2, email3]))
                all_emails_from_home_page = ':'.join(emails) if len(emails) else None
                phones = list(filter(lambda x: x != "" and x is not None, [home, mobile, work, phone2]))
                all_phones_from_home_page = ':'.join(map(lambda x: self.clear(x), phones)) if len(phones) else None
                contact_list.append(Contact(id=str(id), firstname=firstname, lastname=lastname, address=address or None, email=email, email2=email2, email3=email3, home=home, mobile=mobile, work=work, all_phones_from_home_page=all_phones_from_home_page, all_emails_from_home_page=all_emails_from_home_page))
        finally:
            cursor.close()
        return contact_list

    def destroy(self):
        self.connection.close()

    def clear(self, s):
        return re.sub(r"\(|\)|-", r"", s)
