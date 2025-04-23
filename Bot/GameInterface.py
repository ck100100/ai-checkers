from Bot.Bot import BotMinMaxAB 
from Bot.BoardNode import BoardNode
from utils.types import Coordinates, Player

class GameInterface:
    __bot:BotMinMaxAB
    def __init__(self):
        self.__bot = BotMinMaxAB(Player.WHITE, 3)
        self.__bot.initialiseState(True)
        self.gameLoop()

    def gameLoop(self) -> None:
        opponentMove:bool = False
        while True:
            self.paintBoard()
            if opponentMove:
                self.getOpponentMove()
            else:
                self.makeBotMove()
            opponentMove = False if opponentMove else True

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