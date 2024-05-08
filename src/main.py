import turtle
import time
from decimal import *
from angles import all_bases


def change_base_get_num(num, max_num, base, num_to_char):
    new_num = ""
    quosent = num / base
    count = 1
    new_max = get_new_base_calc(base, max_num)
    print()
    while quosent > 0:
        if count % 1000 == 0:
            percent = round((len(new_num) / new_max) * 100)
            if percent + 1 == 100 or percent + 2 == 100 or percent - 1 == 100 or percent - 2 == 100:
                print("\t" + str(100) + "% done converting Pi to base " + str(base), end='\r')
            elif percent < 100:
                print("\t" + str(percent) + "% done converting Pi to base " + str(base), end='\r')
        split = str(quosent).split(".")
        if len(split) == 1:
            split = [split[0], "0"]
        n = round(eval("." + split[1].strip()) * base)
        new_num += num_to_char[n]
        quosent = Decimal(split[0])
        quosent /= base
        count += 1

    new_num = new_num[::-1]
    return new_num


def get_new_base_calc(base, max_num):
    if base == 3:
        new_max = max_num * 2.0655
    elif base == 4:
        new_max = max_num * 1.6655
    elif base == 5:
        new_max = max_num * 1.4655
    elif base == 6:
        new_max = max_num * 1.3655
    elif base == 7:
        new_max = max_num * 1.2655
    elif base == 8:
        new_max = max_num * 1.1655
    elif base == 9:
        new_max = max_num * 1.0655
    elif base == 11:
        new_max = max_num * 0.905
    elif base == 12:
        new_max = max_num * 0.91
    elif base == 13:
        new_max = max_num * 0.845
    elif base == 14:
        new_max = max_num * 0.86
    elif base == 15:
        new_max = max_num * 0.85
    else:
        new_max = max_num * 0.825
    return new_max


def change_base(num, max_num, base):
    string_num = str(num)
    num = Decimal(string_num.replace(".", ""))
    num_to_char = {i: "0123456789ABCDEF"[i] for i in range(16)}
    converted_pi = change_base_get_num(num, max_num, base, num_to_char)
    return converted_pi


def get_pi(max_num):
    # 1/1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + .... = pi / 4
    numerator = Decimal(1)
    denominator = Decimal(3)
    count = 1
    is_minus = True
    getcontext().prec = max_num
    pi = Decimal(1)
    while count < max_num:
        if count % 1000 == 0:
            print("\t" + str(round((count / max_num) * 100)) + "% done calculating Pi", end='\r')
        if is_minus:
            pi -= numerator / denominator
        else:
            pi += numerator / denominator
        is_minus = not is_minus
        denominator += 2
        count += 1
    pi = pi * 4
    return pi


def drawing(num, user_base, time_stamp1):
    interator = 0
    base = all_bases[user_base]
    if num[1] == ".":
        num = num.replace('.', '')
    print()
    print("Gathering Data:")
    start_time = time.time()
    while interator < len(num):
        if interator % 1000 == 0:
            percent = round((interator / len(num)) * 100)
            duration = time.time() - start_time
            estimated_time = (((len(num) - interator) * duration) / (interator + 1))
            m, s = divmod(estimated_time, 60)
            h, m = divmod(m, 60)
            print("\tEstimated Time: " + '{:d}% {:d}h {:02d}m {:02d}s'.format(int(percent), int(h), int(m), int(s)),
                  end="\r")

        get_number = num[interator]
        heading = base[get_number]
        interator += 1
        turtle.setheading(heading)
        turtle.forward(10)
    turtle.hideturtle()

    print()
    print("Complete!")
    time_stamp2 = time.time()
    time_passed = ((time_stamp2 - time_stamp1) / 60) / 60
    if time_passed < 1:
        time_passed *= 60
        print("Total Time: " + '{:.2f}'.format(time_passed) + "Minutes")
    elif time_passed >= 1:
        print("Total Time: " + '{:.2f}'.format(time_passed) + " Hours")
    turtle.done()


def main():
    print("\t\tDrawing Program")
    print("Pi")
    user_base = int(input("What numerical Base (3-16): "))
    max_num = int(input("How long should Pi be: "))
    print()
    time_stamp1 = time.time()
    turtle.screensize(10000, 10000)
    turtle.speed(0)
    if user_base < 3 or user_base > 16 or max_num % 10 != 0:
        print("Invalid Input. Try again.")
    else:
        base_ten_pi = get_pi(max_num)
        if user_base == 10:
            drawing(str(base_ten_pi), user_base, time_stamp1)
        else:
            new_pi = change_base(base_ten_pi, max_num, user_base)
            drawing(new_pi, user_base, time_stamp1)


main()
