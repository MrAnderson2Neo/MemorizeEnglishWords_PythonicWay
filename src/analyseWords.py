from collections import defaultdict

words = defaultdict(int)
with open("../collection.txt","r") as f:
    for line in f.readlines():
        w = line.split(" ")
        for word in w:
                words[word] += 1

sortedWords = sorted(words.items(),key = lambda e : e[1],reverse=True )
print(sortedWords)
for pair in sortedWords:
    with open("words.txt","a+") as f:
        f.write(pair[0])
        f.write("\n")