# settings
letterPerWord = 6
guessesPerGame = 7
CORRECT = '\033[32m'
MISPLACED = '\033[33m'
INCORRECT = '\033[90m'
DEFAULT = '\033[0m'

board = [['_' for x in range(letterPerWord)] for y in range(guessesPerGame)]# x = #columns, y = #rows
juvieBoard = board.copy()
boardPos = 0

currGuess = ['_' for x in range(letterPerWord)]
guessPos = 0

answer = 'SAMPLE'

def display():
    print('WORDLE', '\nanswer =', answer)
    for x in range(len(board)):
        print(x+1,'{', end = " ")
        for y in range(len(board[x])):
            if juvieBoard[x][y] == 'c':
                print(CORRECT+board[x][y]+DEFAULT, end = " ")
            elif juvieBoard[x][y] == 'm':
                print(MISPLACED+board[x][y]+DEFAULT, end = " ")
            elif juvieBoard[x][y] == 'i':
                print(INCORRECT+board[x][y]+DEFAULT, end = " ")
            else:
                print(DEFAULT+board[x][y]+DEFAULT, end = " ")
                
        if(x == boardPos):
            print('} <-')
        else:
            print('}')
    print('\ng { ', end = "")
    for x in range(len(currGuess)):
        print(currGuess[x], end = " ")
    print('}')
    
def addGuess(str):
    global guessPos
    queue = []
    for x in range(len(str)):
        queue.append(str[x].capitalize())
        if (queue[x] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']) == False:
            queue.remove(queue[x])
    queue = queue[0:letterPerWord-guessPos]
    for x in range(len(queue)):
        currGuess[guessPos] = queue[x]
        guessPos+=1
    
def delGuess():
    global guessPos
    if(guessPos>0):
        guessPos -= 1
        currGuess[guessPos] = '_'

def enterGuess():
    global boardPos, currGuess, guessPos
    if(guessPos == letterPerWord) and (boardPos<guessesPerGame):
        board[boardPos] = currGuess
        boardPos = boardPos+1
        currGuess = ['_' for x in range(letterPerWord)]
        guessPos = 0
    policeGuess()

def policeGuess():
    comparedRow = boardPos-1
    
    correctness = 0
    
    an = []
    for x in range(len(answer)):
        an.append(answer[x])
    
    comp = []
    for y in range(len(board[comparedRow])):
        comp.append(board[comparedRow][y])
    
    #guilty until proven innocent
    juvieBoard[comparedRow] = ['i' for x in range(letterPerWord)]
    
    #do the green tiles
    for y in range(len(comp)):
        if an[y] == comp[y]:
            juvieBoard[comparedRow][y] = 'c'
            an[y] = '0'
            comp[y] = '1'
            correctness += 1
    #do the yellow tiles
    for y in range(len(comp)):
        if comp[y] in an:
            juvieBoard[comparedRow][y] = 'm'
            found = False
            for i in range(len(an)):
                if found == False and comp[y] == an[i]:
                    an[i] = '2'
                    found = True
            comp[y] = '3'
            
    if correctness == letterPerWord:
        win()
        
def win():
    print('yip yip hooray')
display()