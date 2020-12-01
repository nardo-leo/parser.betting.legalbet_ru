from datetime import datetime
import requests
from bs4 import BeautifulSoup


class LegalBetParser:

    def __init__(self, start_url):
        self.start_url = start_url
        self.today = datetime.date(datetime.now())

    def _get(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def make_header(self):
        header = 'date,owner,guest,koeff_1,koeff_2,koeff_3\n'
        with open(f'{self.today}_legalbet.csv', 'w', encoding='utf-8') as file:
            file.write(header)

    def run(self):
        soup = self._get(self.start_url)
        self.make_header()
        for event in self.parse(soup):
            self.save(event)

    def find_sport_type(self, games_day, sport_type: str):
        sport_raw = games_day.find('div', {'class': 'match-sport-type'})
        if sport_type == sport_raw.find('div', {'class': 'icon'}).text:
            games_table = sport_raw.findNext('table')
            games = games_table.find_all('tr', attrs={'class', 'td-row'})
            return games

    def parse(self, soup: BeautifulSoup) -> dict:
        games_days = soup.find_all('div', {'class': 'matches-table-block'})

        # parse every day
        for games_day in games_days:
            date = games_day.find('div',
                                  attrs={'class':
                                         'heading-3'}).text.split('\n')[0]
            games = self.find_sport_type(games_day, 'Футбол')

            # TODO try:
            for game in games:
                players = game.find('a',
                                    attrs={'class': 'link'}).findAll('span')
                koefs = []
                koefs_row = game.findAll('td', {'class': 'odd-td'})

                for koef in koefs_row:
                    try:
                        koef_val_raw = koef.find('a', {'class': 'button'}).text
                        koef_val = koef_val_raw.strip('\n')
                    # TODO which exception
                    except Exception:
                        koef_val = '—'

                    koefs.append(koef_val)

                game_data = {
                    'date': date,
                    'owner': players[0].text[:-2],
                    'guest': players[1].text,
                    'koefs': koefs
                }

                yield game_data

    def save(self, game_data: dict):
        with open(f'{self.today}_legalbet.csv', 'a', encoding='utf-8') as file:
            file.write(f"{game_data['date']},{game_data['owner']},\
                       {game_data['guest']},{game_data['koefs'][0]},\
                       {game_data['koefs'][1]},{game_data['koefs'][2]}\n")


if __name__ == '__main__':
    url = 'https://legalbet.ru/match-center/'
    parser = LegalBetParser(url)
    parser.run()
