from decimal import *

def changeBaseGetNum(num, maxNum, base, numToChar, userNumChoice):
    print("2")
    newNum = ""
    quosent = num / base
    count = 1
    newMax = getNewBaseCalc(base, maxNum)
    print()

    if userNumChoice == 1:
        print("3")
        while quosent > 0:
            if count % 1000 == 0:
                poop = round((len(newNum) / newMax) * 100)
                if poop + 1 == 100 or poop + 2 == 100 or poop - 1 == 100 or poop - 2 == 100:
                    print("\t" + str(100) + "% done converting Pi to base " + str(base), end='\r')
                elif poop < 100:
                    print("\t" + str(poop) + "% done converting Pi to base " + str(base), end='\r')

            newNum = getNewNumCalculation(quosent, newNum, numToChar, base, count)

        newNum = newNum[::-1]
        return newNum
    elif userNumChoice == 2:
        while quosent > 0:
            if count % 1000 == 0:
                poop = round((len(newNum) / newMax) * 100)
                if poop + 1 == 100 or poop + 2 == 100 or poop + 3 == 100 or poop - 1 == 100 or poop - 2 == 100 or poop - 3 == 100:
                    print("\t" + str(100) + "% done converting E to base " + str(base), end='\r')
                elif poop < 100:
                    print("\t" + str(poop) + "% done converting E to base " + str(base), end='\r')

            newNum = getNewNumCalculation(quosent, newNum, numToChar, base, count)

        newNum = newNum[::-1]
        return newNum

def getNewBaseCalc(base, maxNum):
    print("4")
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

def getNewNumCalculation(quosent, newNum, numToChar, base, count):
    print("5")
    split = str(quosent).split(".")
    if len(split) == 1:
        split = [split[0], "0"]
    n = round(eval("." + split[1].strip()) * base)
    newNum += numToChar[n]
    quosent = Decimal(split[0])
    quosent /= base
    count += 1
    return newNum

def changeBase(num, maxNum, base, userNumChoice):
    print("1")
    stringNum = str(num)
    num = Decimal(stringNum.replace(".", ""))
    numToChar = {i: "0123456789ABCDEF"[i] for i in range(16)}
    convertedPi = changeBaseGetNum(num, maxNum, base, numToChar, userNumChoice)
    return convertedPi