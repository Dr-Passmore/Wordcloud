from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk
from tkinter import messagebox
import logging

class wordCloud:
    def __init__(self):
        print("hello world")
        self.directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        self.outputImage = None
        self.Image = None
        self.stopwords = STOPWORDS
        self.mask = None
        #wordCloud.selectImage(self)
        
        
        #wordCloud.testRun(self)   
        #wordCloud.userInterface(self)  
        wordCloud.previewCloud(self)
        
    def userInterface(self):
        root = tk.Tk()
        root.title("Word Cloud Generator")
        #root.configure(background="light green")
        root.geometry("600x480")
        title = tk.Label(text="Word Cloud Generator")
        title.pack()
        root.mainloop()
    
    def selectImage(self):
        number = 1
        print(number)
        print (self.stopwords)
    
    def selectText(self):
        print("test")
    
    def cloudShape(Self):
        print("test")
        
    def generateCloud(self):
        logging.info("Cloud Generation with the follow text file - " + self.textFile)
        # !! Prints the entire txt file. Update to just show file name
        self.cloud = WordCloud(
            mode = "RGBA",
            background_color=None,
            stopwords=self.stopwords,
            height = 1280,
            width = 1920,
            mask = self.mask,
            min_word_length= 3,
            max_words= 200
        )
        self.cloud.generate(self.textFile)
        
        return self.cloud
        
    def previewCloud(self):   
        logging.info("Preview Cloud Selected")
        if self.textFile is None:
            logging.warn('No .txt file selected')
            messagebox.showerror("Text File Error", "No Text File Selected")
        else:
            wordCloud.generateCloud(self)
            
            fig, axes = plt.subplots(1,1)
            axes.imshow(self.cloud, interpolation="bilinear")
            axes.set_axis_off()
            #for ax in axes:
                #ax.set_axis_off()
            plt.show()
        print("test") 
    
    def testRun(self):
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        wordCloud.generateCloud(self)
        self.cloud.generate(self.textFile)
        output = r'WordClouds\test2.png' 
        self.cloud.to_file(output)
#logging.basicConfig(filename='Word Cloud.log', filemode='w', level=logging.DEBUG)

wordCloud()

#wordCloud.generateCloud(wordCloud.textFile)