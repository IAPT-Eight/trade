if db(db.category.id > 0).count() == 0:
    categories = ['Advertising and brand', 'Architectural', 'Art', 'Books and magazines',
                  'Clothing, fabric, textiles', 'Money and stamps', 'Film and television',
                  'Glass and pottery', 'Household items', 'Memorabilia', 'Music', 'Nature and animals',
                  'Sports', 'Technology', 'Themed', 'Toys and games', 'Other']
    for category in categories:
        db.category.insert(name=category)
