import requests
from datetime import datetime
from bs4 import BeautifulSoup


today = datetime.date(datetime.now())


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
        date = day.find('div', {'class': 'heading-3'}).text.split('\n')
        game_box = day.findAll('tr', {'class': 'td-row'})

        # TODO one more loop for all event per day
        for game_row in game_box:

            game_link = game_row.find('a', {'class': 'link'})
            try:
                game = game_link.findAll('span')
            except Exception:
                game = ['', '']
            koef_row = game_row.findAll('td', {'class': 'odd-td'})

            for koef in koef_row:
                # find value
                try:
                    koef_val_raw = koef.find('a', {'class': 'button'}).text
                    koef_val = koef_val_raw.strip('\n')
                except Exception:
                    koef_val = ''
                koef_list.append(koef_val)

            try:
                # slice to remove "-" symbol
                owner = game[0].text[:-2]
                guest = game[1].text
                list_of_games.append(f'{date[0]},{owner},{guest},'
                                     f'{koef_list[0]},{koef_list[1]},'
                                     f'{koef_list[2]}')
            except Exception:
                pass

    return '\n'.join(list_of_games)


# write data to file
with open(f'{today}_legalbet.csv', 'w', encoding='utf-8') as f:
    f.write(scrap())
