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



##
#      <form class="navbar-form navbar-left" role="search">
#        <div class="form-group">
#          <input type="text" class="form-control" placeholder="Search">
#        </div>
#        <button type="submit" class="btn btn-default">Submit</button>
#      </form>


number_of_proposals = _number_of_waiting_proposals()

response.menu = [
    (STRONG("Collectibles"), False, URL(c='default', f='index')),
    (SPAN(I(_class="fa fa-fw fa-compass"), "Explore"), False, URL('trade', 'default', 'index')),
    (SPAN(
        SPAN(I(_class="fa fa-fw fa-clock-o"), "My Proposals"),
        SPAN(number_of_proposals, _class="badge badge-notification", _style="margin-left: 5px;") if number_of_proposals else "",
        data={"toggle": "tooltip", "placement": "bottom"},
        _title=("You have %d pending proposal(s)" % number_of_proposals) if number_of_proposals else "",
    ), False, URL('trade', 'trade', 'index')),
    (SPAN(I(_class="fa fa-fw fa-user"), "My Profile"), False, URL('user', 'me')),
]

if auth.user:
    response.right_menu = [
        (SPAN(I(_class="fa fa-fw fa-plus-circle"), "Add New Item"), False, URL('trade', 'items', 'add_item')),
        (SPAN(I(_class="fa fa-fw fa-sign-out"), "Sign out"), False, URL(c='user', f='user', args='logout')),
    ]
else:
    response.right_menu = [
        (SPAN(I(_class="fa fa-fw fa-sign-in"), "Sign in"), False, URL(c='user', f='user', args='login')),
        (SPAN(I(_class="fa fa-fw fa-user-plus"), "Create Account"), False, URL(c='user', f='user', args='register')),
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
