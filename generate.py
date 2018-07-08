import argparse
import random
import re
import sys


def get_name(filename):
    MINLEN = 3
    LOOKAHEAD = 3
    LOOKBEHIND = 1
    r = re.compile("([A-Z]+)\s*(\d)\.(\d{3})")
    names = []
    with open("androg.txt", "r") as f:
        for line in f:
            m = r.match(line)
            if m:
                name, percint, percfrac = m.groups()
                names.append((name, int(percint) * 1000 + int(percfrac)))

    letters = [None]
    letter_list = {letter: {"total": 0} for letter in letters}
    # one letter lookbehind & lookahead, for now

    for name, perc in names:  # generate table
        letter_list[None][name[0]] = letter_list[None].get(name[0], 0) + perc
        letter_list[None]["total"] += perc
        for i, _ in enumerate(name):
            letter = name[max(0, i - LOOKBEHIND + 1): i + 1].rjust(LOOKBEHIND, "-")
            tperc = perc  # // name.count(letter)
            next = name[i + 1: i + 1 + LOOKAHEAD].ljust(LOOKAHEAD, "-")
            letter_list.setdefault(letter, {"total": 0})
            letter_list[letter][next] = letter_list[letter].get(next, 0) + tperc
            letter_list[letter]["total"] += perc

    my_name = ""
    last_letter = None
    while not last_letter or last_letter[-1] != '-':
        ws = letter_list[last_letter]
        num = random.randint(0, ws["total"])
        for letter, value in ws.items():
            if letter == "total":
                continue
            num -= value
            if num < 0 and not (letter[-1] == "-" and len((my_name + letter).rstrip("-")) < MINLEN):
                my_name += letter
                last_letter = my_name[-LOOKBEHIND:].rjust(LOOKBEHIND, "-")
                break

    return my_name.rstrip("-").title()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gender', nargs='?', default='androg', choices=['male', 'female', 'androg'])
    args = parser.parse_args()
    print(get_name(args.gender))


if __name__ == '__main__':
    main()
