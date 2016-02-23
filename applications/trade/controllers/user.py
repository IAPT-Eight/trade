def user():
    return dict(form=auth())

def view():
    username = request.args(0)

    if username is None:
        raise HTTP(422, "Username not provided")

    results = db(auth.settings.table_user.username == username).select(auth.settings.table_user.id, auth.settings.table_user.username)

    if not results:
        raise HTTP(404, "User not found")

    assert(len(results) == 1)
    user = results[0]
    items = user.item.select(db.item.name, db.item.description, db.item.item_value, db.item.image)

    return dict(user=user, items=items)