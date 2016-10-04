#!/usr/bin/python2
#inputfile
#name: Ren Chen
#date: June/8/2016

import getopt
import sys
import copy
    
def getArgs():
    args = sys.argv[1:]
    fileName = args[0]
    ##opts, args = getopt.getopt(sys.argv[1:], [])
    ##for fileName in opts:
    #print 'File name: %s' % fileName
    ##
    with open(fileName, 'r') as inputFile:
        result = inputFile.read().splitlines()
        inputFile.close()
    return result
    
def cutOffTest(board, depth):
    cutOff = False
    if terminalTest(board):
        cutOff = True
    if depth >= cutOffDepth:
        cutOff = True
    return cutOff
    
def someOneWin(board, player, move):
    if evalNewPieceScore(move, board, player) >= 50000:
        return True
    else:
        return False
    
def terminalTest(board):
    for i in range(0, numBLines):
        for j in range(0, numBLines):
            if board[i][j] == '.':
                return False
    return True

def outOfBoard(x, y):
    if (x < 0 or x >= numBLines or y < 0 or y >= numBLines):
       return True
    return False
    
def getNewBoard(board, newMove, player) :
    newBoard = copy.deepcopy(board)
    newBoard[newMove[0]][newMove[1]] = symbol[player] 
    return newBoard
    
    
#Check consecutive pieces of 'length' starting from (x,y)
def checkRow(x, y, player, length, board) :
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    offsetMax = length
    
    #check in a row
    if (outOfBoard(x, y) or outOfBoard(x + offsetMax, y)):
        return False, False, False, False
    else:
        for i in range(0, offsetMax):
            isConsecutive =  isConsecutive and (board[x+i][y] == symbol[player])
        if(isConsecutive):
            if outOfBoard(x-1, y):
                if board[x+length][y] == '.':
                    isClosed = True        
                if board[x+length][y] == symbol[(player+1)%2]:            
                    isBlocked = True                  
            elif outOfBoard(x+length, y):
                if board[x - 1][y] == '.':
                    isClosed = True
                if board[x - 1][y] == symbol[(player+1)%2]:            
                    isBlocked = True                              
            else:                   
                if(  ( board[x - 1][y] == '.' and  board[x + length][y] == symbol[(player+1)%2])  or
                    ( board[x - 1][y] == symbol[(player+1)%2] and  board[x + length][y] ==  '.')  ):
                    isClosed = True
                if( board[x - 1][y] == '.' and  board[x + length][y] == '.' ):
                    isOpen = True        
                if(  board[x - 1][y] == symbol[(player+1)%2] and board[x + length][y] == symbol[(player+1)%2] ):                       
                    isBlocked = True
                      
    return isConsecutive, isOpen, isClosed, isBlocked
            
##lower starting point          
def checkCol(x, y, player, length, board):
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    offsetMax = length - 1
    
    #check in a column
    if (outOfBoard(x, y) or outOfBoard(x, y+length-1)):
        return False, False, False, False
    else:
        for i in range(0, length):
            isConsecutive =  isConsecutive and (board[x][y+i] == symbol[player])
        if(isConsecutive):
            if outOfBoard(x, y-1):
                if board[x][y+length] == '.':
                    isClosed = True
                if board[x][y+length] == symbol[(player+1)%2]:
                    isBlocked = True
            elif outOfBoard(x, y+length):
                if board[x][y - 1] == '.':
                    isClosed = True
                if board[x][y - 1] == symbol[(player+1)%2]:            
                    isBlocked = True    
            else:                   
                if(  ( board[x][y - 1] == '.' and  board[x][y + length] == symbol[(player+1)%2] )  or
                    ( board[x][y - 1] == symbol[(player+1)%2] and  board[x][y + length] ==  '.' )  ):
                    isClosed = True
                if( board[x][y - 1] == '.' and  board[x][y + length] == '.' ):
                    isOpen = True    
                if(  board[x][y - 1] == symbol[(player+1)%2] and  board[x][y + length] == symbol[(player+1)%2] ):                       
                    isBlocked = True
                       
    return isConsecutive, isOpen, isClosed, isBlocked
    
#check in a left diagonal        
def checkLeftDiag(x, y, player, length, board)    :
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    offsetMax = length - 1
    
    if (outOfBoard(x, y) or outOfBoard(x+length-1, y+length-1)):
        return False, False, False, False
    else:
        for i in range(0, length):
            isConsecutive =  isConsecutive and (board[x+i][y+i] == symbol[player])
        if(isConsecutive):
            if outOfBoard(x-1, y-1):
                if board[x+length][y+length] == '.':
                    isClosed = True        
                if board[x+length][y+length] == symbol[(player+1)%2]:            
                    isBlocked = True                           
            elif outOfBoard(x+length, y+length):
                if board[x-1][y - 1] == '.':
                    isClosed = True
                if board[x-1][y - 1] == symbol[(player+1)%2]:            
                    isBlocked = True    
            else:                   
                if(  ( board[x - 1][y - 1] == '.' and  board[x + length][y + length] == symbol[(player+1)%2] ) or
                    ( board[x - 1][y - 1] == symbol[(player+1)%2] and  board[x + length][y + length] ==  '.' )  ):
                      isClosed = True
                if( board[x - 1][y - 1] == '.' and  board[x + length][y + length] == '.' ):
                    isOpen = True    
                if(  board[x - 1][y - 1] == symbol[(player+1)%2] and  board[x + length][y + length] == symbol[(player+1)%2] ):                       
                    isBlocked = True
                   
    return isConsecutive, isOpen, isClosed, isBlocked

    
