
WAITING = 1
ACCEPTED = 2
DECLINED = 3

STATES = (
    (WAITING, "Waiting"),
    (ACCEPTED, "Accepted"),
    (DECLINED, "Declined")
)

STATES_DICT = dict(STATES)  # e.g. STATES_DICT[WAITING] = "Waiting"
