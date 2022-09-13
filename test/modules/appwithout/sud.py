import numpy as np


def getIntegersColumn(sudoku,j):
    i=0
    oneBy9=sudoku[i:i+9,j]
    sol=oneBy9[oneBy9!=0]
    return sol

def getIntegersRow(sudoku,i):
    j=0
    nineBy1=sudoku[i,j:j+9]
    sol=nineBy1[nineBy1!=0]
    return sol

def getIntegersSquare(sudoku,i,j):
    n=i-i%3#start of the square row
    m=j-j%3#start of the square column
    threeBy3=sudoku[n:n+3,m:m+3]
    sol=threeBy3[threeBy3!=0]#extracted contraints within a square
    return sol

def getMissingNo(npArr):
    if npArr.size<8:
        lis=[]
        for i in range(1,10):
            if not np.isin(i,npArr):
                lis.append(i)
        return [lis,0]
        
    elif npArr.size==8:
        for i in range(1,10):
            if not np.isin(i,npArr):
                return [i,-1]
    else:
        return "broken"
            
def getConstraints(sudoku,i,j):
    
    a=getIntegersSquare(sudoku,i,j)
    b=getIntegersColumn(sudoku,j)
    c=getIntegersRow(sudoku,i)
    
    cons=np.concatenate([a,b,c])
    
    return np.unique(cons)
def checkSudokuSolved(sudoku):
    if 0 in sudoku :
        return False
    elif -1 in sudoku:
        return False
    else:
        return True

def quick_plugs(sudoku):
    flag=True
    while flag==True:
        flag=False
        for i in range(0,9):
            for j in range(0,9):
                #print(c," -----here i and j:",i," ,",j)
                if sudoku[i,j]==0:
                    cons=getConstraints(sudoku,i,j)
                    missing=getMissingNo(cons)
                    if missing=="broken":
                        return np.full((9,9), -1, dtype=float)
                    elif missing[1]==-1:
                        sudoku[i,j]=missing[0]
                        flag=True
    return sudoku

def sudoku_solver(sudoku):
    backup=sudoku.copy()
    c =quick_plugs(sudoku)
    if checkSudokuSolved(c)==True:
        return c
    else:
        while 0 in c:
            for i in range(0,9):
                for j in range(0,9):
                    if c[i,j]==0:
                        cons=getConstraints(c,i,j)
                        missing=getMissingNo(cons)
                        if missing[1]==0:
                            t=c.copy()
                            possibilities=missing[0]
                            for possNo in possibilities:
                                h=c.copy()
                                h[i,j]=possNo
                                c=sudoku_solver(h)
                                if checkSudokuSolved(c)==True:
                                    return c
                                if(c[0,0]==-1):
                                    c=t
                                else:
                                    pass
                            return backup

        return c



	#print("sudoku 1 is complete:",checkSudokuSolved(sudokus[1]))
