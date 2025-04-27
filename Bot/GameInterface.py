from Bot.Bot import BotMinMaxAB 
from Bot.BoardNode import BoardNode
from utils.types import Coordinates, Piece

class GameInterface:
    __bot:BotMinMaxAB
    __userPlayFirst = True
    def __init__(self):
        self.setSettings()
        self.__bot = BotMinMaxAB(Piece.WHITE if self.__userPlayFirst else Piece.RED, 3)
        # self.__bot.initialiseState(not self.__userPlayFirst)
        self.gameLoop()

    def setSettings(self):
        valid:bool = False
        while valid == False:
            res = input("Do you want to play first?[Y\\N]:")
            if(res == "Y"):
                self.__userPlayFirst = True
                valid = True
            elif res == "N":
                self.__userPlayFirst = False
                valid = True

    def gameLoop(self) -> None:
        while True:
            self.paintBoard()
            if self.__userPlayFirst:
                self.getOpponentMove()
            else:
                self.makeBotMove()
            self.__userPlayFirst = False if self.__userPlayFirst else True

    def paintBoard(self):
        print(self.__bot.getCurrentBoardState())

    def getOpponentMove(self):
        prevX = int(input("Enter prev x coordinates: "))
        prevY = int(input("Enter prev y coordinates: "))
        newX = int(input("Enter new x coordinates: "))
        newY = int(input("Enter new y coordinates: "))
        self.__bot.setOpponentMove(Coordinates(prevX, prevY), Coordinates(newX, newY))

    def makeBotMove(self):
        self.__bot.getBotMove()