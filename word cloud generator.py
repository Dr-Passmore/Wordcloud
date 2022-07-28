import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

textfile = 'Text\Journalistic norms.txt'

output = 'WordClouds\Masters Dissertation.png' 

words = open(textfile, mode = 'r', encoding='utf-8').read()

removed_words = STOPWORDS

cloud = WordCloud(
    mode = "RGBA",
    background_color=None,
    height = 600,
    width = 400,
    min_word_length= 4,
    max_words= 200
)

cloud.generate(words)

cloud.to_file(output)