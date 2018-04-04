import random, sys, time

SCRABBLE_LETTER_VALUES = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}
playerScore = 0  
computerScore = 0
currentPlayerWords=[]
currentComputerWords=[]

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Creates and returns a list of valid words from file. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def getNewBoard():
    """Creates a brand new, blank board data structure. Returns the board data structure
    """
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board


def testBoard(board):
    board[4][0]= 'd'
    board[4][1]= 'a'
    board[4][2]= 'c' 
    board[4][3]= 'b' 
    board[4][4]= 'o' 
    board[4][5]= 'a' 
    board[4][6]= 't' 
    return board

def startBoard(board):
    """Randomly places 10 letters on the board that it was passed. Returns the board"""
    startletters='abcdefghijklmnopqrstuvwxyz'
    startnumbers = [0,1,2,3,4,5,6,7]    
    for x in range(10):
        startx = random.choice(startnumbers)
        starty = random.choice(startnumbers)
        sletter = random.choice(startletters)
        while not isValidMove(board,startx,starty):
            startx = random.choice(startnumbers)
            starty = random.choice(startnumbers)
        board[startx][starty] = sletter
    return board

def drawBoard(board):
    """This function prints out the board that it was passed. Returns None."""
    HLINE = '  +----+----+----+----+----+----+----+----+'
    VLINE = '  |    |    |    |    |    |    |    |    |'

    print('    1    2    3    4    5    6    7    8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print y+1, 
        for x in range(8):
            print '| %s ' % (board[x][y]), 
        print('|')
        print(VLINE)
        print(HLINE)

def displayLetters():
    """Simple function to print out the letters with their associated values """
    print SCRABBLE_LETTER_VALUES


def whoGoesFirst():
    """Randomly choose the player who goes first. Returns either computer or human player"""
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def getPlayerScores():
    """Return the scores for the players. playerScore and computerScore are global variables """
    return {'player':playerScore, 'computer':computerScore}

## def setPlayerScore(player,wscore):
##     global playerScore
##     global computerScore
##     if player == 'playerScore':
##         playerScore+= wscore
##     if player == 'computerScore':
##         computerScore+=wscore


def calculateScore(word):
    """Function to calculate score for word passed. Returns the total score for the word."""
    totalScore=0
    word = word.upper()
    for letter in word:
        totalScore = totalScore + SCRABBLE_LETTER_VALUES.get(letter, 0)
    return totalScore

def getPlayerWords():
    """Function to print words the players have played so far. currentPlayerWords and
    currentComputerWords are global variables."""
    print 'Player words: ', currentPlayerWords
    print 'Computer words: ', currentComputerWords
    print 


def isOnBoard(x, y):
    """Returns True if the coordinates are located on the board."""
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def isValidMove(board, xstart, ystart):
    """Returns False if the player\'s move on space xstart, ystart is invalid."""
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    else:
        return True

def getPlayerMove(board):
    """Let the player type in their move. The board is passed in to check validity of the move
    Returns the move as list with letter and tuple with x and y move. Will also return 'quit' to
    end game."""
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your letter, or type quit to end the game')
        letter = raw_input().lower()
        if letter == 'quit':
            return 'quit'
        if letter not in 'abcdefghijklmnopqrstuvwxyz':
            continue
        print('Enter position to place letter')
        move = raw_input()
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')
    return [letter,(x, y)]
    

def getComputerMove(board):
    """ Get random valid move for computer player. The board is passed
    in to check the validity of the move. Returns move as list with letter and tuple with
    x and y move."""
    while True:
        letter = random.choice('abcdefghijklmnopqrstuvwxyz')
        xpos = random.choice(range(1,9))
        ypos = random.choice(range(1,9))
        xpos = xpos -1
        ypos = ypos - 1
        if isValidMove(board,xpos,ypos) == False:
            continue
        else:
            break
    return [letter.lower(),(xpos,ypos)]

def reverse_str(s):
    """Function to reverse a string."""
    ns=""
    for c in s:
        ns = c + ns
    return ns

def getWordCreated(board,letterX,letterY,wordList):
    """ Check for if last letter played can spell a word with 4 letters of more in any direction.
    Once first word is found the search breaks and adds word to the list. Returns list of words found.
    Note that this list will not be all words found but first words in any direction."""
    print 'Starting check for word Created'
    wordToCheck=''
    listOfWords=[]
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [-1, 1]]:
    #for xdirection, ydirection in [[0, 1]]:  #, [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = letterX, letterY
        #wordToCheck+=board[x][y]
        while isOnBoard(x,y) and board[x][y] != ' ':
            #print 'Printing x and y :', x+1, y+1
            #print 'WordTocheck before appending while1: ', wordToCheck
            wordToCheck+=board[x][y]         
            #print 'WordTocheck after appending while1: ', wordToCheck
            #time.sleep(3)
            x+=xdirection
            y+=ydirection
            if len(wordToCheck) >= 4:
                for word in wordList:
                    #print 'First Check: ', word
                    #print 'Printing word to check: ',wordToCheck
                    if word == wordToCheck or reverse_str(wordToCheck) == word:
                        listOfWords.append(word)
                        break
        print 'Will now go to not on board'
        #time.sleep(2)
        if not isOnBoard(x,y) or board[x][y] == ' ':
            print 'not on boad: x and y', x+1,y+1
            x, y = letterX, letterY
            wordToCheck=''
            #wordToCheck+=board[x][y]
        
        
        while isOnBoard(x,y) and board[x][y] != ' ':
                #print 'Printing Next x and y :', x+1,y+1
                #print 'wordToChec before apending while2: ', wordToCheck
                wordToCheck+=board[x][y] 
                #print 'wordToCheck after apending while2:', wordToCheck
                #time.sleep(3)
                x-=xdirection
                y-=ydirection
                if len(wordToCheck) >= 4:
                    for word in wordList:
                        #print 'Second check : ', word
                        #print 'Printing word to check: ', wordToCheck
                        if word == wordToCheck or reverse_str(wordToCheck) == word:
                            listOfWords.append(word)
                            break
        if not isOnBoard(x,y) or board[x][y] == ' ':
            x, y = letterX, letterY
            wordToCheck=''
    print 'Printing words Found: ',listOfWords
    return listOfWords
    
