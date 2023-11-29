from model.group import Group


def test_delete_first_group(app):
    if app.group.count() == 0:
        app.group.create(Group(name="group_preconditions", header="group_preconditions", footer="group_preconditions"))
    app.group.delete_first_group()
