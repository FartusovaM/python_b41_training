from selenium.webdriver.support.ui import Select
from model.contact import Contact
from model.group import Group
import re


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def create(self, contact):
        wd = self.app.wd
        # init contact creation
        wd.find_element_by_link_text("add new").click()
        self.fill_contact_form(contact)
        # submit contact creation
        wd.find_element_by_name("submit").click()
        self.go_to_home_page()
        self.contact_cache = None

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_contact_by_index(index)
        # submit deletion
        wd.find_element_by_xpath(f"//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        self.contact_cache = None

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_contact_by_id(id)
        # submit deletion
        wd.find_element_by_xpath(f"//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        self.contact_cache = None

    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def modify_first_contact(self):
        self.modify_contact_by_index(0)

    def modify_contact_by_index(self, index, new_group_data):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_contact_by_index(index)
        self.edit_contact_by_index(index)
        # fill contact form
        self.fill_contact_form(new_group_data)
        wd.find_element_by_name("update").click()
        self.go_to_home_page()
        self.contact_cache = None

    def modify_contact_by_id(self, id, new_group_data):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_contact_by_id(id)
        self.edit_contact_by_id(id)
        # fill contact form
        self.fill_contact_form(new_group_data)
        wd.find_element_by_name("update").click()
        self.go_to_home_page()
        self.contact_cache = None

    def edit_contact_by_id(self, id):
        wd = self.app.wd
        contact = wd.find_element_by_css_selector("table[id='maintable'] tr[name='entry']:has(input[id='%s'])" % id)
        contact.find_element_by_css_selector("a img[title='Edit']").click()

    def select_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def edit_contact_by_index(self, index):
        wd = self.app.wd
        contact = wd.find_elements_by_css_selector("table[id='maintable'] tr[name='entry']")[index]
        contact.find_element_by_css_selector("a img[title='Edit']").click()

    def go_to_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/index.php") or wd.current_url.endswith("/")):
            wd.find_element_by_link_text("home").click()

    def fill_contact_form(self, contact):
        self.change_input_field_value("firstname", contact.firstname)
        self.change_input_field_value("middlename", contact.middlename)
        self.change_input_field_value("lastname", contact.lastname)
        self.change_input_field_value("nickname", contact.nickname)
        self.change_input_field_value("title", contact.title)
        self.change_input_field_value("company", contact.company)
        self.change_input_field_value("address", contact.address)
        self.change_input_field_value("home", contact.home)
        self.change_input_field_value("mobile", contact.mobile)
        self.change_input_field_value("work", contact.work)
        self.change_input_field_value("fax", contact.fax)
        self.change_input_field_value("email", contact.email)
        self.change_input_field_value("email2", contact.email2)
        self.change_input_field_value("email3", contact.email3)
        self.change_input_field_value("homepage", contact.homepage)
        self.change_input_field_value("work", contact.work)
        self.change_date_value('bday', contact.bday)
        self.change_date_value('bmonth', contact.bmonth)
        self.change_input_field_value("byear", contact.byear)
        self.change_date_value('aday', contact.aday)
        self.change_date_value('amonth', contact.amonth)
        self.change_input_field_value("ayear", contact.ayear)
        self.change_input_field_value("address2", contact.address2)
        self.change_input_field_value("phone2", contact.secondaryphone)
        self.change_input_field_value("notes", contact.notes)

    def change_input_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_date_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)
            wd.find_element_by_xpath(f"//select[@name='{field_name}']//option[@value='{text}']").click()

    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            self.app.open_home_page()
            self.contact_cache = self.find_elements_in_list()
        return self.contact_cache

    def find_elements_in_list(self):
        wd = self.app.wd

        elements = []

        for row in wd.find_elements_by_name('entry'):
            cells = row.find_elements_by_tag_name("td")
            lastname = cells[1].text
            firstname = cells[2].text
            contact_id = cells[0].find_element_by_name("selected[]").get_attribute("value")
            address = cells[3].text
            all_emails = cells[4].text.replace("\n", ":")
            all_phones = cells[5].text.replace("\n", ":")
            elements.append(Contact(id=contact_id, lastname=lastname, firstname=firstname,
                                              address=address, all_emails_from_home_page=all_emails,
                                              all_phones_from_home_page=all_phones))
        return list(elements)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.edit_contact_by_index(index)
        firstname = wd.find_element_by_name('firstname').get_attribute('value')
        lastname = wd.find_element_by_name('lastname').get_attribute('value')
        id = wd.find_element_by_name('id').get_attribute('value')
        homephone = wd.find_element_by_name('home').get_attribute('value')
        mobilephone = wd.find_element_by_name('mobile').get_attribute('value')
        workphone = wd.find_element_by_name('work').get_attribute('value')
        secondaryphone = wd.find_element_by_name('phone2').get_attribute('value')
        address = wd.find_element_by_name('address').get_attribute('value')
        email = wd.find_element_by_name('email').get_attribute('value')
        email2 = wd.find_element_by_name('email2').get_attribute('value')
        email3 = wd.find_element_by_name('email3').get_attribute('value')
        return Contact(id=id, firstname=firstname, lastname=lastname, address=address,
                       home=homephone, mobile=mobilephone, work=workphone, secondaryphone=secondaryphone,
                       email=email, email2=email2, email3=email3)

    def add_contact_to_group(self):
        wd = self.app.wd
        wd.find_element_by_xpath(f"//input[@name='add']").click()

    def remove_from_group(self):
        wd = self.app.wd
        wd.find_element_by_xpath(f"//input[@name='remove']").click()

    def add(self, contact_id, group_id):
        self.select_contact_by_id(contact_id)
        self.select_group_in_list(group_id)
        self.add_contact_to_group()

    def select_group_in_filter(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath(f"//select[@name='group']").click()
        wd.find_element_by_xpath(f"//select[@name='group']//option[@value='%s']" % id).click()

    def select_group_in_list(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath(f"//select[@name='to_group']").click()
        wd.find_element_by_xpath(f"//select[@name='to_group']//option[@value='%s']" % id).click()