#check in a right diagonal        
def checkRightDiag(x, y, player, length, board)    :
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    offsetMax = length - 1
    
    if (outOfBoard(x, y) or outOfBoard(x+length-1, y-length+1)):
        return False, False, False, False
    else:
        for i in range(0, length):
            isConsecutive =  isConsecutive and (board[x+i][y-i] == symbol[player])
        #print 'check isConsecutive'
        #print isConsecutive
        
        if(isConsecutive):
            if outOfBoard(x-1, y+1):
                if board[x + length][y - length] == '.':
                    isClosed = True        
                if board[x + length][y - length] == symbol[(player+1)%2]:            
                    isBlocked = True                           
            elif outOfBoard(x + length, y - length):
                if board[x - 1][y + 1] == '.':
                    isClosed = True
                if board[x - 1][y + 1] == symbol[(player+1)%2]:
                    isBlocked = True    
            else:                   
                if(  ( board[x - 1][y + 1] == '.' and  board[x + length][y - length] == symbol[(player+1)%2]  )  or
                     ( board[x - 1][y + 1] == symbol[(player+1)%2] and  board[x + length][y - length] ==  '.' )  ):
                    isClosed = True
                if( board[x - 1][y + 1] == '.' and  board[x + length][y - length] == '.' ):
                    isOpen = True    
                if(  board[x - 1][y + 1] == symbol[(player+1)%2] and  board[x + length][y - length] == symbol[(player+1)%2] ):                       
                    isBlocked = True
                   
    return isConsecutive, isOpen, isClosed, isBlocked           


######left starting point    
def evalScoreInRow(newpiece, board, player) :
    x, y = newpiece[0], newpiece[1]    
    
    createScore, blockScore, totalScore = 0, 0, 0    
    #check create score
    lengthArray = range(5, 1, -1)                        #length of consecutive pieces
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    
    ##for idx in range(3,-1,-1):                              #index of scoreOpen, scoreClosed   
    ##for offset in range (lengthArray[idx]-1, -1, -1):                         #offset = x - xStart or y - yStart
    #Check consecutive pieces in a direction
    
    #check left side
    li = 0
    bli = 0
    ri = 0
    bri = 0    
    
    #count left
    while(isConsecutive)   :
        li = li + 1    
        if(x-li < 0):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x-li][y] == symbol[player])
      
    #check left block      
    if(li < 2):
        #check left block        
        isConsecutive = True     
        outBoard = False        
        while(isConsecutive)  : 
            bli = bli + 1    
            if(x-bli < 0):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x-bli][y] == symbol[(player+1)%2])
        
        if(bli >= 4):
            if bli == 4:    
                if outBoard:
                    blockScore += scoreBlock[2]   #blockClosedThree                     
                elif board[x-bli][y] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bli == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x-bli][y]  != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
                            
     
    #count right
    isConsecutive = True
    while(isConsecutive)   :
        ri = ri + 1    
        if(x + ri >= numBLines):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x + ri][y] == symbol[player])
    
    #check right block
    if (ri < 2):
        #check if block
        isConsecutive = True
        outBoard = False
        while(isConsecutive)  : 
            bri = bri + 1    
            if(x + bri >= numBLines):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x + bri][y] == symbol[(player+1)%2])
        
        if(bri >= 4):
            if bri == 4:        
                if outBoard:
                    blockScore += scoreBlock[2]   #blockClosedThree  
                elif board[x + bri][y] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bri == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x + bri][y]  != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
                            
    #get create score 
    if(ri < 2):
        if(li < 5 and li >= 2):
            if x-li < 0:
                if board[x+1][y] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x+1 >= numBLines:
                if board[x-li][y] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x - li][y] == '.' and  board[x + 1][y] == symbol[(player+1)%2])  or
                    ( board[x - li][y] == symbol[(player+1)%2] and  board[x + 1][y] ==  '.')  ):
                    createScore += scoreClosed[li]  
                if( board[x - li][y] == '.' and  board[x + 1][y] == '.' ):
                    createScore += scoreOpen[li]  
        elif (li == 5):
            createScore += scoreOpen[li]
            
    elif(li < 2):
        if(ri < 5 and ri >= 2):
            if x+ri >= numBLines:
                if board[x-1][y] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x-1 < 0:
                if board[x+ri][y] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x + ri][y] == '.' and  board[x - 1][y] == symbol[(player+1)%2])  or
                    ( board[x + ri][y] == symbol[(player+1)%2] and  board[x - 1][y] ==  '.')  ):
                    createScore += scoreClosed[ri]  
                if( board[x + ri][y] == '.' and  board[x - 1][y] == '.' ):
                    createScore += scoreOpen[ri]  
        elif (ri == 5):
            createScore += scoreOpen[ri]
            
    elif(ri >= 2 and li >= 2):
        numConsec = ri + li - 1
        if x+ri >= numBLines:
            if board[x-li][y] == '.':
                createScore += scoreClosed[numConsec]     ##                
        elif x-li < 0:
            if board[x+ri][y] == '.':
                createScore += scoreClosed[numConsec]                               
        else:                   
            if(  ( board[x + ri][y] == '.' and  board[x - li][y] == symbol[(player+1)%2])  or
                ( board[x + ri][y] == symbol[(player+1)%2] and  board[x - li][y] ==  '.')  ):
                createScore += scoreClosed[numConsec]  
            if( board[x + ri][y] == '.' and  board[x - li][y] == '.' ):
                createScore += scoreOpen[numConsec]  
    
             
    totalScore = createScore + blockScore
    
    return totalScore
            
            
