def view_items():
    item_id = request.args(0)
    privacy_filter = (db.item.list_type != LIST_PRIVATE_COLLECTION) | (db.item.owner_ref == auth.user_id)

    if item_id is not None:
        items = db(privacy_filter & (db.item.id == item_id)).select()
    else:
        items = db(privacy_filter).select()

    if not items:
        raise HTTP(404, "Item not found or you are not authorised to view it")

    return dict(items=items)


@auth.requires_login()
def add_item():
    additemform = SQLFORM(
		db.item, 
		fields=['name', 'item_value', 'category', 'list_type', 'description', 'image']
		)

    if additemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=additemform.vars.id))
    elif additemform.errors:
        response.flash = 'ERROR! All fields are required to be complete'
    else:
        response.flash = 'Please complete the form below to add an item to your collection'

    return dict(additemform=additemform)


@auth.requires_login()
def delete_item():
    url = URL('default', 'download', args=db.item.image)
    item = db.item(request.args(0))

    deleteitemform = SQLFORM(db.item, item, fields=['name', 'image'], ignore_rw=True, deletable=True, showid=False, upload=url)

    if deleteitemform.accepts(request,session):
        redirect(URL('trade', 'user', 'view', args=auth.user.username))

    elif deleteitemform.errors:
        response.flash = 'ERROR! One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Are you sure you want to Delete this Item. If yes, please tick the "Check to delete" box below and click on Submit.'

    return dict(deleteitemform=deleteitemform)


@auth.requires_login()
def update_item():
    db.item.description.widget = SQLFORM.widgets.text.widget
    url = URL('default', 'download', args=db.item.image)
    item = db.item(request.args(0))

    updateitemform = SQLFORM(db.item, item, fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'], showid=False, upload=url)

    if updateitemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=updateitemform.vars.id))
    elif updateitemform.errors:
        response.flash = 'ERROR! One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to edit this item'

    return dict(updateitemform=updateitemform)
