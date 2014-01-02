import sys
import requests
import pprint
#from PySide.QtCore import *
#from PySide.QtGui import *
from PySide import QtGui


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
    print 'Champ: {0}'.format(champName)
    pprint.pprint((item['stats'] for item in rdicts if item['name'] ==
                    champName).next())

def findGametype(gameType, sumdicts):

    print 'Game Type: {0}'.format(gameType)
    pprint.pprint((item for item in sumdicts if item['playerStatSummaryType'] ==
            gameType).next())

def determineStatus(summaryStats,rankedStats):
    summaryStatus = summaryStats.status_code
    rankedStatus = rankedStats.status_code

    if summaryStatus==404:
        print 'Summoner Not Found'
        sys.exit(0)

    elif rankedStatus==404:
        print 'No Ranked Information for Summoner Found'
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

                self.summary = QtGui.QLabel("Summary", self)
                self.noInfo = QtGui.QLabel("No Ranked Information for Summoner Found", self)
                self.summary.move(25, 2)
                self.noInfo.move(25, 25)

                self.game = QtGui.QLabel("Game Type", self)
                Gamecombo = QtGui.QComboBox(self)

                Gamecombo.move(50, 100)
                self.game.move(25, 50)

                self.gameInfo = QtGui.QLabel("Info", self)
                self.gameInfo.move(25, 150)

                for item in self.sumdicts:
                    Gamecombo.addItem(item['playerStatSummaryType'])

                Gamecombo.activated[str].connect(self.onSum)

                self.setGeometry(300, 300, 300, 200)
                self.setWindowTitle('QtGui.QComboBox')
                self.show()

            else:

                summaryText = eval(summaryStats.text)
                rankedText = eval(rankedStats.text)
                self.sumdicts = summaryText['playerStatSummaries']
                self.rdicts = rankedText['champions']


                self.champion = QtGui.QLabel("Champion", self)
                self.game = QtGui.QLabel("Game Type", self)

                self.gameInfo = QtGui.QLabel("Game Info", self)
                self.champInfo = QtGui.QLabel("Champ Info", self)

                Champcombo = QtGui.QComboBox(self)
                Gamecombo = QtGui.QComboBox(self)

                for item in self.rdicts:
                    Champcombo.addItem(item['name'])

                for item in self.sumdicts:
                    Gamecombo.addItem(item['playerStatSummaryType'])

                Champcombo.move(250,100)
                Gamecombo.move(50, 100)

                self.champion.move(250, 50)
                self.game.move(50, 50)
                self.gameInfo.move(50, 150)
                self.champInfo.move(250, 150)


                Champcombo.activated[str].connect(self.onRank)
                Gamecombo.activated[str].connect(self.onSum)

                self.setGeometry(300, 300, 300, 200)
                self.setWindowTitle('QtGui.QComboBox')
                self.show()

        else:
            sys.exit(0)

    def onSum(self, text):

        gameType = text
        findGametype(gameType, self.sumdicts)

        self.gameInfo.setText(pprint.pprint((item for item in self.sumdicts if item['playerStatSummaryType'] ==
            gameType).next()))

        self.gameInfo.adjustSize()
        #self.game.setText(text)
        #self.game.adjustSize()

    def onRank(self, text):

        champName = text
        findChamp(champName, self.rdicts)
        self.champInfo.setText(pprint.pprint((item['stats'] for item in self.rdicts if item['name'] ==
                    champName).next()))
        self.champInfo.adjustSize()

        #self.champion.setText(text)
        #self.champion.adjustSize()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    key = 'e7c98671-aaf5-4818-8bf4-6f47da218ede'
    main()


    # Create the Qt Application
#    app = QApplication(sys.argv)
#    # Create and show the form
#    form = Form()
#    form.show()
#    # Run the main Qt loop
#    sys.exit(app.exec_())
