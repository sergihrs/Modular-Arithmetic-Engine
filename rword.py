import random as r


def random_word():
    with open("words.txt", "r", encoding="utf-8") as f:
        insults = f.readlines()
    return insults[r.randint(0, len(insults) - 1)].strip()
