# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## The homepage of the website
#########################################################################

def index():
	if request.vars.q == None or ''.join(request.vars.q.split()) == "":
		search_vals = None
		search_query = True
		limitby = (0, 100)
	else:
		search_vals = request.vars.q.split(' ')
		search_query = (db.item.name.contains(search_vals, all=False) or db.item.description.contains(search_vals, all=False))
		limitby = None

	if request.vars.cat == None:
		category_query = True
	else:
		category_query = db.category.name == request.vars.cat

	privacy_query = db.list_item_type != LIST_PRIVATE_COLLECTION
	list_join = db.list_item_type.id == db.item.list_type
	category_join = db.item.categories == db.category.id

	items = db(list_join & category_join & search_query & category_query & privacy_query).select(
		db.item.name, db.item.image, db.item.item_value, db.item.id, db.item.categories, limitby=limitby)

	categories_as_dicts = db(db.category).select(db.category.name).as_list()
	categories_as_list = [cat['name'] for cat in categories_as_dicts]
	
	return dict(search_vals=search_vals, categories=categories_as_list, items=items,
				current_category=request.vars.cat)


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


