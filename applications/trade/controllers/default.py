# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## The homepage of the website
#########################################################################

def index():
	response.title = "Explore"
	
	if request.vars.q == None or ''.join(request.vars.q.split()) == "":
		search_vals = None
		search_query = True
	else:
		search_vals = request.vars.q.split(' ')
		search_query = (db.item.name.contains(search_vals, all=False) or db.item.description.contains(search_vals, all=False))

	if request.vars.cat == None:
		category_query = True
	else:
		category_query = db.category.name == request.vars.cat
		
	privacy_query = (db.item.list_type != LIST_PRIVATE_COLLECTION) | (db.item.owner_ref == auth.user_id)
	list_join = db.list_item_type.id == db.item.list_type
	category_join = db.item.category == db.category.id

	limitby = (0, 100)
	items = db(list_join & category_join & search_query & category_query & privacy_query).select(
		db.item.name, db.item.image, db.item.item_value, db.item.id, db.item.category, limitby=limitby)

	categories_as_dicts = db(db.category).select(db.category.name, db.category.id).as_list()

	all_items = db(list_join & category_join & privacy_query & search_query).select(
		db.item.name, db.item.image, db.item.item_value, db.item.id, db.item.category, limitby=limitby)
		
	for cat in categories_as_dicts:
		cat['count'] = len(all_items.find(lambda item: item.category == cat['id']))
	
	return dict(search_vals=search_vals, categories=categories_as_dicts, items=items, current_category=request.vars.cat)


#########################################################################
## Default methods
#########################################################################

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
