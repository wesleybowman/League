import sys
import requests
from PySide import QtGui
#import pprint

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

def findChamp(champName,rdicts):
#    print 'Champ: {0}'.format(champName)
#    pprint.pprint((item['stats'] for item in rdicts if item['name'] ==
#                    champName).next())

    x= (item for item in rdicts if item['name'] ==
                  champName).next()

    return x

def findGametype(gameType, sumdicts):

#    print 'Game Type: {0}'.format(gameType)
#    pprint.pprint((item for item in sumdicts if item['playerStatSummaryType'] ==
#            gameType).next())

    x= (item for item in sumdicts if item['playerStatSummaryType'] ==
                  gameType).next()

    return x

def determineStatus(summaryStats,rankedStats):
    summaryStatus = summaryStats.status_code
    rankedStatus = rankedStats.status_code

    if summaryStatus==404:
        print 'Summoner Not Found'
        sys.exit(0)

    elif rankedStatus==404:
        #print 'No Ranked Information for Summoner Found'
        rankedStats = False
        return summaryStats,rankedStats

    else:
        return summaryStats,rankedStats


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.champs=[]
        self.initUI()

    def initUI(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog','Enter your name:')
        if ok:
            summonerName = text
            summaryStats, rankedStats = getURL(summonerName)
            summaryStats, rankedStats = determineStatus(summaryStats,rankedStats)

            if rankedStats == False:

                summaryText = eval(summaryStats.text)
                self.sumdicts = summaryText['playerStatSummaries']

                self.summon = QtGui.QLabel(summonerName, self)
                self.summary = QtGui.QLabel("Summary", self)
                self.noInfo = QtGui.QLabel("No Ranked Information for Summoner Found", self)
                self.summon.move(25, 2)
                self.summary.move(25, 20)
                self.noInfo.move(25, 35)

                self.game = QtGui.QLabel("Game Type", self)
                Gamecombo = QtGui.QComboBox(self)

                Gamecombo.move(50, 100)
                self.game.move(25, 50)

                self.gameInfo = QtGui.QTextEdit("Game Info", self)
                self.gameInfo.setGeometry(500,200,275,300)
                self.gameInfo.setReadOnly(True)
                self.gameInfo.move(25, 150)

                for item in self.sumdicts:
                    Gamecombo.addItem(item['playerStatSummaryType'])

                Gamecombo.activated[str].connect(self.onSum)

                self.setGeometry(300, 300, 300, 200)
                self.setWindowTitle('League of Legends Stats')
                self.show()

            else:

                summaryText = eval(summaryStats.text)
                rankedText = eval(rankedStats.text)
                self.sumdicts = summaryText['playerStatSummaries']
                self.rdicts = rankedText['champions']

                self.summon = QtGui.QLabel(summonerName, self)
                self.summon.move(50,2)

                self.champion = QtGui.QLabel("Champion", self)
                self.game = QtGui.QLabel("Game Type", self)

                self.gameInfo = QtGui.QTextEdit("Game Info", self)
                self.gameInfo.setGeometry(500,200,275,300)
                self.gameInfo.setReadOnly(True)

                self.champInfo = QtGui.QTextEdit("Champ Info", self)
                self.champInfo.setGeometry(500,200,275,300)
                self.champInfo.setReadOnly(True)

                Champcombo = QtGui.QComboBox(self)
                Gamecombo = QtGui.QComboBox(self)

                for item in self.rdicts:
                    Champcombo.addItem(item['name'])

                for item in self.sumdicts:
                    Gamecombo.addItem(item['playerStatSummaryType'])

                Champcombo.move(350,100)
                Gamecombo.move(50, 100)

                self.champion.move(350, 50)
                self.game.move(50, 50)
                self.gameInfo.move(50, 150)
                self.champInfo.move(350, 150)

                Champcombo.activated[str].connect(self.onRank)
                Gamecombo.activated[str].connect(self.onSum)

                self.setGeometry(300, 300, 300, 200)
                self.setWindowTitle('League of Legends Stats')
                self.show()

        else:
            sys.exit(0)

    def onSum(self, text):

        gameType = text
        x = findGametype(gameType, self.sumdicts)

        self.gameInfo.clear()

        for i,v in x.items():
            if type(v)==dict:
                text = '{}:'.format(i)
                self.gameInfo.append(text)
                #print i,':'
                for j,k in v.items():
                    text = '\t{0} : {1}'.format(j,k)
                    self.gameInfo.append(text)
                    #print '\t',j,k

            else:
                text = '{0} : {1}'.format(i,v)
                self.gameInfo.append(text)

    def onRank(self, text):

        champName = text
        x = findChamp(champName, self.rdicts)
        self.champInfo.clear()

        for i,v in x.items():
            if type(v)==dict:
                text = '{}:'.format(i)
                self.champInfo.append(text)
                #print i,':'
                for j,k in v.items():
                    text = '{0} : {1}'.format(j,k)
                    self.champInfo.append(text)
                    #print '\t',j,k

            else:
                text = '{0} : {1}'.format(i,v)
                self.champInfo.append(text)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    key = 'e7c98671-aaf5-4818-8bf4-6f47da218ede'
    main()
