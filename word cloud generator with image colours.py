from configparser import Interpolation
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os

directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#load text
textfile = open(os.path.join(directory, r'Text\BA - Political Transformation and the mass media.txt'), encoding="utf-8").read()

image_colour = np.array(Image.open(os.path.join(directory,r'Pictures\flag of the russian federation.png')))

removed_words = STOPWORDS

cloud = WordCloud(
    mode = "RGBA",
    background_color='black',
    stopwords=removed_words,
    height = 1280,
    width = 1920,
    min_word_length= 3,
    max_words= 200
)

cloud.generate(textfile)

#create colours
image = ImageColorGenerator(image_colour)

fig, axes = plt.subplots(1,3)
axes[0].imshow(cloud, interpolation="bilinear")

axes[1].imshow(cloud.recolor(color_func=image), interpolation="bilinear")
axes[2].imshow(image_colour, cmap=plt.cm.gray, interpolation="bilinear")
for ax in axes:
    ax.set_axis_off()
plt.show()