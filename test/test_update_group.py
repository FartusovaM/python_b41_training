from model.group import Group


def test_update_first_group(app):
    app.session.login(username="admin", password="secret")
    app.group.update_first_group(Group(name="update", header="update", footer="update"))
    app.session.logout()