def evalScoreInCol(newpiece, board, player):
    x, y = newpiece[0], newpiece[1]               
    createScore, blockScore, totalScore = 0, 0, 0
    
    #check create score
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    
    ##for idx in range(3,-1,-1):                              #index of scoreOpen, scoreClosed   
    ##for offset in range (lengthArray[idx]-1, -1, -1):                         #offset = x - xStart or y - yStart
    #Check consecutive pieces in a direction
    
    #check left side
    li = 0
    bli = 0
    ri = 0
    bri = 0    
    
    #count lower
    while(isConsecutive)   :
        li = li + 1    
        if(y-li < 0):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x][y-li] == symbol[player])
      
    #check left block      
    if(li < 2):
        #check left block        
        isConsecutive = True     
        outBoard = False        
        while(isConsecutive)  : 
            bli = bli + 1    
            if(y-bli < 0):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x][y-bli] == symbol[(player+1)%2])
        
        if(bli >= 4):
            if bli == 4:        
                if outBoard:
                    blockScore += scoreBlock[2]   #blockClosedThree 
                elif board[x][y-bli] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bli == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x][y-bli] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour                    
     
    #count upper
    isConsecutive = True
    while(isConsecutive)   :
        ri = ri + 1    
        if(y + ri >= numBLines):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x][y + ri] == symbol[player])
    
    #check right block
    if (ri < 2):
        #check if block
        isConsecutive = True
        outBoard = False
        
        while(isConsecutive)  : 
            bri = bri + 1    
            if(y + bri >= numBLines):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x][y + bri] == symbol[(player+1)%2])
        
        if(bri >= 4):
            if bri == 4: 
                if outBoard:
                    blockScore += scoreBlock[2]   #blockClosedThree                     
                if board[x ][y + bri] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bri == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x ][y + bri] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
                            
    #get create score 
    if(ri < 2):
        if(li < 5 and li >= 2):
            if y-li < 0:
                if board[x][y+1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif y+1 >= numBLines:
                if board[x][y-li] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x ][y- li] == '.' and  board[x ][y + 1] == symbol[(player+1)%2])  or
                    ( board[x ][y- li] == symbol[(player+1)%2] and  board[x][y + 1] ==  '.')  ):
                    createScore += scoreClosed[li]  
                if( board[x][y - li] == '.' and  board[x][y + 1] == '.' ):
                    createScore += scoreOpen[li]  
        elif (li == 5):
            createScore += scoreOpen[li]
    elif(li < 2):
        if(ri < 5 and ri >= 2):
            if y+ri >= numBLines:
                if board[x][y-1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif y-1 < 0:
                if board[x][y+ri] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x][y + ri] == '.' and  board[x][y - 1] == symbol[(player+1)%2])  or
                    ( board[x][y + ri] == symbol[(player+1)%2] and  board[x][y - 1] ==  '.')  ):
                    createScore += scoreClosed[ri]  
                if( board[x][y + ri] == '.' and  board[x][y - 1] == '.' ):
                    createScore += scoreOpen[ri]  
        elif (ri == 5):
            createScore += scoreOpen[ri]
            
    elif(ri >= 2 and li >= 2):
        numConsec = ri + li - 1
        if y+ri >= numBLines:
            if board[x][y-li] == '.':
                createScore += scoreClosed[numConsec]     ##                
        elif y-li < 0:
            if board[x][y+ri] == '.':
                createScore += scoreClosed[numConsec]                               
        else:                   
            if(  ( board[x][y + ri] == '.' and  board[x][y - li] == symbol[(player+1)%2])  or
                ( board[x][y + ri] == symbol[(player+1)%2] and  board[x][y - li] ==  '.')  ):
                createScore += scoreClosed[numConsec]  
            if( board[x][y + ri] == '.' and  board[x][y - li] == '.' ):
                createScore += scoreOpen[numConsec]  
    
             
    totalScore = createScore + blockScore
    
    return totalScore
    
    
