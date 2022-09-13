import time
import matplotlib.pyplot as plt
import numpy as np
import cProfile
import io
import os
import pstats
import time
import pandas as pd
import modules.app.sudoku_ortools as sor
import modules.appwithout.sud as swor

def timeAverageSudokus(sudokus):
    averageTimeSor=0
    averageTimeSwor=0
    sumSor=0
    sumSwor=0
    for sudoku in sudokus:
        start = time.time()
        sor.sudoku_solver(sudoku)
        end = time.time()
        sumSor = sumSor + (end - start)

        #second timing
        start = time.time()
        swor.sudoku_solver(sudoku)
        end = time.time()
        sumSwor = sumSwor + (end - start)
    averageTimeSor = round(sumSor/len(sudokus), 3)
    averageTimeSwor = round(sumSwor/len(sudokus), 3)

    return([averageTimeSor,averageTimeSwor])

def loadSudokus():
    sudokus = np.load("data/sudokus.npy")
    solutions = np.load("data/sudoku_solutions.npy")

    return([sudokus,solutions])

def generateData(sudokus):
    easySudokuTimes=timeAverageSudokus(sudokus[0:5])
    mediumSudokuTimes=timeAverageSudokus(sudokus[5:10])
    invalidSudokuTimes=timeAverageSudokus(sudokus[10:15])
    complexSudokuTimes=timeAverageSudokus(sudokus[15:20])
    
    return([easySudokuTimes, mediumSudokuTimes, invalidSudokuTimes, complexSudokuTimes])

def printDataGen(easySudokuTimes, mediumSudokuTimes, invalidSudokuTimes, complexSudokuTimes):
    print("The average time spent by the non-ortools sudoku on EASY sudokus is : ", easySudokuTimes[0])
    print("Whilst for the ortools sudoku it took : ", easySudokuTimes[1])
    print()
    print("The average time spent by the non-ortools sudoku on MEDIUM sudokus is : ", mediumSudokuTimes[0])
    print("Whilst for the ortools sudoku it took : ", mediumSudokuTimes[1])
    print()
    print("The average time spent by the non-ortools sudoku on INVALID sudokus is : ", invalidSudokuTimes[0])
    print("Whilst for the ortools sudoku it took : ", invalidSudokuTimes[1])
    print()
    print("The average time spent by the non-ortools sudoku on COMPLEX sudokus is : ", complexSudokuTimes[0])
    print("Whilst for the ortools sudoku it took : ", complexSudokuTimes[1])
    print()

def plotTimes(easySudokuTimes, mediumSudokuTimes, invalidSudokuTimes, complexSudokuTimes):
    labels=['Easy', 'Medium', 'Invalid', 'Complex']
    ortoolTimes = (easySudokuTimes[0], mediumSudokuTimes[0], invalidSudokuTimes[0], complexSudokuTimes[0])
    nonortoolTimes = (easySudokuTimes[1], mediumSudokuTimes[1], invalidSudokuTimes[1], complexSudokuTimes[1])

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, ortoolTimes, width, label='OrTool')
    rects2 = ax.bar(x + width/2, nonortoolTimes, width, label='Non-OrTool')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Time(s)')
    ax.set_title('OrTool vs Non-OrTool Sudoku Solver')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()

def runDifference():
    listOfTimes=generateData(listOfSudokus[0])
    printDataGen(listOfTimes[0], listOfTimes[1], listOfTimes[2], listOfTimes[3])
    plotTimes(listOfTimes[0], listOfTimes[1], listOfTimes[2], listOfTimes[3])


    
def prof_to_csv(prof: cProfile.Profile):
    out_stream = io.StringIO()
    pstats.Stats(prof, stream=out_stream).print_stats()
    result = out_stream.getvalue()
    # chop off header lines
    result = 'ncalls' + result.split('ncalls')[-1]
    lines = [','.join(line.rstrip().split(None, 5)) for line in result.split('\n')]
    return '\n'.join(lines)

def cProfileR(sudoku):
    if not os.path.exists('cProfileGeneratedData'):
        os.makedirs('cProfileGeneratedData')
    pr = cProfile.Profile()
    pr.enable()
    sor.sudoku_solver(sudoku)
    pr.disable()
    
    result = io.StringIO()
    pstats.Stats(pr,stream=result).print_stats()
    result=result.getvalue()
    # chop the string into a csv-like buffer
    result='ncalls'+result.split('ncalls')[-1]
    result='\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
    # save it to disk
    nameFileSor="cProfileGeneratedData/"+"profsor"+str(int(time.time()))+".csv"
    with open(nameFileSor, 'w+') as f:
        #f=open(result.rsplit('.')[0]+'.csv','w')
        f.write(result)
        f.close()
    

    pr1 = cProfile.Profile()
    pr1.enable()
    swor.sudoku_solver(sudoku)
    pr1.disable()
    
    result = io.StringIO()
    pstats.Stats(pr1,stream=result).print_stats()
    result=result.getvalue()
    # chop the string into a csv-like buffer
    result='ncalls'+result.split('ncalls')[-1]
    result='\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
    # save it to disk
    nameFileSwor="cProfileGeneratedData/"+"profswor"+str(int(time.time()))+".csv"
    with open(nameFileSwor, 'w+') as f:
        #f=open(result.rsplit('.')[0]+'.csv','w')
        f.write(result)
        f.close()

    
listOfSudokus=loadSudokus()
cProfileR(listOfSudokus[0][19])
runDifference()
