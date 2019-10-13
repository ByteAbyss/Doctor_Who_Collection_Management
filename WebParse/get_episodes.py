#! /usr/bin/env python
import re
from WebParse import get_page_index as  idx
from DatabaseManagement.Who_DML import add_record
from DatabaseManagement.DataLookUp import last_episode

results = []

def get_episodes(Story_Aired=last_episode() or 0):
    """
    Parse through & extract story elements of each 'saga'
    ------ Use Parameters to limit what is attempted to be written --

    :param Story_Aired: > # of Sequential Sagas aired -- IE: Season 11 Last Episode Aired Saga 284 - Demons of Punjab
     -- Set to the highest number into database so it only attempts updates on new data --

    :return: Saga elements & pass to database to write Saga : PRIMARY KEY (Title, Series_Run) - Stop duplicates
    """

    actors = {'1': 'William Hartnell (1963–66)', '2': 'Patrick Troughton (1966–69)', '3': 'Jon Pertwee (1970–74)',
              '4': 'Tom Baker (1974–81)', '5': 'Peter Davison (1982–84)', '6': 'Colin Baker (1984–86)',
              '7': 'Sylvester McCoy (1987–89)', '8': 'Paul McGann (1996)', '9': 'Christopher Eccleston (2005)',
              '10': 'David Tennant (2005–10)', '11': 'Matt Smith (2010–13)', '12': 'Peter Capaldi (2014–17)',
              '13': 'Jodie Whittaker (2018–present)'}


    # Episode Element Matching
    ep_match = re.compile('Episodes: ([0-9]{1,2})', re.MULTILINE)
    ep_alt_match = re.compile('([0-9]{1,2} )Episodes', re.MULTILINE)
    doc_match = re.compile('Doctor: ([0-9]{1,2})')
    comp_match =  re.compile('(Companions):( .*)(Aliens)')
    mons_match = re.compile('(Aliens/Monsters:) (.*)(Setting:)')
    setting_match = re.compile('(Setting:) (.*)')

    story = 0
    for elem in idx.get_seasons():
        episodes = idx.requests.get(elem.URL)
        ep_soup = idx.BeautifulSoup(episodes.content, 'html.parser')
        episode = ep_soup.find_all('article')

        for item in episode:
            ep = [line.strip() for line in item.text.split('\n') if len(line) > 1]
            Title , Stats , Synopsis = ep[0], ep[1], '\n'.join(ep[3:])
            Season = elem.Season

            if elem.Type == 'Season':
                Version = 'Doctor Who - 1963'
            else:
                Version = 'Doctor Who - 2005'

            # Break Out Values in Stats / Set Defaults
            Episodes = ep_match.search(Stats) or ep_alt_match.search(Stats)
            if Episodes:
                Episodes = Episodes.group(1)
            else:
                Episodes = 'Not Listed'

            Doctor_Number = doc_match.search(Stats) or re.search('(N/A)', Stats)
            if Doctor_Number:
                Doctor_Number = Doctor_Number.group(1)
            else:
                Doctor_Number = 'Not Listed'

            Companions = comp_match.search(Stats)
            if Companions:
                Companions = Companions.group(2)
            else:
                Companions = 'Not Listed'

            Aliens = mons_match.search(Stats)
            if Aliens:
                Aliens = Aliens.group(2)
            else:
                Aliens = 'Not Listed'

            Setting = setting_match.search(Stats)
            if Setting:
                Setting = Setting.group(2)
            else:
                Setting = 'Somewhere in Time & Space'

            Actor = actors.get(str(Doctor_Number), 'Not Listed')
            story += 1

            if story > Story_Aired:
                results.append([Title , 'Series Run: '+Version, 'Season: '+str(Season), 'Story Aired: '+str(story),
                'Season URL : '+elem.URL, 'Episodes : '+str(Episodes), 'Doctor Incarnation: '+str(Doctor_Number),
                'Doctor Actor: '+Actor, 'Companions: '+Companions, 'Monster | Aliens : '+Aliens, 'Setting: '+Setting,
                'Synposis: '+Synopsis])

                add_record(Title, Version, Season, story, elem.URL, Episodes, Doctor_Number, Actor, Companions,
                           Aliens, Setting, Synopsis)

    if len(results) > 0:
        return results
    else:
        return '--- No New Results -----'
