from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os

directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#load text
textfile = open(os.path.join(directory, r'Text\BA - Political Transformation and the mass media.txt'), encoding="utf-8").read()

# load image
image = np.array(Image.open(os.path.join(directory,r'Pictures\Moscow test.png')))

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

cloud = WordCloud(
    mode = "RGBA",
    background_color=None,
    mask=image_mask,
    height = 400,
    width = 600,
    min_word_length= 4,
    max_words= 200
)
cloud.generate(textfile)

image_colours = ImageColorGenerator(image)
cloud.recolor(color_func=image)
plt.figure(figsize=(10, 10))
plt.imshow(cloud, interpolation="bilinear")


output = r'WordClouds\undergrad Dissertation.png' 
cloud.to_file(output)

