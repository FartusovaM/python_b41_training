from model.group import Group
from random import randrange


def test_modify_group_name(app):
    if app.group.count() == 0:
        app.group.create(Group(footer="group_preconditions"))
    old_groups = app.group.get_group_list()
    index = randrange(len(old_groups))
    group = Group(name="%s modify_group_header" % index)
    group.id = old_groups[index].id
    app.group.modify_group_by_index(index, group)
    assert len(old_groups) == app.group.count()
    new_groups = app.group.get_group_list()
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


# def test_modify_group_header(app):
#    if app.group.count() == 0:
#        app.group.create(Group(name="group_preconditions"))
#    old_groups = app.group.get_group_list()
#    app.group.modify_first_group(Group(header="modify_group_header"))
#    new_groups = app.group.get_group_list()
#    assert len(old_groups) == len(new_groups)
