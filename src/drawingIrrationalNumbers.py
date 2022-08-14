import turtle
import time
from decimal import *
from getPi import firstOneMilDigOfPi

def changeBaseGetNum(num, maxNum, base, numToChar, userNumChoice):
    newNum = ""
    quosent = num / base
    count = 1
    newMax = getNewBaseCalc(base, maxNum)
    print()

    if userNumChoice == 1:
        while quosent > 0:
            if count % 1000 == 0:
                percent = round((len(newNum) / newMax) * 100)
                if percent + 1 == 100 or percent + 2 == 100 or percent - 1 == 100 or percent - 2 == 100:
                    print("\t" + str(100) + "% done converting Pi to base " + str(base), end='\r')
                elif percent < 100:
                    print("\t" + str(percent) + "% done converting Pi to base " + str(base), end='\r')

            split = str(quosent).split(".")
            if len(split) == 1:
                split = [split[0], "0"]
            n = round(eval("." + split[1].strip()) * base)
            newNum += numToChar[n]
            quosent = Decimal(split[0])
            quosent /= base
            count += 1

        newNum = newNum[::-1]
        return newNum
    elif userNumChoice == 2:
        while quosent > 0:
            if count % 1000 == 0:
                percent = round((len(newNum) / newMax) * 100)
                if percent + 1 == 100 or percent + 2 == 100 or percent + 3 == 100 or percent - 1 == 100 or percent - 2 == 100 or percent - 3 == 100:
                    print("\t" + str(100) + "% done converting E to base " + str(base), end='\r')
                elif percent < 100:
                    print("\t" + str(percent) + "% done converting E to base " + str(base), end='\r')

            split = str(quosent).split(".")
            if len(split) == 1:
                split = [split[0], "0"]
            n = round(eval("." + split[1].strip()) * base)
            newNum += numToChar[n]
            quosent = Decimal(split[0])
            quosent /= base
            count += 1

        newNum = newNum[::-1]
        return newNum

def getNewBaseCalc(base, maxNum):
    if base == 3:
        newMax = maxNum * 2.0655
    elif base == 4:
        newMax = maxNum * 1.6655
    elif base == 5:
        newMax = maxNum * 1.4655
    elif base == 6:
        newMax = maxNum * 1.3655
    elif base == 7:
        newMax = maxNum * 1.2655
    elif base == 8:
        newMax = maxNum * 1.1655
    elif base == 9:
        newMax = maxNum * 1.0655
    elif base == 11:
        newMax = maxNum * 0.905
    elif base == 12:
        newMax = maxNum * 0.91
    elif base == 13:
        newMax = maxNum * 0.845
    elif base == 14:
        newMax = maxNum * 0.86
    elif base == 15:
        newMax = maxNum * 0.85
    else:
        newMax = maxNum * 0.825
    return newMax

def changeBase(num, maxNum, base, userNumChoice):
    stringNum = str(num)
    num = Decimal(stringNum.replace(".", ""))
    numToChar = {i: "0123456789ABCDEF"[i] for i in range(16)}
    convertedPi = changeBaseGetNum(num, maxNum, base, numToChar, userNumChoice)
    return convertedPi

def pi(maxNum):
    # 1/1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + .... = pi / 4
    numerator = Decimal(1)
    denominator = Decimal(3)
    count = 1
    plusOrMinus = True
    getcontext().prec = maxNum
    pi = Decimal(1)
    while count < maxNum:
        if count % 1000 == 0:
            print("\t" + str(round((count/maxNum) * 100)) + "% done calculating Pi", end='\r')
        if plusOrMinus:
            pi -= numerator / denominator
        else:
            pi += numerator / denominator
        plusOrMinus = not plusOrMinus
        denominator += 2
        count += 1
    pi = pi * 4
    return pi

def eulersNum(maxNum):
    # e = 2 + 1/2 + 1/6 + 1/24 + .....
    numerator = Decimal(1)
    denominator = Decimal(2)
    multiplyer = Decimal(3)
    e = Decimal(2)
    count = 1
    while count < maxNum:
        if count % 1000 == 0:
            print("\t" + str(round((count / maxNum) * 100)) + "% done calculating E", end='\r')
        stringOfDenominator = str(denominator)
        if len(stringOfDenominator) > 23:
            stringOfDenominator = stringOfDenominator[0:23]
            denominator = Decimal(stringOfDenominator)
        e += numerator / denominator
        denominator *= multiplyer
        multiplyer += 1
        count += 1

    print(e)
    return e

