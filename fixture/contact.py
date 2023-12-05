from selenium.webdriver.support.ui import Select
from model.contact import Contact


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
        wd = self.app.wd
        self.app.open_home_page()
        # select first contact
        self.select_first_contact()
        # submit deletion
        wd.find_element_by_xpath(f"//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        self.contact_cache = None

    def modify_first_contact(self, new_group_data):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_first_contact()
        wd.find_element_by_xpath(f"//a//img[@title='Edit']").click()
        # fill contact form
        self.fill_contact_form(new_group_data)
        wd.find_element_by_name("update").click()
        self.go_to_home_page()
        self.contact_cache = None

    def select_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

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
        self.change_input_field_value("phone2", contact.phone2)
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
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for element in wd.find_elements_by_css_selector('table[id="maintable"] tr[name=entry]'):
                lastname = element.find_element_by_css_selector('td:nth-child(2)').text
                firstname = element.find_element_by_css_selector('td:nth-child(3)').text
                contact_id = element.find_element_by_name("selected[]").get_attribute("value")
                self.contact_cache.append(Contact(lastname=lastname, firstname=firstname, id=contact_id))
        return list(self.contact_cache)