def evalScoreInLeftDiag(newpiece, board, player):
    x, y = newpiece[0], newpiece[1]    
    
    createScore, blockScore, totalScore = 0, 0, 0    
    #check create score
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    
    ##for idx in range(3,-1,-1):                              #index of scoreOpen, scoreClosed   
    ##for offset in range (lengthArray[idx]-1, -1, -1):                         #offset = x - xStart or y - yStart
    #Check consecutive pieces in a direction
    
    #check left side
    li = 0
    bli = 0
    ri = 0
    bri = 0    
    
    #count lower left
    while(isConsecutive)   :
        li = li + 1    
        if(x-li < 0 or y-li <0):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x-li][y-li] == symbol[player])
      
    #check lower left block      
    if(li < 2):
        #check left block        
        isConsecutive = True        
        outBoard = False
        
        while(isConsecutive)  : 
            bli = bli + 1    
            if(x-bli < 0 or y-bli<0):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x-bli][y-bli] == symbol[(player+1)%2])
        
        if(bli >= 4):
            if bli == 4:     
                if outBoard: 
                    blockScore += scoreBlock[2]   #blockClosedThree     
                elif  board[x-bli][y-bli] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bli == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x-bli][y-bli] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
     
    #count upper right
    isConsecutive = True
    while(isConsecutive)   :
        ri = ri + 1    
        if(x + ri >= numBLines or y+ri >= numBLines):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x + ri][y + ri] == symbol[player])
    
    #check upper right block
    if (ri < 2):
        #check if block
        isConsecutive = True
        outBoard = False
        
        while(isConsecutive)  : 
            bri = bri + 1    
            if(x + bri >= numBLines or y+bri >= numBLines):
                outBoard = True
                isConsecutive = False
                break
            isConsecutive =  isConsecutive and (board[x + bri][y + bri] == symbol[(player+1)%2])
        
        if(bri >= 4):
            if bri == 4:   
                if outBoard: 
                    blockScore += scoreBlock[2]   #blockClosedThree  
                elif board[x + bri][y + bri] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree  
            elif bri == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x + bri][y + bri] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
                            
    #get create score 
    if(ri < 2):
        #lower left
        if(li < 5 and li >= 2):
            if x-li < 0 or y - li < 0:
                if board[x+1][y+1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x+1 >= numBLines or y+1 >= numBLines:
                if board[x-li][y-li] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x - li][y - li] == '.' and  board[x + 1][y + 1] == symbol[(player+1)%2])  or
                    ( board[x - li][y - li] == symbol[(player+1)%2] and  board[x + 1][y + 1] ==  '.')  ):
                    createScore += scoreClosed[li]  
                if( board[x - li][y - li] == '.' and  board[x + 1][y + 1] == '.' ):
                    createScore += scoreOpen[li]  
        elif (li == 5):
            createScore += scoreOpen[li]
    elif(li < 2):
        #upper right
        if(ri < 5 and ri >= 2):
            if x+ri >= numBLines or y+ri >= numBLines:
                if board[x-1][y-1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x-1 < 0 or y - 1 < 0:
                if board[x+ri][y+ri] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x + ri][y+ri] == '.' and  board[x - 1][y-1] == symbol[(player+1)%2])  or
                    ( board[x + ri][y+ri] == symbol[(player+1)%2] and  board[x - 1][y - 1] ==  '.')  ):
                    createScore += scoreClosed[ri]  
                if( board[x + ri][y + ri] == '.' and  board[x - 1][y-1] == '.' ):
                    createScore += scoreOpen[ri]  
        elif (ri == 5):
            createScore += scoreOpen[ri]
            
    elif(ri >= 2 and li >= 2):
        numConsec = ri + li - 1
        if x+ri >= numBLines or y+ri >= numBLines:
            if board[x-li][y-li] == '.':
                createScore += scoreClosed[numConsec]     ##                
        elif x-li < 0 or y-li < 0:
            if board[x+ri][y+ri] == '.':
                createScore += scoreClosed[numConsec]                               
        else:                   
            if(  ( board[x + ri][y + ri] == '.' and  board[x - li][y-  li] == symbol[(player+1)%2])  or
                ( board[x + ri][y + ri] == symbol[(player+1)%2] and  board[x - li][y - li] ==  '.')  ):
                createScore += scoreClosed[numConsec]  
            if( board[x + ri][y + ri] == '.' and  board[x - li][y - li] == '.' ):
                createScore += scoreOpen[numConsec]  
    
             
    totalScore = createScore + blockScore
    
    return totalScore
    
    
    
