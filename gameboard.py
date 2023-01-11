import tkinter as tk
from functools import partial
import socket

class BoardClass:
    """BoardClass provides method to use and create the interface and also the method that used to run Tic Tac Toe"""
    window = 0
    hostAddress = 0
    hostPort = 0
    userName = 0
    otherPlayer = 0
    lastPlayer = 0
    numTotal = 0
    numWins = 0
    numTies = 0
    numLoss = 0
    move = 0
    socket = 0
    buttonList = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    boardList = [[' ', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]


    def __init__(self, name: str, move: str, socket: socket) -> None:
        """set up window and some basic buttons
            transform all variable to the type can be used in tk inter
            disable all board button for player2

            args:
                name: user's name that's going to be presented at the stats area's first line
                move: character presents your move
                socket: object to receive and send information with the other player"""
        self.setUpWindow()
        self.initTkVariable()
        self.createLabelAndEntry()
        self.createButton()
        self.runUI()
        self.move.set(move)
        self.userName.set(name)
        self.createStatsArea()
        self.socketSetUp(socket)
        if move == 'o' or move == 'O':
            for i in range(3):
                for j in range(3):
                    self.buttonList[i][j]['state'] = 'disabled'


    def socketSetUp(self, socket: socket) -> None:
        """create socket attribute for later information change with competitor"""
        self.socket = socket


    def runUI(self) -> None:
        """keep updating the interface"""
        self.window.update_idletasks()
        self.window.update()


    def initTkVariable(self) -> None:
        """Change all variable type then they can be used for tk interface"""
        self.hostAddress = tk.StringVar()
        self.hostPort = tk.IntVar()
        self.move = tk.StringVar()
        self.userName = tk.StringVar()
        self.numTotal = tk.IntVar()
        self.numTies = tk.IntVar()
        self.numWins = tk.IntVar()
        self.numLoss = tk.IntVar()
        self.otherPlayer = tk.StringVar()
        self.lastPlayer = tk.StringVar()

    def setUpWindow(self) -> None:
        """create interface"""
        self.window = tk.Tk()
        self.window.geometry('600x600')
        self.window.title('Tic Tac Toe')
        self.window.configure(background='LightSteelBlue')
        self.window.resizable(0, 0)


    def createLabelAndEntry(self) -> None:
        """create host address and port labels and entrys
            create last player's label and winner's label"""
        self.hostAddressEntry = tk.Entry(self.window, textvariable=self.hostAddress, width=10)
        self.hostAddressEntry.grid(row=0, column=4)
        self.AddressLabel = tk.Label(self.window, text='Please Enter The Host Address Here:')
        self.AddressLabel.grid(row=0, column=3)

        self.hostPortEntry = tk.Entry(self.window, textvariable=self.hostPort, width=10)
        self.hostPortEntry.grid(row=1, column=4)
        self.portLabel = tk.Label(self.window, text='Please Enter Your Port Number Here:')
        self.portLabel.grid(row=1, column=3)

        self.lastPlayer = tk.Label(self.window, text=self.lastPlayer.get())
        self.lastPlayer.grid(row=0, column=1)

        self.winner = tk.Label(self.window, text='winner:')
        self.winner.grid(row=4, column=1)


    def createButton(self) -> None:
        """create 9 board buttons, by clicking on the button, player can indicate occupation of the place"""
        self.quitButton = tk.Button(self.window, text='Quit', command=self.window.destroy)
        self.quitButton.grid(row=5, column=4)
        for row in range(3):
            for col in range(3):
                new_command = partial(self.changeBoardAndCheckWinner, row, col)
                self.buttonList[row][col] = tk.Button(self.window, text='', command=new_command, width=5, height=4)
                self.buttonList[row][col].grid(row=row + 1, column=col)


    def changeBoardAndCheckWinner(self, row, col) -> None:
        """Command for board button
            change the text of button to player's move character and disable all 9 buttons untill the player's next round arrive
            check if the updated board has a winner, """
        if self.move.get() == 'o' or self.move.get() == 'O':
            self.buttonList[row][col].config(text='O')
            self.boardList[row][col] = 'O'
        elif self.move.get() == 'x' or self.move.get() == 'X':
            self.buttonList[row][col].config(text='X')
            self.boardList[row][col] = 'X'

        for i in range(3):
            for j in range(3):
                self.buttonList[i][j]['state'] = 'disabled'

        self.lastPlayer.config(text=self.otherPlayer.get())
        self.socket.send(bytes('Move ' + str(row) + ' ' + str(col), 'ascii'))
        if self.isWinner() == True:
            self.numTotal.set(self.numTotal.get() + 1)
            self.numWins.set(self.numWins.get() + 1)
            self.winner.config(text='winner: ' + self.userName.get())
            if self.move.get() == 'x' or self.move.get() == 'X':
                self.createPlayAgainButton()
            self.createStatsArea()
            for i in range(3):
                for j in range(3):
                    self.buttonList[i][j]['state'] = 'disabled'
        elif self.boardIsFull() == True and self.isWinner() == False:
            self.numTotal.set(self.numTotal.get() + 1)
            self.numTies.set(self.numTies.get() + 1)
            self.winner.config(text='Tie')
            if self.move.get() == 'x' or self.move.get() == 'X':
                self.createPlayAgainButton()
            self.createStatsArea()
            for i in range(3):
                for j in range(3):
                    self.buttonList[i][j]['state'] = 'disabled'


    def createStatsArea(self) -> None:
        """Create a label displays user name, other player's n=ame, total number of games
            number of wins, loss and ties"""
        self.stats = tk.Label(self.window, text=f'Player: {self.userName.get()}\n\n'
                                                f'Player: {self.otherPlayer.get()}\n\n'
                                                f'Total number of games: {self.numTotal.get()}\n\n'
                                                f'Number of wins: {self.numWins.get()}\n\n'
                                                f'Number of ties: {self.numTies.get()}\n\n'
                                                f'Number of loss: {self.numLoss.get()}\n\n')
        self.stats.grid(row=4, column=3)


    def boardIsFull(self) -> bool:
        """Check whether the board is full."""
        emptyNum  = 9
        for rows in self.boardList:
            for col in rows:
                if col != ' ':
                    emptyNum -= 1
        if emptyNum == 0:
            return True
        else:
            return False


    def isWinner(self) -> bool:
        """Check if the last player win this game."""
        isWin = False
        for row in self.boardList:
            if row[0] == row[1] and row[0] == row[2] and row[0] != ' ':
                isWin = True

        for c in range(3):
            if self.boardList[0][c] == self.boardList[1][c] and self.boardList[0][c] == self.boardList[2][c] and self.boardList[0][c] != ' ':
                isWin = True

        if self.boardList[1][1] == self.boardList[0][0] and self.boardList[1][1] == self.boardList[2][2] and self.boardList[1][1] != ' ':
            isWin = True
        elif self.boardList[1][1] == self.boardList[0][2] and self.boardList[1][1] == self.boardList[2][0] and self.boardList[1][1] != ' ':
            isWin = True

        return isWin


    def createBindButton(self) -> None:
        """create bind button"""
        self.bind = tk.Button(self.window, text='Bind', command=self.bindSocket)
        self.bind.grid(row=2, column=3)


    def bindSocket(self) -> None:
        """command for bind button. By clicking a server socket will be bind. If error occurs during this process
            ifBindAgain function will be called.
            And before connect client, it will call ifAcceptConnectWindow to check if player2 wants to connect"""
        try:
            address = self.hostAddressEntry.get()
            port = int(self.hostPortEntry.get())
            self.socket.bind((address, port))
            self.bind.destroy()
            self.socket.listen(5)
            clientSocket, clientAddress = self.socket.accept()
            self.socket = clientSocket
            self.ifAcceptConnectWindow()
        except:
            self.ifBindAgain()


    def ifAcceptConnectWindow(self) -> None:
        """create a little window asking player2 if he/she wants to play
            yesButton will destroy the little window and back to normal playing process
            noButton will destry the little window and wait for player1 for his/her next move"""
        self.acceptWindow = tk.Toplevel(self.window)
        self.acceptWindow.title('if accept connection')
        self.info = tk.Label(self.acceptWindow, text='Do you want to accept the connection?')
        self.info.grid(row=0, column=1)
        self.yesButton = tk.Button(self.acceptWindow, text='Yes', command=self.acceptWindow.destroy)
        self.yesButton.grid(row=1, column=0)
        self.noButton = tk.Button(self.acceptWindow, text='No', command=lambda: [self.socket.send(bytes('reject', 'ascii')),
                                                                                 self.socket.close(),
                                                                                 self.acceptWindow.destroy()])
        self.noButton.grid(row=1, column=2)


    def ifBindAgain(self) -> None:
        """Create a little window displaying the error message and two buttons asking user to
            decide whether bind again."""
        self.failBindWindow = tk.Toplevel(self.window)
        self.failBindWindow.title('Bind Fail')
        self.errorInfo = tk.Label(self.failBindWindow, text='Unsuccessful Binding. Try Again?')
        self.errorInfo.grid(row=0, column=1)
        self.yesButton = tk.Button(self.failBindWindow, text='Yes', command=self.failBindWindow.destroy)
        self.yesButton.grid(row=1, column=0)
        self.noButton = tk.Button(self.failBindWindow, text='No', command=self.window.destroy)
        self.noButton.grid(row=1, column=2)

    def createConnectButton(self) -> None:
        """create connect button"""
        self.connect = tk.Button(self.window, text='Connect', command=self.connectSocketAndCreateNameEntry)
        self.connect.grid(row=2, column=3)


    def connectSocketAndCreateNameEntry(self) -> None:
        """command for connectButton. By clicking it, player1's socket will try to connect player2's.
            If failed, call the createFailConnectWindow function"""
        try:
            address = self.hostAddressEntry.get()
            port = int(self.hostPortEntry.get())
            self.socket.connect((address, port))
            self.connect.destroy()

            self.nameLabel = tk.Label(self.window, text='Enter Your Username Here:')
            self.nameLabel.grid(row=2, column=3)
            self.nameEntry = tk.Entry(self.window, textvariable=self.userName, width=10)
            self.nameEntry.grid(row=2, column=4)

            self.nameButton = tk.Button(self.window, text='Send', command=self.getAndSendName)
            self.nameButton.grid(row=3, column=3)
        except:
            self.createFailConnectWindow()


    def createNewConnectButton(self) -> None:
        """create a New ConnectButton"""
        self.connect = tk.Button(self.window, text='Connect', command=self.connectSocketAndCreateNameEntry)
        self.connect.grid(row=3, column=4)


    def createFailConnectWindow(self) -> None:
        """create a window displaying error message
             yesButton to close the little window
             noButton to close all windows for player1"""
        self.failConnectWindow = tk.Toplevel(self.window)
        self.failConnectWindow.title('Connect Fail')
        self.errorInfo = tk.Label(self.failConnectWindow, text='Unsuccessful Connection. Try Again?')
        self.errorInfo.grid(row=0, column=1)
        self.yesButton = tk.Button(self.failConnectWindow, text='Yes', command=self.failConnectWindow.destroy)
        self.yesButton.grid(row=1, column=0)
        self.noButton = tk.Button(self.failConnectWindow, text='No', command=self.window.destroy)
        self.noButton.grid(row=1, column=2)


    def getAndSendName(self) -> None:
        """check if the username is alphanumeric, if is, send it to player2
            if not, call createWarningwindow function"""
        try:
            for element in self.nameEntry.get():
                if ord(element) not in range(48, 58) and ord(element) not in range(65, 91) and ord(element) not in range(97,123):
                 raise ValueError
            self.nameButton.destroy()
            self.userName.set(self.nameEntry.get())
            self.lastPlayer.config(text=self.userName.get())
            self.createStatsArea()
            self.socket.send(bytes('Name' + ' ' + self.userName.get(), 'ascii'))
        except:
            self.createWarningWindow()


    def createWarningWindow(self) -> None:
        """create a little window displaying name error message
            okButton to close the little window"""
        self.warningWindow = tk.Toplevel(self.window)
        self.warningInfo = tk.Label(self.warningWindow, text='Please enter alphanumeric username.')
        self.warningInfo.grid(row=0, column=0)
        self.okButton = tk.Button(self.warningWindow, text="Ok", command=self.warningWindow.destroy)
        self.okButton.grid(row=1, column=0)


    def createPlayAgainButton(self) -> None:
        """create playAgainButton and stopPlayButton"""
        self.playAgainButton = tk.Button(self.window, text='Play Again', command=self.playAgain)
        self.playAgainButton.grid(row=3, column=3)

        self.stopPlayButton = tk.Button(self.window, text='Stop Play', command=self.stopPlay)
        self.stopPlayButton.grid(row=3, column=4)


    def playAgain(self) -> None:
        """command for playAgainButton. it will destroy both playAgainButton and StopPlay button
            and send play again message to player 2"""
        self.stopPlayButton.destroy()
        self.playAgainButton.destroy()
        self.resetBoard()
        self.socket.send(bytes('Play Again', 'ascii'))


    def stopPlay(self) -> None:
        """command for playAgainButton. it will destroy both playAgainButton and StopPlay button
                and send stop play message to player 2"""
        self.stopPlayButton.destroy()
        self.playAgainButton.destroy()
        self.socket.send(bytes('Fun Times', 'ascii'))
        self.createStatsWindow()


    def resetBoard(self) -> None:
        """Reset both button list which destroys 9 old button and create 9 news
            and board list which used to tell if a winner if exist"""
        self.buttonList = [[' ', ' ', ' '],
                           [' ', ' ', ' '],
                           [' ', ' ', ' ']]

        for row in range(3):
            for col in range(3):
                new_command = partial(self.changeBoardAndCheckWinner, row, col)
                self.buttonList[row][col] = tk.Button(self.window, text='', command=new_command, width=5, height=4)
                self.buttonList[row][col].grid(row=row + 1, column=col)

        if self.move.get() == 'o' or self.move.get() == 'O':
            for i in range(3):
                for j in range(3):
                    self.buttonList[i][j]['state'] = 'disabled'

        self.boardList = [[' ', ' ', ' '],
                          [' ', ' ', ' '],
                          [' ', ' ', ' ']]

        self.winner.config(text='winner:')

        if self.move.get() == 'X':
            self.lastPlayer.config(text=self.userName.get())
        elif self.move.get() == "O":
            self.lastPlayer.config(text=self.otherPlayer.get())


    def createStatsWindow(self) -> None:
        """This will create a window to show stats when the player decides not to play again.
            and the window has a button that can destroy the board window."""
        self.statsWindow = tk.Toplevel(self.window)
        self.statsLabel = tk.Label(self.statsWindow, text=f'Player: {self.userName.get()}\n\n'
                                                          f'Player: {self.otherPlayer.get()}\n\n'
                                                          f'Total number of games: {self.numTotal.get()}\n\n'
                                                          f'Number of wins: {self.numWins.get()}\n\n'
                                                          f'Number of ties: {self.numTies.get()}\n\n'
                                                          f'Number of loss: {self.numLoss.get()}\n\n')
        self.statsLabel.grid(row=1, column=1)

        self.quit = tk.Button(self.statsWindow, text='Quit', command=self.window.destroy)
        self.quit.grid(row=1, column=0)