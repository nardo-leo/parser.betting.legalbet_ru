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
        # make sport None
        sport = None

        # find date
        date = day.find('div', {'class': 'heading-3'}).text.split('\n')

        # find type of game
        sport_raw = day.find('div', {'class': 'match-sport-type'})
        sport = sport_raw.find('div', {'class': 'icon'}).text

        if sport == 'Футбол':
            # find target game container in day
            game_box = day.find('table', {'class': 'matches-tv-table'})
            # then games
            games = game_box.findAll('tr', {'class': 'td-row'})
            # one more loop for all events per day
            for game in games:

                # find comands names
                try:
                    game_link = game.find('a', {'class': 'link'})
                    players = game_link.findAll('span')
                except Exception:
                    pass

                # find koefs
                koef_list = []
                koef_row = game.findAll('td', {'class': 'odd-td'})

                for koef in koef_row:
                    # find value of koefs
                    try:
                        koef_val_raw = koef.find('a', {'class': 'button'}).text
                        koef_val = koef_val_raw.strip('\n')
                    except Exception:
                        koef_val = '—'

                    koef_list.append(koef_val)

                try:
                    # slice to remove "—" symbol
                    owner = players[0].text[:-2]
                    guest = players[1].text
                    list_of_games.append(f'{date[0]},{owner},{guest},'
                                         f'{koef_list[0]},{koef_list[1]},'
                                         f'{koef_list[2]}')
                except Exception:
                    pass

        # skip non target games
        else:
            pass

    return '\n'.join(list_of_games)


# write data to file
with open(f'{today}_legalbet.csv', 'w', encoding='utf-8') as f:
    f.write(scrap())