def evalScoreInRightDiag(newpiece, board, player):
    x, y = newpiece[0], newpiece[1]    
    
    createScore, blockScore, totalScore = 0, 0, 0    
    #check create score
    isConsecutive, isOpen, isClosed, isBlocked = True, False, False, False
    
    ##for idx in range(3,-1,-1):                              #index of scoreOpen, scoreClosed   
    ##for offset in range (lengthArray[idx]-1, -1, -1):                         #offset = x - xStart or y - yStart
    #Check consecutive pieces in a direction
    
    #check left side
    li = 0
    bli = 0
    ri = 0
    bri = 0    
    
    #count upper left
    while(isConsecutive)   :
        li = li + 1    
        if(x-li < 0 or y+li >= numBLines):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x-li][y+li] == symbol[player])
      
    #check upper left block      
    if(li < 2):
        #check upper left block        
        isConsecutive = True        
        outBoard = False
        
        while(isConsecutive)  : 
            bli = bli + 1    
            if(x-bli < 0 or y+bli >= numBLines):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x-bli][y+bli] == symbol[(player+1)%2])
        
        if(bli >= 4):
            if bli == 4:    
                if outBoard: 
                    blockScore += scoreBlock[2]   #blockClosedThree                    
                if board[x-bli][y+bli] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bli == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x-bli][y+bli] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
     
    #count lower right
    isConsecutive = True
    while(isConsecutive)   :
        ri = ri + 1    
        if(x + ri >= numBLines or y-ri < 0):
            isConsecutive = 0
            break
        isConsecutive =  isConsecutive and (board[x + ri][y - ri] == symbol[player])
    
    #check lower right block
    if (ri < 2):
        #check if block
        isConsecutive = True
        outBoard = False
        
        while(isConsecutive)  : 
            bri = bri + 1    
            if(x + bri >= numBLines or y-bri < 0):
                isConsecutive = False
                outBoard = True
                break
            isConsecutive =  isConsecutive and (board[x + bri][y-bri] == symbol[(player+1)%2])
        
        if(bri >= 4):
            if bri == 4:        
                if outBoard: 
                    blockScore += scoreBlock[2]   #blockClosedThree  
                elif board[x + bri][y - bri] == '.':
                    blockScore += scoreBlock[3]   #blockOpenThree
                else:
                    blockScore += scoreBlock[2]   #blockClosedThree     
            elif bri == 5:
                if outBoard: 
                    blockScore += scoreBlock[4]       #blockClosedFour
                elif board[x + bri][y - bri] != '.':
                    blockScore += scoreBlock[4]       #blockClosedFour
    
    ##if(x == 5 and y == 11):
    ##    print 'li, ri:'
    ##    print li
    ##    print ri
    ##    print board[x]
    ##    print board[x+1]
    ##    print player
    ##    print symbol[player]
    ##    printBoard(rotateBoard(board))
    
    #get create score 
    if(ri < 2):
        #upper left
        if(li < 5 and li >= 2):
            if x-li < 0 or y + li >= numBLines:
                if board[x+1][y-1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x+1 >= numBLines or y-1 < 0:
                if board[x-li][y+li] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x - li][y + li] == '.' and  board[x + 1][y - 1] == symbol[(player+1)%2])  or
                    ( board[x - li][y + li] == symbol[(player+1)%2] and  board[x + 1][y - 1] ==  '.')  ):
                    createScore += scoreClosed[li]  
                if( board[x - li][y + li] == '.' and  board[x + 1][y - 1] == '.' ):
                    createScore += scoreOpen[li]  
        elif (li == 5):
            createScore += scoreOpen[li]
    elif(li < 2):
        #lower right
        if(ri < 5 and ri >= 2):
            if x+ri >= numBLines or y-ri < 0:
                if board[x-1][y+1] == '.':
                    createScore += scoreClosed[li]     ##                
            elif x-1 < 0:
                if board[x+ri][y-ri] == '.':
                    createScore += scoreClosed[li]                               
            else:                   
                if(  ( board[x + ri][y-ri] == '.' and  board[x - 1][y+1] == symbol[(player+1)%2])  or
                    ( board[x + ri][y-ri] == symbol[(player+1)%2] and  board[x - 1][y + 1] ==  '.')  ):
                    createScore += scoreClosed[ri]  
                if( board[x + ri][y - ri] == '.' and  board[x - 1][y + 1] == '.' ):
                    createScore += scoreOpen[ri]  
        elif (ri == 5):
            createScore += scoreOpen[ri]
            
    elif(ri >= 2 and li >= 2):
        numConsec = ri + li - 1
        if x+ri >= numBLines or y-ri < 0:
            if board[x-li][y+li] == '.':
                createScore += scoreClosed[numConsec]     ##                
        elif x-li < 0 or y+li >= numBLines:
            if board[x+ri][y-ri] == '.':
                createScore += scoreClosed[numConsec]                               
        else:                   
            if(  ( board[x + ri][y - ri] == '.' and  board[x - li][y + li] == symbol[(player+1)%2])  or
                ( board[x + ri][y - ri] == symbol[(player+1)%2] and  board[x - li][y + li] ==  '.')  ):
                createScore += scoreClosed[numConsec]  
            if( board[x + ri][y - ri] == '.' and  board[x - li][y + li] == '.' ):
                createScore += scoreOpen[numConsec]  
    
             
    totalScore = createScore + blockScore
    
    return totalScore

    
