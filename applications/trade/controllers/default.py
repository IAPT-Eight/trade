# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
	if request.args(0) == None:
		search_vals = None
	else: 
		search_vals = request.args(0).split('_')
		
	
	categories_as_dicts = db(db.category).select(db.category.name).as_list()
	categories_as_list = [cat['name'] for cat in categories_as_dicts]
	
	items = None
	return dict(search_vals=search_vals, categories=categories_as_list, items=items)


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


