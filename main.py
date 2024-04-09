from random import randint

from PyQt6 import pip
# validate input

team_red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
team_black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
zero = 0

# main cycle

while True:
    command = input()
    analyze_command(command)

    this_roll = randint(0, 37)
    analuze_roll(this_roll)












