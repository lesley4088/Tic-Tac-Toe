import socket
from gameboard import BoardClass

def infoCheckAndUpdate(window: BoardClass, message: str) -> str or None:
    """This function checks information from player2 and executes corresponding command.
        If message starts with 'Move', player1 will update board to be the same as player2.
        If message starts with 'reject', player1's window will re-appear the connect button and asks
        player1 to connect again.

        args:
            window: provide the canvas whose buttons might be changed and socket functioning as a receiver
            message: moving or rejecting information send by other player

        return:
            None means this round is not ending
            True means player1 losses
            False means tie. """
    if message.startswith('Move'):
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
            window1.winner.config(text='winner: ' + window1.otherPlayer.get())
            window.createStatsArea()
            for i in range(3):
                for j in range(3):
                    window.buttonList[i][j]['state'] = 'disabled'
            return 'Loss'
        elif window.boardIsFull() == True and window.isWinner() == False:
            window.numTotal.set(window.numTotal.get() + 1)
            window.numTies.set(window.numTies.get() + 1)
            window.createStatsArea()
            for i in range(3):
                for j in range(3):
                    window.buttonList[i][j]['state'] = 'disabled'
            return 'Tie'

    elif message.startswith('reject'):
        window.createNewConnectButton()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    window1 = BoardClass('', 'X', client)
    window1.otherPlayer.set('Player2')
    window1.createStatsArea()
    window1.createConnectButton()

    while True:
        window1.runUI()
        try:
            window1.socket.send(bytes('No Data', 'ascii'))
            message = window1.socket.recv(1024)
            message = message.decode('ascii')
            isEnd = infoCheckAndUpdate(window1, message)
            if isEnd != None:
                if isEnd == 'Tie':
                    window1.winner.config(text='Tie')
                elif isEnd == 'Loss':
                    window1.winner.config(text='winner: ' + window1.otherPlayer.get())
                window1.createPlayAgainButton()




        except:
            print('11111111')

