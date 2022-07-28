import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

words = open('Corbyn Conference Speeches 2015-2019.txt', mode = 'r', encoding='utf-8').read()

removed_words = STOPWORDS

cloud = WordCloud(
    mode = "RGBA",
    background_color=None,
    height = 600,
    width = 400,
    min_word_length= 4,
    max_words= 100
)

cloud.generate(words)

cloud.to_file('Corbyn Conference Speech Output.png')