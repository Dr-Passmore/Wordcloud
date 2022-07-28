import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

textfile = r'Text\Corbyn Conference Speeches 2015-2019.txt'

output = r'WordClouds\Corbyn Conference Speech Output.png' 

words = open(textfile, mode = 'r', encoding='utf-8').read()

removed_words = STOPWORDS

cloud = WordCloud(
    mode = "RGBA",
    background_color=None,
    stopwords=removed_words,
    height = 600,
    width = 400,
    min_word_length= 3,
    max_words= 200
)

cloud.generate(words)

cloud.to_file(output)