# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

search_form=FORM(
	INPUT(_name='search', requires=IS_NOT_EMPTY()),
	INPUT(_type='submit', _value='Search')
	)
	
if search_form.process(hideerror=True).accepted:
	redirect(URL('trade', 'default', 'index', args = [search_form.vars.search]))

response.menu = [
    (T('Explore'), False, URL('trade', 'default', 'index')),
    (T('My Proposals'), False, URL('trade', 'trade', 'index')),
	(search_form, False, search_form.process()),
    (T('My Profile'), False, URL('user', 'me')),
]

if auth.user:
    response.right_menu = [
        (T('Sign out'), False, URL(c='user', f='user', args='logout')),
    ]
else:
    response.right_menu = [
        (T('Sign in'), False, URL(c='user', f='user', args='login')),
        (T('Create account'), False, URL(c='user', f='user', args='register')),
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()