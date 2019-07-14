import os
import sys

title = "Goblin Slayer"
files = os.listdir("D://Manga/{}".format(title))
maxEp = []
for file in files:
    if file.split(".")[-1] == "mobi" or file.split(".")[-1] == "py":
        continue
    maxEp.append(int(file.split(" ")[-1]))
print(max(maxEp))
