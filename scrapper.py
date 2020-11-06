import requests
from bs4 import BeautifulSoup


def scrap():
    # result list
    list_of_games = []

    # read legalbet.ru page with games
    url = 'https://legalbet.ru/match-center/'
    r = requests.get(url)

    # convert page to plain text
    text = r.text

    # then beautify
    soup = BeautifulSoup(text, features='html.parser')
    all_games = soup.find('div', {'class': 'matches-page'})
    days = all_games.findAll('div', {'class': 'matches-table-block'})

    # parse every day
    for day in days:
        game_box = day.find('tr', {'class': 'td-row'})
        game = game_box.find('a', {'class': 'link'}).find_all('span')
        try:
            # slice to remove "-" symbol
            owner = game[0].text[:-2]
            guest = game[1].text
            list_of_games.append(f'{owner},{guest}')
        except Exception:
            pass

    return list_of_games


print(scrap())
