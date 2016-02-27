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

def _number_of_waiting_proposals():
    if not auth.user_id:
        return None
    return db((db.trade_proposal.status==1)&(db.trade_proposal.receiver==auth.user_id))\
        .count()


search_form = FORM(
    DIV(
        DIV(
            INPUT(_name='search', _class="form-control",
              _placeholder="Search for items...", _autofocus="true", _id="search-bar",
              _value=request.args(0) if request.controller == "default" and request.function == "index" else ""),
            DIV(
                BUTTON(I(_class="fa fa-fw fa-search"), _type='submit', _class="btn btn-default"),
                _class="input-group-btn",
            ),
            _class="input-group",
        ),
        _class="form-group"
    ),
    _class="navbar-form navbar-left", _role="search"
)

##
#      <form class="navbar-form navbar-left" role="search">
#        <div class="form-group">
#          <input type="text" class="form-control" placeholder="Search">
#        </div>
#        <button type="submit" class="btn btn-default">Submit</button>
#      </form>

if search_form.process(hideerror=True, onfailure=None).accepted:
	redirect(URL('trade', 'default', 'index', vars = dict(q=[search_form.vars.search])))

number_of_proposals = _number_of_waiting_proposals()

response.menu = [
    (SPAN(I(_class="fa fa-fw fa-compass"), "Explore"), False, URL('trade', 'default', 'index')),
    (SPAN(
        SPAN(I(_class="fa fa-fw fa-clock-o"), "My Proposals"),
        SPAN(number_of_proposals, _class="badge", _style="margin-left: 5px;") if number_of_proposals else "",
    ), False, URL('trade', 'trade', 'index')),
    (SPAN(I(_class="fa fa-fw fa-user"), "My Profile"), False, URL('user', 'me')),
	(search_form, False, search_form.process()),
]

if auth.user:
    response.right_menu = [
        (SPAN(I(_class="fa fa-fw fa-sign-out"), "Sign out"), False, URL(c='user', f='user', args='logout')),
    ]
else:
    response.right_menu = [
        (SPAN(I(_class="fa fa-fw fa-sign-in"), "Sign in"), False, URL(c='user', f='user', args='login')),
        (SPAN(I(_class="fa fa-fw fa-plus-circle"), "Register"), False, URL(c='user', f='user', args='register')),
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
