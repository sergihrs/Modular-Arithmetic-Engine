import re

file = open("tests/primosTest.txt", "r").read()
ns = re.findall(r"\d+", file)
print(sorted(ns)[:100])
