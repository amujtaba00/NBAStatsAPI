from bs4 import BeautifulSoup
import requests
import time
import unicodedata

def getTeamOnOff(teamName,year):
    
    # Construct proper URL
    url = f'https://www.basketball-reference.com/teams/{teamName}/{year}/on-off/'

    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    
    
    # Get the specific div
    div = str(soup.find_all('div',id='all_on_off')[0])

    # Get the commented out parts
    div = div.replace('-->','')
    div = div.replace('<--','')
    div = div.replace('!--','')


    # Get uncommented parts and put it into beautiful soup again
    soup = BeautifulSoup(div,'html.parser')
    
    # Get the table
    soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[1].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    playerStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')] for i in range(len(rows))]


    # Get row headers
    rowHeaders = []
    for row in rows:
        try:
            if row.find('th').text.strip() != 'Player':
                rowHeaders += [row.find('th').text]
        except AttributeError:
            pass

    # Create Dictionary
    stats = {}


    for stat in playerStats:
        if stat == [] or stat == ['']:
            playerStats.remove(stat)
        
    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        if row != '':
            stats[row] = {}
            stats[row]['On'] = playerStats[counter][1:]
            counter += 1
            stats[row]['Off'] = playerStats[counter][1:]
            counter += 1
            stats[row]['On-Off'] = playerStats[counter][1:]
            counter += 1


    print(stats)

    # Return the dictionaries
    return(stats)

