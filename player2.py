import socket
from gameboard import BoardClass

def infoCheckAndUpdate(window: BoardClass, message: str) -> None:
    """This function checks information from player1 and executes corresponding command.
            If message starts with 'Move', player2 will update board to be the same as player1.
            If message starts with 'Name', player2's window will update 'other name'
            If message starts with 'play', then reset the board
            If message starts with 'Fun', then create a window for stats
            args:
                window: provide the canvas whose buttons might be changed and socket functioning as a receiver
                message: moving or rejecting information send by other player. """
    if message.startswith('Name'):
        window.otherPlayer.set(message[5:])
        window.lastPlayer.config(text=window.otherPlayer.get())
        window.createStatsArea()
    elif message.startswith('Move'):
        row = int(message[5])
        col = int(message[7])

        if window.move.get() == 'o' or window.move.get() == 'O':
            window.boardList[row][col] = 'X'
            window.buttonList[row][col].config(text='X')
            window.buttonList[row][col]['state'] = 'disabled'
        elif window.move.get() == 'x' or window.move.get() == 'X':
            window.boardList[row][col] = 'O'
            window.buttonList[row][col].config(text='O')
            window.buttonList[row][col]['state'] = 'disabled'

        window.lastPlayer.config(text=window.userName.get())
        for i in range(3):
            for j in range(3):
                if window.boardList[i][j] == ' ':
                    window.buttonList[i][j]['state'] = 'active'

        if window.isWinner() == True:
            window.numTotal.set(window.numTotal.get() + 1)
            window.numLoss.set(window.numLoss.get() + 1)
            window.createStatsArea()
            window.winner.config(text='winner: ' + window.otherPlayer.get())
            for i in range(3):
                for j in range(3):
                    window.buttonList[i][j]['state'] = 'disabled'

        elif window.boardIsFull() == True and window.isWinner() == False:
            window.numTotal.set(window.numTotal.get() + 1)
            window.numTies.set(window.numTies.get() + 1)
            window.createStatsArea()
            window.winner.config(text='Tie')
            for i in range(3):
                for j in range(3):
                    window.buttonList[i][j]['state'] = 'disabled'

    elif message.startswith("Play"):
        window.resetBoard()
    elif message.startswith("Fun"):
        window.createStatsWindow()



if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    window2 = BoardClass('player2', 'O', server)
    window2.createBindButton()

    while True:
        window2.runUI()
        try:
            message = window2.socket.recv(1024)
            message = message.decode('ascii')
            isEnd = infoCheckAndUpdate(window2, message)
            window2.socket.send(bytes('No Data', 'ascii'))

        except:
            # print('222222222')
            pass



