from datetime import datetime


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

    proposal_form = SQLFORM(db.trade_proposal, fields=[
        'sender_items', 'receiver_items',
    ])

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

