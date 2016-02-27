from datetime import datetime


def _get_form_list(input_name, form):
    """
    Given the name of a multipart-form list,
     always returns a list of numeric IDs.
    """
    input_variable = "%s[]" % input_name
    if form.vars[input_variable] is None:
        return []
    elif isinstance(form.vars[input_variable], list):
        return [long(x) for x in form.vars[input_variable]]
    else:
        return [long(form.vars[input_variable])]


@auth.requires_login()
def index():
    """
    This is the "My Trades" (or alternative name) page.

    It shows any proposals pending acceptance from you,
     or any of your proposals you sent waiting to be accepted.
    """

    if request.vars.get('feedback') == 'declined':
        response.flash = "The offer was successfully declined."

    proposals = db(
                    (db.trade_proposal.sender == auth.user.id) | (db.trade_proposal.receiver == auth.user.id)
                   ).select(db.trade_proposal.ALL, orderby=db.trade_proposal.created)

    return {
        "proposals": proposals
    }


@auth.requires_login()
def new():
    """
    This is the "Propose a new trade" page.

    The URL should be formed like this:
    /trade/new/<user_id>/[<counter_propose_to_id>/]

    Where <user_id> (arg 0) is the ID of the User you want to trade with,
     and <counter_propose_to_id> (opt arg 1) is the ID of a trade you want
     to make a counter-proposal to (which pre-populates the form w/ the old stuff).
    """

    receiver = db.auth_user[request.args(0)]
    old_proposal = db.trade_proposal[request.args(1)]

    # Get the list of items that can be selected for the proposal.
    sender_items = db((db.item.owner_ref==auth.user)&(db.item.list_type==LIST_TRADING)).select(db.item.ALL)
    receiver_items = db((db.item.owner_ref==receiver)&(db.item.list_type==LIST_TRADING)).select(db.item.ALL)

    preselected_item = db.item[request.vars['preselect']]
    selected_sender_items = []
    selected_receiver_items = [preselected_item] if preselected_item else []

    if old_proposal:  # If counter-proposing, pre-select the items.
        selected_receiver_items = old_proposal.sender_items
        selected_sender_items = old_proposal.receiver_items

    proposal_form = FORM(
        DIV(
            DIV(
                DIV(  # Sender Items
                    LABEL(
                        "What would you like to give to %s?" % receiver.username,
                        _class="control-label"
                    ),
                    DIV(
                        P(
                            *[
                                P(LABEL(
                                    INPUT(
                                            _name="sender_items[]",
                                            _value=item.id,
                                            _type="checkbox",
                                            _checked=(item.id in [y.id for y in selected_sender_items]),
                                            requires=(
                                                IS_NOT_EMPTY(),
                                            )),
                                    item.name,
                                ),)
                                for item in sender_items
                            ]),
                        _class=""
                    ),
                    _class="form-group",
                ),
                _class="col-md-6",
            ),
            DIV(
                DIV(  # Receiver Items
                    LABEL(
                        "What would you like from %s?" % receiver.username,
                        _class="control-label"
                    ),
                    DIV(
                        P(
                            *[
                                P(LABEL(
                                    INPUT(
                                            _name="receiver_items[]",
                                            _value=item.id,
                                            _type="checkbox",
                                            _checked=(item.id in [y.id for y in selected_receiver_items]),
                                            requires=(
                                                IS_NOT_EMPTY(),
                                            )),
                                    item.name,
                                ),)
                                for item in receiver_items
                            ]),
                        _class=""
                    ),
                    _class="form-group",
                ),
                _class="col-md-6",
            ),
            _class="row"
        ),
        BUTTON(
            I(_class="fa fa-fw fa-check"),
            "Send this proposal",
            _type="submit",
            _class="btn btn-block btn-primary",
        ),
        record=None,
        keepvalues=True,
    )

    # If the form is completed and valid
    if proposal_form.accepts(request, session):

        # Collets all of the data for the proposal
        sender_item_ids = _get_form_list('sender_items', proposal_form)
        receiver_item_ids = _get_form_list('receiver_items', proposal_form)
        sender = auth.user
        receiver = receiver
        status = WAITING

        # Insert the proposal in the database
        db.trade_proposal.insert(
            status=status, sender=sender, receiver=receiver,
            sender_items=sender_item_ids, receiver_items=receiver_item_ids
        )

        # If this is a counter-proposal, decline the old.
        if old_proposal:
            old_proposal.update_record(
                status=DECLINED
            )

        redirect(URL('trade', 'trade', 'index'))

    return {
        "proposal_form": proposal_form
    }


@auth.requires_login()
def respond():
    """
    This action is used to respond to a proposal.

    The URL should be formed like either one of these:
    /trade/respond/<trade_proposal_id>/accept/
    /trade/respond/<trade_proposal_id>/decline/
    """

    proposal_id = request.args(0)
    proposal = db.trade_proposal[proposal_id]
    if not proposal:
        raise HTTP(404, "Proposal not found")

    if proposal.receiver.id != auth.user_id:
        raise HTTP(403, "Forbidden")

    action = request.args(1)

    if action == "accept":
        db.trade_proposal[proposal_id] = {"status": ACCEPTED, "updated": datetime.now()}
        redirect(URL(c='trade', f='success', args=[proposal_id]))

    elif action == "decline":
        db.trade_proposal[proposal_id] = {"status": DECLINED, "updated": datetime.now()}
        redirect(URL(c='trade', f='index', vars={"feedback": "declined"}))

    else:  # Invalid action.
        raise HTTP(400, "Bad request")


@auth.requires_login()
def success():
    """
    This is displayed after the trade is successful.
    """

    proposal_id = request.args(0)
    proposal = db.trade_proposal[proposal_id]

    if not proposal:
        raise HTTP(404, "Proposal not found")

    if proposal.receiver.id != auth.user_id and proposal.sender.id != auth.user_id:
        raise HTTP(403, "Forbidden")

    if proposal.status != ACCEPTED:
        raise HTTP(403, "Forbidden: Proposal not accepted")

    return {
        "proposal": proposal,
    }


def _number_of_pending_proposals(user_id):
    proposals = db((db.trade_proposal.status == WAITING) & (
                    (db.trade_proposal.sender == auth.user.id) | (db.trade_proposal.receiver == auth.user.id)
                )).select(db.trade_proposal.ALL, orderby=db.trade_proposal.created).count()
    return proposals

