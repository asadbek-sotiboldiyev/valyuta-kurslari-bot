import json
import datetime
import requests as rq

API = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
TOP_CURRENCIES = [('USD', '🇺🇸'), ('RUB', '🇷🇺'), ('EUR', '🇪🇺'), ('KZT', '🇰🇿'), ('TRY', '🇹🇷'), ('CNY', '🇨🇳'), ('AED', '🇦🇪')]

def loadData():
    currencies = dict()
    with open('data.json', 'r') as file:
        json_data = json.load(file)
        expired_date = json_data['expired_date']
        data = json_data['data']
    if datetime.datetime.strptime(expired_date, '%d.%m.%Y').date() < datetime.date.today():
        print('Data has expired')
        data = updateCurrencies()
    for cc in data:
        currencies[cc['Ccy']] = cc
    return currencies

def updateCurrencies():
    currencies = rq.get(API).json()
    expired_date = currencies[0]['Date']
    new_data = dict()
    with open('data.json', 'w') as file:
        new_data['expired_date'] = expired_date
        new_data['data'] = currencies
        json.dump(new_data, file, indent=2)
    print('Data has updated')
    return currencies

def today():
    day, month, year = datetime.date.today().strftime('%d %m %Y').split()
    months = "Yanvar, Fevral, Mart, Aprel, May, Iyun, Iyul, Avgust, Sentabr, Oktabr, Noyabr, Dekabr".split(', ')
    return day + '-' + months[int(month)-1] + " " + year + "-yil"

def makeMessageAll(currencies, top_currencies):
    message_loop = ""
    for c, flag in top_currencies:
        message_loop += f"{flag}<b>{c}</b>:  {currencies[c]['Rate']} so'm {'↗️' if float(currencies[c]['Diff']) >= 0 else '↘️'}\n"
    message = f"{today()} uchun\nvalyuta kurslari.\n\n{message_loop}\nManba: <a href='https://t.me/centralbankuzbekistan'>Markaziy bank</a>"

    return message

def makeMessageOne(target):
    for c, flag in TOP_CURRENCIES:
        if c == target['Ccy']:
            return f"{today()} uchun\nvalyuta kursi.\n\n{flag}<b>{c}</b>:  {target['Rate']} so'm {'↗️' if float(target['Diff']) >= 0 else '↘️'}\n\nManba: <a href='https://t.me/centralbankuzbekistan'>Markaziy bank</a>"

def getCurrenciesMessage(data):
    return makeMessageAll(data, TOP_CURRENCIES)


if __name__ == '__main__':
    data = loadData()
    print(getCurrenciesMessage(data))