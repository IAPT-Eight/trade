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

    item = items[0]
    is_in_active_trade = bool(db((
                                     (db.trade_proposal.receiver_items.contains(item.id))
                                     |(db.trade_proposal.sender_items.contains(item.id))
                                 )&(db.trade_proposal.status==WAITING)
                                  &(db.trade_proposal.receiver==auth.user)).count())

    return dict(items=items, is_in_active_trade=is_in_active_trade)


@auth.requires_login()
def add_item():
    response.title = "Add New Item"
    additemform = SQLFORM(
		db.item,
		fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'],
		submit_button='Create'
		)
    additemform.custom.widget.description.update(_placeholder="Maximum 8000 characters")

    additemform.custom.widget.item_value.update(_placeholder="Enter a Numerical Value in Pounds")

    if additemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=additemform.vars.id))
    elif additemform.errors:
        response.flash = 'There was a problem with the form entry. Please see below for details.'
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
        response.flash = 'There was a problem with the form entry. Please see below for details.'

    return dict(deleteitemform=deleteitemform)


@auth.requires_login()
def update_item():
    response.title = "Update Item"
    url = URL('default', 'download', args=db.item.image)
    item = db.item(request.args(0))

    db.item.image.comment += ' This will replace the existing image'

    updateitemform = SQLFORM(db.item, item, fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'], submit_button='Update', showid=False, upload=url)

    updateitemform.custom.widget.description.update(_placeholder="Maximum 8000 characters")
    updateitemform.custom.widget.item_value.update(_placeholder="Enter a Numerical Value in Pounds")

    if updateitemform.accepts(request,session):
        redirect(URL('trade', 'items', 'view_items', args=updateitemform.vars.id))
    elif updateitemform.errors:
        response.flash = 'There was a problem with the form entry. Please see below for details.'
    else:
        response.flash = 'Please complete the form below to edit this item'

    return dict(updateitemform=updateitemform)