def evalNewPieceScore(newPiece, board, player):
    score = 0    
    
    if(board[newPiece[0]][newPiece[1]] != '.'):
        print('Already exist a piece')     
        return 0
    else:       
        ##if evalScoreInRow(newPiece, board, player) == scoreOpen[0] or      \
        ##   evalScoreInCol(newPiece, board, player) == scoreOpen[0] or      \
        ##   evalScoreInLeftDiag(newPiece, board, player) == scoreOpen[0] or \
        ##   evalScoreInRightDiag(newPiece, board, player) == scoreOpen[0] :
        ##   
        ##   return scoreOpen[0]
        ##else:  
        score = evalScoreInRow(newPiece, board, player)            \
                + evalScoreInCol(newPiece, board, player)          \
                + evalScoreInLeftDiag(newPiece, board, player)     \
                + evalScoreInRightDiag(newPiece, board, player)    
    
    #if(newPiece[0] == 11 and newPiece[1] == 6):
    #if(newPiece[0] == 5 and newPiece[1] == 11):
    #    print evalScoreInRow(newPiece, board, player)  
    #    print evalScoreInCol(newPiece, board, player)  
    #    print evalScoreInLeftDiag(newPiece, board, player)  
    #    print evalScoreInRightDiag(newPiece, board, player)  
        
    return score

def isLegalMove(x, y, board, player):
    pieceNumber = 0
    if(outOfBoard(x, y)):
        print('Out of Board!\n')
        return Flase 
    else:
        if(board[x][y] == '.') :
        ##check if there are >=1 pieces around
            for i in range(-1, 2, 1) :
                for j in range(-1, 2, 1) :
                    if( not outOfBoard(x+i,y+j)):
                        if(board[x+i][y+j] == symbol[0] or board[x+i][y+j] == symbol[1]):
                            pieceNumber += 1
            if(pieceNumber >= 1):                           
                return True 
            else:
                return False
        else :
            return False

def getLegalMoves(board, player):
    moves = []
    for i in range(0, numBLines):
        for j in range (0, numBLines):
            if isLegalMove(i, j, board, player):
                newMove = [i,j]
                moves.append(newMove)
    return moves
    
    
##tree node    
class treeNode():

    def __init__(self, parent, move, score, depth, player):
        ##self.board = board
        self.parent = parent
        self.move = move
        self.score = score
        self.depth = depth
        self.player = player

##unfinished
def printBoard(board):
    newBoard = rotateBoard(board)
    for i in range (numBLines-1, -1, -1):
        line = ''
        for j in range (0, numBLines):
            line = line + newBoard[i][j]
        print line 

def writeBoard(board):
    newBoard = rotateBoard(board)
    f = open('next_state.txt', 'w')
    for i in range (numBLines-1, -1, -1):
        output = ''
        for j in range (0, numBLines ): 
            output += newBoard[i][j]
        output += '\n'
        f.write(output)
        

def getNewChildNode(parentNode, newMove, board, player, depth):
    ##newBoard = getNewBoard(board, newMove, player)
    score = evalNewPieceScore(newMove, board, player)
    if player != initPlayer:
        score = -score
        
    newChildNode = treeNode(parentNode, newMove, score, depth, player)
    return newChildNode

    
def minMaxDecision(board, player):
    finalMove = None
    depth = 0
    #if player == me:
    utility = -float('inf')
    rootNode = treeNode(None, None, utility, 0, player)
    treeNodes.append(rootNode)
    
    for move in getLegalMoves(board, player):
        outputFile.append(('root,0,%.f' % utility).replace('inf', 'Infinity'))
        childNode = getNewChildNode(rootNode, move, board, player, depth+1)
        treeNodes.append(childNode)
        
        ##boardUpdated = getNewBoard(board, move, player)
        
        v = minValue(board, player, depth+1, move, childNode)
        if utility < v:
            utility = v
            finalMove = move
    outputFile.append(('root,0,%.f' % utility).replace('inf', 'Infinity'))
    
    return finalMove

    
