def checkForCurrencies(text):
    text = text.lower()
    currency_keywords = {
        'USD': ['$', 'usd', 'dollar', 'dollor', 'dollr', 'dolr', 'dolar', 'dollir', 'dolir'],
        'RUB': ['₽', 'rubl', 'rub'],
        'EUR': ['€', 'eur', 'euro', 'yevro', 'evro', 'yeuro']
    }
    for key, values in currency_keywords.items():
        for word in values:
            if word in text:
                return key
    return False