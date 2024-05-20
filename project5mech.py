import random

class MustInputSpace(Exception):
    '''An exception raised when exclusively a space input is required, and something else is inputted'''
    pass

class InvalidRows(Exception):
    '''An exception raised when a number of rows less than 4 is inputted'''
    pass
    
class InvalidCols(Exception):
    '''An exception raised when a number of columns less than 3 is inputted'''
    pass

class InvalidColumnFallerSelection(Exception):
    '''An exception raised when a column number is invalid for a created faller'''
    pass

class Columns:
    def __init__(self, rows:int, cols:int):
        '''Creates a Columns board of a specified height and width'''
        self._rows:int = rows
        self._cols:int = cols
        self._board:list = []
        self._faller:list = []
        self._fallerpos:list = []
        self._comboboard:list = []
        for i in range(rows):
            self._board.append([])
            for j in range(cols):
                self._board[-1].append('EMPTY')
        self._pairs:int = 0
                
    def getboard(self) -> list[list]:
        '''Returns copy of self._board'''
        board = [x[:] for x in self._board]
        return board
    
    def content(self, lspecs:list[str]):
        '''Sets up the initial layout for self._board using information from lspecs'''
        for i in range(self._rows-1, -1, -1):
            for j in range(self._cols-1, -1, -1):
                if lspecs[i][j] == ' ':
                    pass
                elif lspecs[i][j] != ' ':
                    tempi = i
                    while tempi + 1 < self._rows:
                            if self._board[tempi+1][j] == 'EMPTY':
                                tempi += 1
                            else:
                                break
                    self._board[tempi][j] = (' ' + lspecs[i][j] + ' ')
                    
                    
    def combo(self):
        '''Identifies horizontal, vertical, and diagonal combos, and updates the board with * signs'''
        backrooms = []
        for i in range(2):
            backrooms.append([])
            for j in range(self._cols):
                backrooms[-1].append('EMPTY')
        if self._fallerpos != []:
            if self._fallerpos[2] == ['None']:
                return
            elif self._fallerpos[1] == ['None']:
                col = self._fallerpos[2][1]
                backrooms[0][col] = ' ' + self._faller[0] + ' '
                backrooms[1][col] = ' ' + self._faller[1] + ' '
            elif self._fallerpos[0] == ['None']:
                col = self._fallerpos[2][1]
                backrooms[1][col] = ' ' + self._faller[0] + ' '
                
        comboboard = backrooms.copy()
        comboboard.extend(self._board.copy())
        
        horizmatches:list[list] = []
        for ri in range(len(comboboard)):
            l2 = []
            l3 = []
            for ci in range((len(comboboard[0]))):
                l2.append(comboboard[ri][ci])
                l3.append((ri, ci))
                if ci < (len(comboboard[0])-1):
                    nextjewel = comboboard[ri][ci+1]
                if ci == (len(comboboard[0])-1) or nextjewel not in l2 or nextjewel == ' ':
                    if len(l2) >= 3 and l2[0] != 'EMPTY' and l2[0][0] != '[' and l2[0][0] != '|':
                        horizmatches.append(l3)
                    l2 = []
                    l3 = []
        verticmatches:list[list] = []
        for ci in range(len(comboboard[0])):
            l2 = []
            l3 = []
            for ri in range(len(comboboard)):
                l2.append(comboboard[ri][ci])
                l3.append((ri, ci))
                if ri < (len(comboboard)-1):
                    nextjewel = comboboard[ri+1][ci]
                if ri == (len(comboboard)-1) or nextjewel not in l2 or nextjewel == ' ':
                    if len(l2) >= 3 and l2[0] != 'EMPTY' and l2[0][0] != '[' and l2[0][0] != '|':
                        verticmatches.append(l3)
                    l2 = []
                    l3 = []
        diagmatches:list[list] = []
        for ri in range(len(comboboard)):
            for ci in range(len(comboboard[0])):
                rightdiag = []
                increment = 0
                while True:
                    if comboboard[ri][ci] != 'EMPTY' and comboboard[ri][ci][0] != '[' and comboboard[ri][ci][0] != '|':
                        #right diag
                        if ri+increment < len(comboboard) and ci+increment < len(comboboard[0]):
                            if comboboard[ri][ci] == comboboard[ri+increment][ci+increment]:
                                rightdiag.append((ri+increment, ci+increment))
                                # if comboboard[ri][ci] != 'EMPTY' and rightdiag[0][0] != '[' and rightdiag[0][0] != '|':
                                increment += 1
                            else:
                                break
                        else:
                            break
                    else:
                        break
                if len(rightdiag) >= 3 and rightdiag[0] != 'EMPTY' and rightdiag[0][0] != '[' and rightdiag[0][0] != '|':
                    diagmatches.append(rightdiag)
        for ri in range(len(comboboard)):
            for ci in range(len(comboboard[0])):
                leftdiag = []
                increment = 0
                while True:
                    if comboboard[ri][ci] != 'EMPTY' and comboboard[ri][ci][0] != '[' and comboboard[ri][ci][0] != '|':
                        if ri+increment < len(comboboard) and ci-increment > -1:
                            if comboboard[ri][ci] == comboboard[ri+increment][ci-increment]:
                                leftdiag.append((ri+increment, ci-increment))
                                increment += 1
                            else:
                                break
                        else:
                            break
                    else:
                        break
                if len(leftdiag) >= 3 and leftdiag[0] != 'EMPTY' and leftdiag[0][0] != '[' and leftdiag[0][0] != ']':
                    diagmatches.append(leftdiag)
        matches = horizmatches.copy() + verticmatches.copy() + diagmatches.copy()
        for match in matches:
            for coord in match:
                ri = coord[0]
                ci = coord[1]
                jewel = comboboard[ri][ci][1]
                comboboard[ri][ci] = '*' + jewel + '*'
        
        self._board = comboboard[2:].copy()
        self._comboboard = comboboard
        
                    
    def createfaller(self, move:str) -> bool:
        '''Generates a 3-jewel faller specified by str move and returns a boolean for if the program can't continue'''
        movepar = move.split()
        self._faller = [movepar[2], movepar[3], movepar[4]]
        self._fallerpos = [['None'], ['None'], [0, int(movepar[1])-1]]
        if self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] != 'EMPTY':
            return True
        if self._board[self._fallerpos[2][0]+1][self._fallerpos[2][1]] != 'EMPTY':
            self._board[0][int(movepar[1])-1] = '|' + str(movepar[4]) + '|'
        else:
            self._board[0][int(movepar[1])-1] = '[' + str(movepar[4]) + ']'
        return False
    
    def rotate(self):
        '''Rotates the elements of the faller'''
        leftb = '['
        rightb = ']'
        if '|' in self._board[self._fallerpos[2][0]][self._fallerpos[2][1]]:
            leftb = '|'
            rightb = '|'
        self._faller = [self._faller[2], self._faller[0], self._faller[1]]
        if self._fallerpos[1] == ['None']:
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + self._faller[2] + rightb
        elif self._fallerpos[0] == ['None']:
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + self._faller[1] + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + self._faller[2] + rightb
        else:
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = leftb + self._faller[0] + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + self._faller[1] + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + self._faller[2] + rightb
        # self._fallerpos = [self._fallerpos[2], self._fallerpos[0], self._fallerpos[1]]
        #BACKUP ^
        
    def fall(self) -> bool:
        '''Makes it so a faller gradually falls, lands, and freezes on a board. Removes current combinations,
        and returns a boolean for whether the game can't continue'''
        justwait = True
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if "*" in self._board[i][j] or '[' in self._board[i][j] or '|' in self._board[i][j]:
                    justwait = False
        if justwait:
            return False
        hascombo = False
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if '*' in self._board[i][j]:
                    hascombo = True
                    break
        if hascombo:
            for i in range(len(self._comboboard)):
                for j in range(len(self._comboboard[0])):
                    if '*' in self._comboboard[i][j]:
                        self._comboboard[i][j] == 'EMPTY'
                        tempi = i
                        while tempi-1 > -1:
                            self._comboboard[tempi][j] = self._comboboard[tempi-1][j]
                            tempi -= 1
                        self._comboboard[tempi][j] = 'EMPTY'
            for i in range(2):
                for j in range(len(self._comboboard[0])):
                    if self._comboboard[i][j] != 'EMPTY':
                        return True
            self._board = self._comboboard[2:].copy()
            return False
        frozen = False
        if '|' in self._board[self._fallerpos[2][0]][self._fallerpos[2][1]]:
            if self._fallerpos[1] == ['None']:
                self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = ' ' + self._faller[2] + ' '
            elif self._fallerpos[0] == ['None']:
                self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = ' ' + self._faller[1] + ' '
                self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = ' ' + self._faller[2] + ' '
            else:
                self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = ' ' + self._faller[0] + ' '
                self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = ' ' + self._faller[1] + ' '
                self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = ' ' + self._faller[2] + ' '
            frozen = True
            
        leftb = '['
        rightb = ']'
        jewelbelow = False
        if self._fallerpos[2][0]+2 < len(self._board):
            if self._board[self._fallerpos[2][0]+2][self._fallerpos[2][1]] != 'EMPTY':
                jewelbelow = True
                
        if self._fallerpos[2][0] == (len(self._board)-2) or jewelbelow: 
            leftb = '|'
            rightb = '|'
        if frozen:
            return False
        if self._fallerpos[1] == ['None']:
            self._fallerpos = [self._fallerpos[0], [0, self._fallerpos[2][1]], [1, self._fallerpos[2][1]]]
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
        elif self._fallerpos[0] == ['None']:
            self._fallerpos = [[0, self._fallerpos[2][1]], [1, self._fallerpos[2][1]], [2, self._fallerpos[2][1]]]
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = leftb + str(self._faller[0]) + rightb
        else:
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = 'EMPTY'
            self._fallerpos = [[self._fallerpos[0][0]+1, self._fallerpos[0][1]], [self._fallerpos[1][0]+1, self._fallerpos[1][1]], [self._fallerpos[2][0]+1, self._fallerpos[2][1]]]
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = leftb + str(self._faller[0]) + rightb
        return False
        
            
    def right(self):
        '''Shifts the faller to the right on the board if there is available room'''
        leftb = '['
        rightb = ']'
        landed = False
        if self._fallerpos[2][0]+1 < self._rows and self._fallerpos[2][1]+1 < self._cols:
            if self._board[self._fallerpos[2][0]+1][self._fallerpos[2][1]+1] != 'EMPTY':
                landed = True
        else:
            landed = True
        
        if landed == True:
            leftb = '|'
            rightb = '|'
        
        if self._fallerpos[2][1] == len(self._board[0])-1:
            return
        
        if self._fallerpos[1] == ['None']:
            if self._board[self._fallerpos[2][0]][self._fallerpos[2][1]+1] != 'EMPTY':
                return
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [self._fallerpos[0], self._fallerpos[1], [self._fallerpos[2][0], self._fallerpos[2][1]+1]]
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
        elif self._fallerpos[0] == ['None']:
            if self._board[self._fallerpos[1][0]][self._fallerpos[1][1]+1] != 'EMPTY' or self._board[self._fallerpos[2][0]][self._fallerpos[2][1]+1] != 'EMPTY':
                return
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = 'EMPTY'
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [self._fallerpos[0], [self._fallerpos[1][0], self._fallerpos[1][1]+1], [self._fallerpos[2][0], self._fallerpos[2][1]+1]]
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
        else:
            if self._board[self._fallerpos[0][0]][self._fallerpos[0][1]+1] != 'EMPTY' or self._board[self._fallerpos[1][0]][self._fallerpos[1][1]+1] != 'EMPTY' or self._board[self._fallerpos[2][0]][self._fallerpos[2][1]+1] != 'EMPTY':
                return
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = 'EMPTY'
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = 'EMPTY'
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [[self._fallerpos[0][0], self._fallerpos[0][1]+1], [self._fallerpos[1][0], self._fallerpos[1][1]+1], [self._fallerpos[2][0], self._fallerpos[2][1]+1]]
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = leftb + str(self._faller[0]) + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb+ str(self._faller[1]) + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
        
            
    def left(self):
        '''Shifts the faller to the left on the board if there is available room'''
        leftb = '['
        rightb = ']'
        landed = False
        if self._fallerpos[2][0]+1 < self._rows and self._fallerpos[2][1]-1 > -1:
            if self._board[self._fallerpos[2][0]+1][self._fallerpos[2][1]-1] != 'EMPTY':
                landed = True
        else:
            landed = True
        
        if landed == True:
            leftb = '|'
            rightb = '|'
            
        if self._fallerpos[2][1] == 0:
            return
        
        if self._fallerpos[1] == ['None']:
            if self._board[self._fallerpos[2][0]][self._fallerpos[2][1]-1] != 'EMPTY':
                return
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [self._fallerpos[0], self._fallerpos[1], [self._fallerpos[2][0], self._fallerpos[2][1]-1]]
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
        elif self._fallerpos[0] == ['None']:
            if self._board[self._fallerpos[1][0]][self._fallerpos[1][1]-1] != 'EMPTY' or self._board[self._fallerpos[2][0]][self._fallerpos[2][1]-1] != 'EMPTY':
                return
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = 'EMPTY'
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [self._fallerpos[0], [self._fallerpos[1][0], self._fallerpos[1][1]-1], [self._fallerpos[2][0], self._fallerpos[2][1]-1]]
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
        else:
            if self._board[self._fallerpos[0][0]][self._fallerpos[0][1]-1] != 'EMPTY' or self._board[self._fallerpos[1][0]][self._fallerpos[1][1]-1] != 'EMPTY' or self._board[self._fallerpos[2][0]][self._fallerpos[2][1]-1] != 'EMPTY':
                return
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = 'EMPTY'
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = 'EMPTY'
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = 'EMPTY'
            self._fallerpos = [[self._fallerpos[0][0], self._fallerpos[0][1]-1], [self._fallerpos[1][0], self._fallerpos[1][1]-1], [self._fallerpos[2][0], self._fallerpos[2][1]-1]]
            self._board[self._fallerpos[0][0]][self._fallerpos[0][1]] = leftb + str(self._faller[0]) + rightb
            self._board[self._fallerpos[1][0]][self._fallerpos[1][1]] = leftb + str(self._faller[1]) + rightb
            self._board[self._fallerpos[2][0]][self._fallerpos[2][1]] = leftb + str(self._faller[2]) + rightb
            
    def p5makerandomfaller(self, currboard:list[list]) -> str:
        '''Makes and returns a random faller string that can be used to create a faller'''
        validcols = []
        for i in range(len(currboard[0])):
            if currboard[0][i] == 'EMPTY':
                validcols.append(i+1)
        if len(validcols) == 0:
            raise Exception
        jewelstr = 'STVWXYZ' #STVWXYZ
        chosencol = validcols[random.randint(0, len(validcols)-1)]
        command = 'F ' + str(chosencol)
        for i in range(3):
            randjewel = jewelstr[random.randint(0, 6)]
            command += ' ' + randjewel
        return command
            
    def p5makeboard(self) -> str:
        '''Creates a game of Columns with specifically 13 rows and 6 columns'''
        rows:int = 13
        cols:int = 6
        self._game = Columns(rows, cols)
        self._fmove = ''
        self._pairs = 0
        self._fallerpresent = False
        return self._game.getboard()
        
    def p5buildfaller(self) -> list[list]:
        '''Constructs a faller while handling whether a faller is already present and returns the current board'''
        if self._fallerpresent == False:
            genfaller = self.p5makerandomfaller(self._game.getboard())
            self._pairs = 0
            self._fmove = genfaller
            self._fallerpresent = True
            shouldquit = self._game.createfaller(genfaller)
            if shouldquit:
                return
        return self._game.getboard()
        
    def p5wait(self) -> list[list]:
        '''Waits for the board to fall once and returns the current board'''
        boardscreated:list = []
        while True:
            shouldquit = self._game.fall()
            if shouldquit:
                return
            version1 = self._game.getboard()
            for i in range(len(version1)):
                for j in range(len(version1[0])):
                    if '|' in version1[i][j]:
                        self._pairs += 1
            self._game.combo()
            versioncombo = self._game.getboard()
            if version1 == versioncombo:
                if self._fmove != '': #no matches after freezing
                    cont = True
                    for i in range(len(version1)):
                        for j in range(len(version1[0])):
                            if '|' in version1[i][j] or '[' in version1[i][j]: #must have frozen
                                # fallerpresent = False
                                cont = False
                    if cont:
                        self._fallerpresent = False
                        if self._pairs < 3: #not every element fit on the board
                            return #not every element fit but also didn't combo afterwards
                break
            else:

                self._fmove = ''
                self._fallerpresent = False
                boardscreated.append(self._game.getboard())

        boardscreated.append(self._game.getboard())
        return boardscreated

    def p5movesright(self) -> list[list]:
        '''Moves the faller right and returns the current board'''
        self._game.right()
        self._pairs = 0
        for i in range(13):
                for j in range(6):
                    if '|' in self._game.getboard()[i][j]:
                        self._pairs += 1
        return self._game.getboard()
        
    def p5movesleft(self) -> list[list]:
        '''Moves the faller left and returns the current board'''
        self._game.left()
        self._pairs = 0
        for i in range(13):
                for j in range(6):
                    if '|' in self._game.getboard()[i][j]:
                        self._pairs += 1
        return self._game.getboard()
        
    def p5rotates(self) -> list[list]: 
        '''Rotates the faller and returns the current board'''
        self._game.rotate()
        self._pairs = 0
        for i in range(13):
                for j in range(6):
                    if '|' in self._game.getboard()[i][j]:
                        self._pairs += 1
        return self._game.getboard()


