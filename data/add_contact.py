import random
import string
from model.contact import Contact

constant = [
    Contact(firstname="firstname1", middlename="middlename1", lastname="lastname1"),
    Contact(firstname="firstname2", middlename="middlename2", lastname="lastname2")
]


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Contact(firstname="", middlename="", lastname="")] + [
    Contact(firstname=random_string("firstname", 10), middlename=random_string("middlename", 10), lastname=random_string("lastname", 10))
    for i in range(5)
]