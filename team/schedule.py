from bs4 import BeautifulSoup
import requests
import time
import unicodedata



def getTeamSchedule(teamName):

    # Make the proper url using the teamName
    url = f'https://www.basketball-reference.com/teams/{teamName}/2020_games.html'


    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the specific div
    div = str(soup.find_all('div',id='all_games')[0])

    # Get the commented out parts
    #div = div.replace('-->','')
    #div = div.replace('<--','')
    #div = div.replace('!--','')


    # Get uncommented parts and put it into beautiful soup again
    soup = BeautifulSoup(div,'html.parser')
    
    # Get the table
    #soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]
    
     # Get the headers from the table
    mainTableHeaders = [th.get_text().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats from the table
    teamStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')] for i in range(len(rows))]

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [row.find('th').text.replace(u'\xa0', u' ')]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        stats[row] = teamStats[counter]
        counter += 1


    return(stats)