def maxValue(board, player, depth, move, parentNode) :   
    newboard = getNewBoard(board, move, player) 
    
    #if(xcord[move[0]]+ycord[move[1]] == 'G6' and depth == 3):
    #    print 'G6,3:'
    #    print parentNode.score
    #    print abs(parentNode.score)
    
    if (cutOffTest(newboard, depth) or abs(parentNode.score) >= 50000):
        score = 0
        parentTmp = parentNode
        for i in range(depth, 0, -1):
            ##if parentTmp.player == player :
            score += parentTmp.score
            parentTmp = parentTmp.parent
            
        outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, score)).replace('inf', 'Infinity'))
        return score
    v = -float('inf')
    
    for newMove in getLegalMoves(newboard, (player+1)%2):
        outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, v)) .replace('inf', 'Infinity'))
        newChildNode = getNewChildNode(parentNode, newMove, newboard, (player+1)%2, depth+1)
        treeNodes.append(newChildNode)
        
        v = max(v, minValue(newboard, (player+1)%2, depth+1, newMove, newChildNode))
    outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, v)).replace('inf', 'Infinity'))
    return v
                           


def minValue(board, player, depth, move, parentNode):  
    newboard = getNewBoard(board, move, player) 
    
    ##if(xcord[move[0]]+ycord[move[1]] == 'G6' and depth == 3):
    ##    print 'G6,3:'
    ##    print parentNode.score
    ##    print abs(parentNode.score)
    
    if (cutOffTest(newboard, depth) or abs(parentNode.score) >= 50000):
        score = 0;
        parentTmp = parentNode
        for i in range(depth, 0, -1):
            ##if parentTmp.player == player:
            score += parentTmp.score
            parentTmp = parentTmp.parent

        outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, score)).replace('inf', 'Infinity'))
        return score
    v = float('inf') 
    
    for newMove in getLegalMoves(newboard, (player+1)%2):
        outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, v)).replace('inf', 'Infinity'))
        newChildNode = getNewChildNode(parentNode, newMove, newboard, (player+1)%2, depth+1)
        treeNodes.append(newChildNode)
        
        v = min(v, maxValue(newboard, (player+1)%2, depth+1, newMove, newChildNode))
    outputFile.append(('%s,%d,%.f' % (xcord[move[0]]+ycord[move[1]], depth, v)).replace('inf', 'Infinity'))
    
    return v                       
            

def abDecision(board, player):
    finalMove = [0,0]
    depth = 0
    utility = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    rootNode = treeNode(None, None, utility, 0, player)
    treeNodes.append(rootNode)
    
    for move in getLegalMoves(board, player):
        outputFile.append(('root,0,%.f,%.f,%.f' % (utility, alpha, beta)).replace('inf', 'Infinity'))
        childNode = getNewChildNode(rootNode, move, board, player, depth+1)
        treeNodes.append(childNode)
        
        v = abMinValue(board, player, depth+1, alpha, beta, move, childNode)
        if utility < v:
            utility = v
            finalMove = move
        if v >= beta:
            break
        else:
            alpha = max(alpha, v)
            
    outputFile.append(('root,0,%.f,%.f,%.f' % (utility, alpha, beta)).replace('inf', 'Infinity'))
    
    return finalMove
            

def abMaxValue(board, player, depth, alpha, beta, move, parentNode):    
    newboard = getNewBoard(board, move, player) 

    if (cutOffTest(newboard, depth) or abs(parentNode.score) >= 50000):
        score = 0
        parentTmp = parentNode
        for i in range(depth, 0, -1):
            ##if parentTmp.player == player :
            score += parentTmp.score
            parentTmp = parentTmp.parent
            
        outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, score, alpha, beta)).replace('inf', 'Infinity'))
        
        return score
        
    v = -float('inf')
    
    for newMove in getLegalMoves(newboard, (player+1)%2):
        outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, v, alpha, beta)).replace('inf', 'Infinity'))
        newChildNode = getNewChildNode(parentNode, newMove, newboard, (player+1)%2, depth+1)
        treeNodes.append(newChildNode)
        
        v = max(v, abMinValue(newboard, (player+1)%2, depth+1, alpha, beta, newMove, newChildNode))
        if v >= beta:
            break
        else:
            alpha = max(alpha, v)
            
    outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, v, alpha, beta)).replace('inf', 'Infinity'))
    
    return v
                           


