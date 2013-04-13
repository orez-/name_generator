import random
import re
from string import uppercase
import sys

LOOKAHEAD = 3
r = re.compile("([A-Z]+)\s*(\d)\.(\d{3})")
names = []
with open("androg.txt", "r") as f:
    for line in f:
        m = r.match(line)
        if m:
            name, percint, percfrac = m.groups()
            names.append((name, int(percint) * 1000 + int(percfrac)))

letters = list(uppercase) + [None]
letter_list = {letter: {"total": 0} for letter in letters}
# one letter lookbehind & lookahead, for now

for name, perc in names:  # generate table
    letter_list[None][name[0]] = letter_list[None].get(name[0], 0) + perc
    letter_list[None]["total"] += perc
    for i, letter in enumerate(name):
        tperc = perc // name.count(letter)
        next = name[i + 1: i + 1 + LOOKAHEAD].ljust(LOOKAHEAD, "-")
        letter_list[letter][next] = letter_list[letter].get(next, 0) + tperc
        letter_list[letter]["total"] += perc

my_name = ""
last_letter = None
while last_letter != '-':
    ws = letter_list[last_letter]
    num = random.randint(0, ws["total"])
    for letter, value in ws.iteritems():
        if letter == "total":
            continue
        num -= value
        if num < 0:
            my_name += letter
            last_letter = my_name[-1]
            break

my_name = my_name.rstrip("-")
print my_name