def view_items():
    item_id = request.args(0)
    privacy_filter = (db.item.list_type != LIST_PRIVATE_COLLECTION) | (db.item.owner_ref == auth.user_id)

    if item_id is not None:
        items = db(privacy_filter & (db.item.id == item_id)).select()
    else:
        items = db(privacy_filter).select()

    if not items:
        raise HTTP(404, "Item not found or you are not authorised to view it")

    response.title= items[0]['name']
    return dict(items=items)


@auth.requires_login()
def add_item():
    response.title = "Add New Item"
    additemform = SQLFORM(
		db.item,
		fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'],
		submit_button='Create'
		)
    additemform.custom.widget.description.update(_placeholder="Maximum 8000 characters")
    additemform.custom.widget.category.update(_placeholder="Maximum 8000 characters")
    additemform.custom.widget.item_value.update(_placeholder="Enter a Numerical Value in Pounds")

    if additemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=additemform.vars.id))
    elif additemform.errors:
        response.flash = 'ERROR! All fields are required to be complete'
    else:
        response.flash = 'Please complete the form below to add an item to your collection'

    return dict(additemform=additemform)


@auth.requires_login()
def delete_item():
    response.title = "Delete Item"
    item = db.item(request.args(0))

    deleteitemform = SQLFORM(db.item, item, fields=['id'], submit_button='Delete', writable=False, deletable=True, showid=False)

    if deleteitemform.accepts(request,session):
        redirect(URL('trade', 'user', 'view', args=auth.user.username))

    elif deleteitemform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information.'

    return dict(deleteitemform=deleteitemform)


@auth.requires_login()
def update_item():
    response.title = "Update Item"
    db.item.category.requires = IS_IN_DB(db, 'category.id', db.category._format,orderby=db.category.id)
    url = URL('default', 'download', args=db.item.image)
    item = db.item(request.args(0))

    updateitemform = SQLFORM(db.item, item, fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'],submit_button='Update', showid=False, upload=url)

    updateitemform.custom.widget.description.update(_placeholder="Maximum 8000 characters")
    updateitemform.custom.widget.item_value.update(_placeholder="Enter a Numerical Value in Pounds")

    if updateitemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=updateitemform.vars.id))
    elif updateitemform.errors:
        response.flash = 'ERROR! One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to edit this item'

    return dict(updateitemform=updateitemform)
