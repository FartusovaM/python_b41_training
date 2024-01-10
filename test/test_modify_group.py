from model.group import Group
import random


def test_modify_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(footer="group_preconditions"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    edited_group = Group(name="new_name", header="new_header", footer="new_footer")
    app.group.modify_group_by_id(group.id, edited_group)
    new_groups = db.get_group_list()
    group_index = old_groups.index(group)
    old_groups[group_index] = edited_group
    assert len(old_groups) == len(new_groups)
    assert new_groups == old_groups
    if check_ui:
        assert sorted(old_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)
