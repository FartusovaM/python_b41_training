from model.group import Group


def test_modify_group_name(app):
    if app.group.count() == 0:
        app.group.create(Group(footer="group_preconditions"))
    app.group.modify_first_group(Group(name="modify_group_header"))


def test_modify_group_header(app):
    if app.group.count() == 0:
        app.group.create(Group(name="group_preconditions"))
    app.group.modify_first_group(Group(header="modify_group_header"))
