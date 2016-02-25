def user():
    """
    This is the exposes the login and register functionality.
    """
    return dict(form=auth())

def view():
    """
    The page to view a user.

    The URL should be formed like this:
    /user/view/<username>/[<filter=filter_id>/]

    It shows information about the user and a preview of their items.
    Only the user can view items in their private collection.

    The items shown can be filtered depending by which list they are on.
    """
    username = request.args(0)

    if username is None:
        raise HTTP(422, "Username not provided")

    users_filter = request.vars['filter']
    if users_filter is not None:
        try:
            users_filter = int(users_filter)
        except ValueError:
            raise HTTP(422, "Filter type must be numeric")

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

    list_items = {list_type_id : items.find(lambda item: item.list_type == list_type_id) for list_type_id in LIST_NAMES_DICT.keys()}
    list_sizes = {list_type_id : len(list_items[list_type_id]) for list_type_id in LIST_NAMES_DICT.keys()}

    if users_filter is not None:
        try:
            items = list_items[users_filter]
        except KeyError:
            raise HTTP(422, "Unrecognised filter")

    return dict(user=user, items=items, is_users_page=is_users_page, list_sizes=list_sizes)

@auth.requires_login()
def me():
    """
    Redirects a logged in user to their own user page.
    """
    redirect(URL(c='user', f='view', args=auth.user.username))
