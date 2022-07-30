from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk

class wordCloud:
    def __init__(self):
        print("hello world")
        self.directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        self.textFile = None
        self.outputImage = None
        self.Image = None
        self.stopwords = STOPWORDS
        wordCloud.selectImage(self)
        root = tk.Tk()

        root.mainloop()
        wordCloud.testRun(self)     
        
    def selectImage(self):
        number = 1
        print(number)
        print (self.stopwords)
    
    def selectText(self):
        print("test")
    
    def cloudShape(Self):
        print("test")
        
    def generateCloud(self,textFile):
        self.cloud = WordCloud(
            mode = "RGBA",
            background_color='black',
            stopwords=self.stopwords,
            height = 1280,
            width = 1920,
            min_word_length= 3,
            max_words= 200
        )
        return self.cloud
        
    def previewCloud(self):   
        print("test") 
    
    def testRun(self):
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        wordCloud.generateCloud(self, self.textFile)
        self.cloud.generate(self.textFile)
        output = r'WordClouds\test.png' 
        self.cloud.to_file(output)
wordCloud()

#wordCloud.generateCloud(wordCloud.textFile)