import requests
import sys
import pprint
from PySide import QtGui

def findChamp(champName,rdicts):
    print 'Champ: {0}'.format(champName)
    pprint.pprint((item['stats'] for item in rdicts if item['name'] ==
                    champName).next())

def getURL(summonerName):
    url = 'https://prod.api.pvp.net/api/lol/na/v1.1/summoner/by-name/{1}?api_key={0}'.format(key,summonerName)

    r = requests.get(url)
    text = eval(r.text)

    summonerId = text['id']

    url = 'https://prod.api.pvp.net/api/lol/na/v1.2/stats/by-summoner/{1}/summary?api_key={0}'.format(key,summonerId)
    summaryStats = requests.get(url)

    url = 'https://prod.api.pvp.net/api/lol/na/v1.2/stats/by-summoner/{1}/ranked?api_key={0}'.format(key,summonerId)
    rankedStats = requests.get(url)

    return summaryStats, rankedStats


print '\n'
key = 'e7c98671-aaf5-4818-8bf4-6f47da218ede'

summonerName = 'ChaoticallyEvil'
#summonerName = 'Peetreee'

summaryStats, rankedStats = getURL(summonerName)

summaryStatus = summaryStats.status_code
rankedStatus = rankedStats.status_code

if summaryStatus==404:
    print 'Summoner Not Found'
    sys.exit(0)

elif rankedStatus==404:
    print 'No Ranked Information for Summoner Found'

    summaryText = eval(summaryStats.text)

    print '\n'
    print 'Summary'
    sumdicts = summaryText['playerStatSummaries']

    print 'Summary'
    gameTypes = ['Unranked']

    for gameType in gameTypes:
        print 'Game Type: {0}'.format(gameType)
        pprint.pprint((item for item in sumdicts if item['playerStatSummaryType'] ==
            gameType).next())


        y =pprint.pprint((item for item in sumdicts if item['playerStatSummaryType'] ==
            gameType).next())

        y
        x= (item for item in sumdicts if item['playerStatSummaryType'] ==
                  gameType).next()

        for i,v in x.items():
            print i,v
        #for item in sumdicts:
        #    print item


else:
    summaryText = eval(summaryStats.text)
    rankedText = eval(rankedStats.text)
    sumdicts = summaryText['playerStatSummaries']
    rdicts = rankedText['champions']

    print 'Summary'
    gameTypes = ['Unranked']

    gameTypes=[]
    for item in sumdicts:
        gameTypes.append(item['playerStatSummaryType'])


    for gameType in gameTypes:
        print 'Game Type: {0}'.format(gameType)
        pprint.pprint((item for item in sumdicts if item['playerStatSummaryType'] ==
            gameType).next())

    print '\n'
    print 'Ranked'


    champs = []
    for item in rdicts:
        champs.append(item['name'])

    champs = ['Combined','Katarina']

    for champ in champs:
        print '\n'
        champName = champ
        findChamp(champName, rdicts)



print '\n'


'''
Unranked
RankedSolo5x5
RankedTeam5x5
'''