def abMinValue(board, player, depth, alpha, beta, move, parentNode)  :

    newboard = getNewBoard(board, move, player) 
    
    #if (cutOffTest(board, depth, player)):
    if (cutOffTest(newboard, depth) or abs(parentNode.score) >= 50000):
        score = 0
        parentTmp = parentNode
        for i in range(depth, 0, -1):
            ##if parentTmp.player == player:
            score += parentTmp.score
            parentTmp = parentTmp.parent
            
        outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, score, alpha, beta)).replace('inf', 'Infinity'))
        return score
        
    v = float('inf') 
    
    for newMove in getLegalMoves(newboard, (player+1)%2):
        outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, v, alpha, beta)).replace('inf', 'Infinity'))
        newChildNode = getNewChildNode(parentNode, newMove, newboard, (player+1)%2, depth+1)
        treeNodes.append(newChildNode)
        
        v = min(v, abMaxValue(newboard, (player+1)%2, depth+1, alpha, beta, newMove, newChildNode))
        if v <= alpha:
            break
        else:
            beta = min(beta, v)
        
    outputFile.append(('%s,%d,%.f,%.f,%.f' % (xcord[move[0]]+ycord[move[1]],  \
             depth, v, alpha, beta)).replace('inf', 'Infinity'))
    
    return v    
            
            
def greedy(board, player):
    maxScore = 0
    maxMove = [0, 0]
    ##print 'NewBOard:'
    ##print board[5]
    ##print board[6]    
    
    for i in range(0, numBLines ):
        for j in range (0, numBLines ):
            if isLegalMove(i, j, board, player):
                newPiece = [i, j]
                moveScore = evalNewPieceScore(newPiece, board, player)
                if moveScore > maxScore:
                    maxScore = moveScore
                    maxMove[0], maxMove[1] = i, j
    
    if maxScore == 0:
        print 'Game End'
        
    #print maxScore
    #print maxMove[0], maxMove[1] 
        
    newboard = getNewBoard(board, maxMove, player)
    return newboard
    

def minMaxAlg(board, player, cutOffDepth):
    initBoard = board
    move = minMaxDecision(initBoard, player)
    newBoard = getNewBoard(initBoard, move, player)
    
    return newBoard
    
def abAlg(board, player, cutOffDepth):
    initBoard = board
    move = abDecision(initBoard, player)
    newBoard = getNewBoard(initBoard, move, player)
    
    return newBoard
    
def rotateBoard(initBoard):
    newBoard = copy.deepcopy(initBoard)
    for i in range (0, numBLines):
        for j in range (0, numBLines):
            newBoard[j][i] = initBoard[i][j]
    return newBoard

##main program

#global variables
global symbol
symbol = ['b','w']
global scoreOpen
scoreOpen = [0, 0, 5, 50, 5000, 50000]    #0, 0, createOpenTwo createOpenThree createOpenFour win
global scoreClosed
scoreClosed = [0, 0,  1, 10, 1000]      #null, createClosedTwo  createClosedThree  createClosedFour
global scoreBlock
scoreBlock = [0, 0, 100, 500, 10000 ]   #null, njull, blockClosedThree blockOpenThree blockClosedFour

global outputFile
global treeNodes 
treeNodes = []

#read input board state
input = getArgs()

algSel = int(input[0])
#print(algSel)

player = int(input[1])
#print(player)

#use (player + 1)%2 to obtain the opponent number
##player1: black, player2: white
player = player - 1 

global initPlayer
initPlayer = player

cutOffDepth = int(input[2])
#print(cutOffDepth)

numBLines = int(input[3])
#print(numBLines)

board = [(' ') for idx in range(0, numBLines )]
ii = 0
for i in range (numBLines + 3, 3, -1):
    board[ii] = list(input[i])
    ii = ii + 1

##rotate board

#print len(board)
#for i in range (numBLines-1, -1, -1):
#    line = ''
#    for j in range (0, numBLines):
#        line = line + board[i][j]
#        line = line + board[i][j]
#    print line
    
newinBoard = rotateBoard(board)
 

#print len(newBoard)
#for i in range (0, numBLines):
#    line = ''
#    for j in range (0, numBLines):
#        line = line + newBoard[i][j]
#    print line

#printBoard(newBoard)

global xcord
xcord = [[] for i in range(0, numBLines)]
for i in range (0, numBLines):
    xcord[i] = chr(ord('A')+i)
    
global ycord
ycord = [[] for i in range(0, numBLines)]
for i in range (0, numBLines):
    ycord[i] = str(i+1)

##Greedy    
if algSel == 1:
   #print 'Select greedy algorithm'
   writeBoard(greedy(newinBoard, player))
   
##MinMax
elif algSel == 2:
   outputFile = ['Move,Depth,Value']
   writeBoard(minMaxAlg(newinBoard, player, cutOffDepth))
   diff = 0
   with open('traverse_log.txt', 'w') as f:
      for log_line in outputFile:
          diff = diff + 1
          #if diff < len(outputFile):
          f.write(log_line+'\n')
          #else:
          #    f.write(log_line)
              
#AlphaBeta   
elif algSel == 3:
   outputFile = ['Move,Depth,Value,Alpha,Beta']
   writeBoard(abAlg(newinBoard, player, cutOffDepth))
   diff = 0
   with open('traverse_log.txt', 'w') as f:
      for log_line in outputFile:
          diff = diff + 1
          #if diff < len(outputFile):
          f.write(log_line+'\n')
          #else:
          #    f.write(log_line)



