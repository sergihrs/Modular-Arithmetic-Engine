import re

file = open("tests/eulerTest.txt", "r").read()
ns = re.findall(r"\d+", file)
print(sorted(ns, reverse=True)[:10])
