"""
issue:
1.如何去掉太简单了的单词，还有空格之类的
2.不能用line.aplit(" "),会出现类似 "  community." " 的情况 
"""
import importlib,sys
importlib.reload(sys)
from collections import defaultdict

words = defaultdict(int)
with open("../collection.txt","r",encoding="utf-8") as f:
    for line in f.readlines():
        w = line.split(" ")
        for word in w:
                words[word] += 1

sortedWords = sorted(words.items(),key = lambda e : e[1],reverse=True )
print(sortedWords)
for pair in sortedWords:
    with open("words.txt","a+",encoding="utf-8") as f:
        f.write(pair[0])
        f.write("\n")
