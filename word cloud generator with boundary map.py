from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os

directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#load text
textfile = open(os.path.join(directory, r'Text\HP book 1.txt'), encoding="utf-8").read()

# load image
image = np.array(Image.open(os.path.join(directory,r'Pictures\Cat_Silhouette_PNG_Transparent_Clip_Art_Image.png')))

# subsample by a factor of 3
image = image[::3, ::3]

# create mask
image_mask = image.copy()
print (len(image_mask.shape))
print(image_mask)
image_mask[image_mask.sum(axis=2) == 0] = 255

#edge detection
edges = np.mean([gaussian_gradient_magnitude(image[:, :, i] / 255., 2) for i in range(3)], axis=0)
image_mask[edges > 0.8] = 255
removed_words = STOPWORDS
cloud = WordCloud(
    mode = "RGBA",
    background_color='green',
    stopwords=removed_words,
    mask=image_mask,
    height = 1280,
    width = 1920,
    min_word_length= 4,
    max_words= 300
)
cloud.generate(textfile)

image_colours = ImageColorGenerator(image)
cloud.recolor(color_func=image_colours)
plt.figure(figsize=(10, 10))
plt.imshow(cloud, interpolation="bilinear")


output = r'WordClouds\HP 1.png' 
cloud.to_file(output)