def drawing(num, userBase, timeStamp1):
    interator = 0
    base3 = {"0": 120, "1": 240, "2": 360}
    base4 = {"0": 90, "1": 180, "2": 270, "3": 360}
    base5 = {"0": 72, "1": 144, "2": 216, "3": 288, "4": 360}
    base6 = {"0": 60, "1": 120, "2": 180, "3": 240, "4": 300, "5": 360}
    base7 = {"0": (360/7), "1": ((360/7) * 2), "2": ((360/7) * 3), "3": ((360/7) * 4), "4": ((360/7) * 5), "5": ((360/7) * 6), "6": ((360/7) * 7)}
    base8 = {"0": 45, "1": 90, "2": 135, "3": 180, "4": 225, "5": 270, "6": 315, "7": 360}
    base9 = {"0": 40, "1": 80, "2": 120, "3": 160, "4": 200, "5": 240, "6": 280, "7": 320, "8": 360}
    base10 = {"0": 36, "1": 72, "2": 108, "3": 144, "4": 180, "5": 216, "6": 252, "7": 288, "8": 324, "9": 360}
    base11 = {"0": (360/11), "1": ((360/11) * 2), "2": ((360/11) * 3), "3": ((360/11) * 4), "4": ((360/11) * 5), "5": ((360/11) * 6), "6": ((360/11) * 7), "7": ((360/11) * 8), "8": ((360/11) * 9), "9": ((360/11) * 10), "A": ((360/11) * 11)}
    base12 = {"0": 30, "1": 60, "2": 90, "3": 120, "4": 150, "5": 180, "6": 210, "7": 240, "8": 270, "9": 300, "A": 330, "B": 360}
    base13 = {"0": (360/13), "1": ((360/13) * 2), "2": ((360/13) * 3), "3": ((360/13) * 4), "4": ((360/13) * 5), "5": ((360/13) * 6), "6": ((360/13) * 7), "7": ((360/13) * 8), "8": ((360/13) * 9), "9": ((360/13) * 10), "A": ((360/13) * 11), "B": ((360/13) * 12), "C": ((360/13) * 13)}
    base14 = {"0": (360/14), "1": ((360/14) * 2), "2": ((360/14) * 3), "3": ((360/14) * 4), "4": ((360/14) * 5), "5": ((360/14) * 6), "6": ((360/14) * 7), "7": ((360/14) * 8), "8": ((360/14) * 9), "9": ((360/14) * 10), "A": ((360/14) * 11), "B": ((360/14) * 12), "C": ((360/14) * 13), "D": ((360/14) * 14)}
    base15 = {"0": 24, "1": 48, "2": 72, "3": 96, "4": 120, "5": 144, "6": 168, "7": 192, "8": 216, "9": 240, "A": 264, "B": 288, "C": 312, "D": 336, "E": 360}
    base16 = {"0": 22.5, "1": 45, "2": 67.5, "3": 90, "4": 112.5, "5": 135, "6": 157.5, "7": 180, "8": 202.5, "9": 225, "A": 247.5, "B": 270, "C": 292.5, "D": 315, "E": 337.5, "F": 360}
    allBases = {3: base3, 4: base4, 5: base5, 6: base6, 7: base7, 8: base8, 9: base9, 10: base10, 11: base11, 12: base12, 13: base13, 14: base14, 15: base15, 16: base16}
    base = allBases[userBase]
    if num[1] == ".":
        num = num.replace('.', '')
    print()
    print("Gathering Data:")
    startTime = time.time()
    percent = 0
    while interator < len(num):
        if interator % 1000 == 0:
            percent = round((interator / len(num)) * 100)
            duration = time.time() - startTime
            estimatedTime = (((len(num) - interator) * duration) / (interator + 1))
            m, s = divmod(estimatedTime, 60)
            h, m = divmod(m, 60)
            print("\tEstimated Time: " + '{:d}% {:d}h {:02d}m {:02d}s'.format(int(percent), int(h), int(m), int(s)), end="\r")

        getNumber = num[interator]
        heading = base[getNumber]
        interator += 1
        turtle.setheading(heading)
        turtle.forward(10)
    turtle.hideturtle()

    print()
    print("Complete!")
    timeStamp2 = time.time()
    timePassed = ((timeStamp2 - timeStamp1) / 60) / 60
    if timePassed < 1:
        timePassed *= 60
        print("Total Time: " + '{:.2f}'.format(timePassed) + "Minutes")
    elif timePassed >= 1:
        print("Total Time: " + '{:.2f}'.format(timePassed) + " Hours")
    turtle.done()

def main():
    print("\t\tDrawing Program")
    print()
    print("(1) Pi")
    print("(2) E")
    userNumChoice = int(input("Pi or E: "))
    if userNumChoice == 1:
        print("Ok Pi")
        userBase = int(input("What numarical Base (3-16): "))
        maxNum = int(input("How long should Pi be: "))
        print()
        timeStamp1 = time.time()
        turtle.screensize(100000, 100000)
        turtle.speed(0)
        if userBase < 3 or userBase > 16 or maxNum % 10 != 0:
            print("Invalid Input. Try again")
            main()
        elif maxNum == 1000000 and userBase == 10:
            drawing(firstOneMilDigOfPi(), userBase, timeStamp1)
        else:
            baseTenPi = pi(maxNum)
            if userBase == 10:
                drawing(str(baseTenPi), userBase, timeStamp1)
            else:
                newPi = changeBase(baseTenPi, maxNum, userBase, userNumChoice)
                drawing(newPi, userBase, timeStamp1)
    elif userNumChoice == 2:
        print("Ok E")
        userBase = int(input("What Base (3-16): "))
        maxNum = int(input("How long should E be: "))
        print()
        timeStamp1 = time.time()
        turtle.screensize(100000, 100000)
        turtle.speed(0)
        if userBase < 3 or userBase > 16 or maxNum % 10 != 0:
            print("Invalid Input. Try again")
            main()
        else:
            goToNum = maxNum
            baseTenE = ''
            with open('/Users/nathanstott/PycharmProjects/drawingIrrationalNumbers/src/e') as file:
                while goToNum > 0:
                    num = file.read(1).strip()
                    if num == '.':
                        num.replace('.', '')
                    if num == '\\':
                        num.replace('\\', '')
                    if num == 'n':
                        num.replace('n', '')
                    baseTenE += num
                    goToNum -= 1
            if userBase == 10:
                drawing(str(baseTenE), userBase, timeStamp1)
            else:
                newE = changeBase(int(baseTenE), maxNum, userBase, userNumChoice)
                drawing(str(newE), userBase, timeStamp1)
    else:
        print("Invalid Input. Try again")
        main()

main()
