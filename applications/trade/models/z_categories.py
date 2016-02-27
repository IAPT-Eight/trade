if db(db.category.id > 0).count() == 0:
    categories = ['Advertising and brand', 'Architectural', 'Art', 'Books, magazines, paper',
                  'Clothing, fabric, textiles', 'Coins, currency, stamps', 'Film and television',
                  'Glass and pottery', 'Household items', 'Memorabilia', 'Music', 'Nature and animals',
                  'Other', 'Sports', 'Technology', 'Themed', 'Toys and games']
    for category in categories:
        db.category.insert(name=category)
