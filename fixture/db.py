import pymysql.cursors
from model.group import Group
from model.contact import Contact


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
        list = []
        try:
            cursor.execute("select id, firstname, lastname, address, home, mobile, work, email, email2, email3 from addressbook where deprecated='0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstname, lastname, address, home, mobile, work, email, email2, email3) = row
                all_emails_from_home_page = ':'.join(filter(lambda x: x != "" and x is not None, [email, email2, email3]))
                all_phones_from_home_page = ':'.join(filter(lambda x: x != "" and x is not None, [home, mobile, work]))
                list.append(Contact(id=str(id), firstname=firstname, lastname=lastname, address=address, email=email, email2=email2, email3=email3, home=home, mobile=mobile, work=work, all_phones_from_home_page=all_phones_from_home_page, all_emails_from_home_page=all_emails_from_home_page))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()
