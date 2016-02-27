
LIST_PUBLIC_COLLECTION = 1
LIST_WISH_LIST = 2
LIST_TRADING = 3
LIST_PRIVATE_COLLECTION = 4

LIST_NAMES = (
    (LIST_PUBLIC_COLLECTION, "Public Collection"),
    (LIST_WISH_LIST, "Wish List"),
    (LIST_TRADING, "Trading List"),
    (LIST_PRIVATE_COLLECTION, "Private Collection"),
)

LIST_NAMES_DICT = dict(LIST_NAMES)  # e.g. LIST_NAMES_DICT[LIST_WANT] == "Want List"

if db(db.list_item_type.id > 0).count() == 0:
    for id, name in LIST_NAMES_DICT.items():
        db.list_item_type.insert(id=id, name=name)
