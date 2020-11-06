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
        koef_list = []

        # TODO remove \n and name of the day
        date = day.find('div', {'class': 'heading-3'}).text.strip('\n')

        game_box = day.find('tr', {'class': 'td-row'})
        koefs = game_box.find_all('td', {'class': 'odd-td'})
        for koef in koefs:
            koef_val = koef.find('a', {'class': 'button'}).text.strip('\n')
            if koef_val == '—':
                koef_val = ''
            # slice breaking string
            koef_list.append(koef_val)

        game = game_box.find('a', {'class': 'link'}).find_all('span')
        try:
            # slice to remove "-" symbol
            owner = game[0].text[:-2]
            guest = game[1].text
            list_of_games.append(f'{date},{owner},{guest},{koef_list[0]},'
                                 f'{koef_list[1]},{koef_list[2]}')
        except Exception:
            pass

    return '\n'.join(list_of_games)


print(scrap())
