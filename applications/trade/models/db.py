# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

from gluon.custom_import import track_changes
track_changes(True)

auth = Auth(db)
service = Service()
plugins = PluginManager()

auth.settings.controller = 'user'
auth.settings.login_url = URL(c='user', f='user', args='login')
auth.settings.logged_url = URL(c='user', f='me')
auth.settings.login_next = URL(c='user', f='me')
auth.settings.register_next = URL(c='user', f='me')

# Improve the error messages
auth.messages.invalid_email = 'Invalid email address. A valid email address has 2 parts separated by an @ symbol, such as john.smith@example.com'
auth.messages.invalid_login = 'Username and password combination not found'

# We decided to use the term 'Sign in' rather than 'Login'
auth.messages.login_disabled = 'Sign in disabled by administrator'
auth.messages.logged_in = 'Signed in'
auth.messages.logged_out = 'Signed out'

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

import string

class IS_NAME(object):
    def __init__(self):
        self.disallowed_characters = set(string.digits + '!@£$%^&*()¡€#¢∞§¶•ªº-=≠[];\\,./{}:"|<>?')

    def __call__(self, value):
        intersection = set(value) & self.disallowed_characters
        if intersection:
            return (value, "Username contains disallowed character(s): %s" % ', '.join(intersection))
        return (value, None)

auth.table_user().first_name.requires = [IS_NOT_EMPTY(error_message=auth.messages.is_empty), IS_NAME()]
auth.table_user().last_name.requires = [IS_NOT_EMPTY(error_message=auth.messages.is_empty), IS_NAME()]

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('category',
    Field('name', 'string'),
    format='%(name)s'
)

db.define_table('list_item_type',
    Field('name', 'string'),
    format='%(name)s'
)

db.define_table('item',
    Field('list_type', 'reference list_item_type', label='List Type *', comment=T(\
		"Lists show which items you want to trade and which items you don't want other users to be able to see. \
		Your Public Collection is for items you don't want to trade but can be seen by other users. \
		Your Wish List is for items you want to receive. \
		Your Trading List is for items you want to trade away. \
		Your Private Collection is for items that you don't want other users to be able to see.")),
    Field('name', 'string', requires=IS_LENGTH(minsize=1, maxsize=50),label='Name *'),
    Field('description', 'text', requires=IS_LENGTH(minsize=1, maxsize=8000, error_message='too small or too large! max limit is 8000 characters'),label='Description *'),
    Field('item_value', 'decimal(10, 2)', requires=IS_DECIMAL_IN_RANGE(minimum=0), label='Item Value (£) *'),
    Field('owner_ref', 'reference %s' % auth.settings.table_user_name, default=auth.user),
    Field('image', 'upload', requires=IS_IMAGE(minsize=(100, 100)), label='Image *',  comment=T("Minimum Size 100*100 pixels. \
		Formats Supported  are .png, .gif, .jpeg and .bmp.")),
    Field('category', 'reference category', label='Category *'),
    format='%(name)s'
)


db.define_table('trade_proposal',
    Field('status', 'integer'),
    Field('sender', 'reference %s' % auth.settings.table_user_name),
    Field('sender_items', 'list:reference item'),
    Field('receiver', 'reference %s' % auth.settings.table_user_name),
    Field('receiver_items', 'list:reference item'),
    Field('created', 'datetime', default=request.now, writable=False),
    Field('updated', 'datetime', default=request.now, update=request.now, writable=False),
)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
