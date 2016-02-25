def user():
    return dict(form=auth())

def view():
    username = request.args(0)

    if username is None:
        raise HTTP(422, "Username not provided")

    results = db(auth.settings.table_user.username == username).select(auth.settings.table_user.id, auth.settings.table_user.username, auth.settings.table_user.first_name, auth.settings.table_user.last_name)

    if not results:
        raise HTTP(404, "User not found")

    assert(len(results) == 1)
    user = results[0]
    is_users_page = auth.user and username==auth.user.username

    item_filter = db.item.id > 0
    if not is_users_page:
        item_filter &= db.item.list_type != LIST_PRIVATE_COLLECTION

    items = user.item(item_filter).select(db.item.ALL)

    list_sizes = {list_type_id : len([item for item in items if item.list_type == list_type_id]) for list_type_id in LIST_NAMES_DICT.keys()}

    return dict(user=user, items=items, is_users_page=is_users_page, list_sizes=list_sizes)

@auth.requires_login()
def me():
    redirect(URL(c='user', f='view', args=auth.user.username))