def showPoints():
    """Print out the current score."""
    print 
    print
    scores = getPlayerScores()
    print('You have %s points. The computer has %s points.' % (scores['player'], scores['computer']))


def makeMove(board, letter, xstart, ystart):
    """ Use the board letter and x and y positions passed in to make a move on the board."""
    board[xstart][ystart] = letter
    return True


def canPlay(board):
    """Check if a player can make a move on the board 
    this function will be called to find if the game is finished
     Arguments:
    - `boad`: board to check
    """
    count = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == ' ':
                count =  count + 1
            
    if count ==  0:
        print 'Game has ended'
        if computerScore > playerScore:
            print 'Computer won with score: ', computerScore
        elif computerScore < playerScore:
            print 'Human Player won with scrore: ', playerScore
        else:
            print 'There is a tie '
            print 'computer score: ', computerScore
            print 'Player score: ', playerScore
        sys.exit()




def play_game():
    global playerScore
    global computerScore
    print "Welcome to LetterPY"
    word_list = load_words()
    while True:
        mainBoard = getNewBoard()
        #mainBoard = testBoard(mainBoard)
        mainBoard = startBoard(mainBoard)
        turn = whoGoesFirst()
        print  
        print turn + ' will go First'
        print    
        while True:
            if turn == 'player':
                drawBoard(mainBoard)
                displayLetters()
                showPoints()
                getPlayerWords()
                move = getPlayerMove(mainBoard)
                if move == 'quit':
                    print "Thanks for playing PyScrab"
                    sys.exit()
                else:
                    makeMove(mainBoard,move[0],move[1][0],move[1][1])
                    wcreated = getWordCreated(mainBoard,move[1][0],move[1][1],word_list)
                    if wcreated:
                        pscore = calculateScore(wcreated[0])
                        playerScore+=pscore
                        currentPlayerWords.append(wcreated[0])
                    turn = 'computer'
            else:
                #computer's turn to play
                drawBoard(mainBoard)
                displayLetters()
                showPoints()
                getPlayerWords()
                print 'computer\'s turn to play'
                compMove = getComputerMove(mainBoard) 
                makeMove(mainBoard,compMove[0],compMove[1][0],compMove[1][1]) 
                compWordCreated = getWordCreated(mainBoard,compMove[1][0],compMove[1][1],word_list)
                print
                print 'The Computer played letter %s at position %d%d' % (compMove[0], compMove[1][0]+1,compMove[1][1]+1)
                print 
                if compWordCreated:
                    compScore = calculateScore(compWordCreated[0])
                    computerScore+=compScore
                    currentComputerWords.append(compWordCreated[0])
                turn = 'player'

            canPlay(mainBoard)
    
