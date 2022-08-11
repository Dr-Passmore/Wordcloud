text = open("Text\Corbyn Conference Speeches 2015-2019.txt", encoding="utf8")
data = text.read()
words = data.split()
print (len(words))