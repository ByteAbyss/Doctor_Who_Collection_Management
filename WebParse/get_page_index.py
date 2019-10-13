import requests
import re
from bs4 import BeautifulSoup
from collections import namedtuple

season_idx = namedtuple('season_idx', 'Type Season URL')
seasons = []

base_url = r'http://www.thedoctorwhosite.co.uk/doctorwho/episodes/'
page = requests.get('http://www.thedoctorwhosite.co.uk/doctorwho/episodes/')
soup = BeautifulSoup(page.content, 'html.parser')


def get_seasons():
    who_index = 'html body.doctorwho div#body.clear-fix section ul.col-3.col-link-square.clear-fix li a'
    listing = soup.select(who_index)
    pattern = re.compile(r'Series|Season [0-9]{1,2}')

    for x in listing:
        for elem in x:
            mo = pattern.search(str(elem.string))
            if mo:
                if mo.string.split()[0] == 'Season':
                    seasons.append(season_idx('Season', int(mo.string.split()[1]),base_url + x.attrs['href']))
                else:
                    seasons.append(season_idx('Series', int(mo.string.split()[1]), base_url + x.attrs['href']))
    return seasons



