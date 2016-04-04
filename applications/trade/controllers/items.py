from AwesomeForms import AwesomeSQLFORM
from gluon.utils import simple_hash

def _delete_token(delete_key, session_id=response.session_id):
    return simple_hash(delete_key + session_id, digest_alg='sha512')

def view_items():
    item_id = request.args(0)

    if item_id is None:
        raise HTTP(422, "Item ID must be provided")

    item = db.item[item_id]

    if not item:
        raise HTTP(404, "Item not found or you are not authorised to view it")

    response.title = item['name']

    is_in_active_trade = bool(db((
                                     (db.trade_proposal.receiver_items.contains(item.id))
                                     |(db.trade_proposal.sender_items.contains(item.id))
                                 )&(db.trade_proposal.status==WAITING)
                                  &((db.trade_proposal.receiver==auth.user)
                                    |(db.trade_proposal.sender==auth.user))).count())

    is_in_tradable_list = item['list_type'] == LIST_TRADING

    delete_url = None
    if item.owner_ref == auth.user_id:
        delete_token = _delete_token(item.delete_key)
        delete_url = URL('items', 'delete_item', vars={'id': item.id, 'token': delete_token})

    return dict(item=item, is_in_active_trade=is_in_active_trade,
                is_in_tradable_list=is_in_tradable_list, delete_url=delete_url)


@auth.requires_login()
def add_item():
    response.title = "Add New Item"
    additemform = AwesomeSQLFORM(
        db.item,
        fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'],
        submit_button='Create'
        )

    additemform.add_button("Cancel", URL('trade', 'user', 'view', args=auth.user.username))

    error_message = ''
    if additemform.accepts(request,session):
        session.flash = 'Item created'
        redirect(URL('trade', 'items', 'view_items', args=additemform.vars.id))
    elif additemform.errors:
        error_message = 'There was a problem with the form entry. Please see below for details.'
    else:
        response.flash = 'Please complete the form below to add an item to your collection'

    return dict(additemform=additemform, error_message=error_message)


@auth.requires_login()
def delete_item():
    item_id = request.vars.id
    delete_token = request.vars.token

    if item_id is None or delete_token is None:
        raise HTTP(422, "Item ID and delete token must be provided")

    item = db((db.item.owner_ref == auth.user_id) & (db.item.id == item_id)).select().first()
    expected_delete_token = _delete_token(item.delete_key if item else 'prevent_timing_attacks')

    if not item or expected_delete_token != delete_token:
        raise HTTP(404, "Item not found, you are not authorised to delete it, or the delete token did not match")

    del db.item[item_id]

    session.flash = "Item deleted"
    redirect(URL('trade', 'user', 'view', args=auth.user.username))


@auth.requires_login()
def update_item():
    response.title = "Update Item"
    url = URL('default', 'download', args=db.item.image)
    item = db((db.item.owner_ref == auth.user_id) & (db.item.id == request.args(0))).select().first()

    if not item:
        raise HTTP(404, "Item not found or you are not authorised to view it")

    updateitemform = AwesomeSQLFORM(db.item, item, fields=['name', 'item_value', 'category', 'list_type', 'description', 'image'], submit_button='Update', showid=False, upload=url, buttons=['submit', A("Cancel",_class='btn',_href=URL("items","view_items", args=request.args(0)))])

    updateitemform.add_button("Cancel", URL('trade', 'items', 'view_items', args=request.args(0)))

    error_message = ''
    if updateitemform.accepts(request,session):
        session.flash = 'Item updated'
        redirect(URL('trade', 'items', 'view_items', args=updateitemform.vars.id))
    elif updateitemform.errors:
        error_message = 'There was a problem with the form entry. Please see below for details.'
    else:
        response.flash = 'Please complete the form below to edit this item'

    return dict(updateitemform=updateitemform, error_message=error_message)
