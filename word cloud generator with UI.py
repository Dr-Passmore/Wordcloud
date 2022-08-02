from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import logging

class wordCloud:
    def __init__(self):
        print("hello world")
        self.directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        self.outputImage = None
        self.Image = None
        self.stopwords = STOPWORDS
        self.image_mask = None
        self.cloud = None
        self.image_colours = None  
        wordCloud.userInterface(self)  
        
    def userInterface(self):
        self.root = tk.Tk()
        self.root.title("Word Cloud Generator")
        #root.configure(background="light green")
        self.root.geometry("600x480")
        title = tk.Label(text="Word Cloud Generator")
        button_preview = tk.Button(
            self.root, 
            text = "Preview", 
            command = lambda : wordCloud.previewCloud(self)
            )
        button_save = tk.Button(
            self.root,
            text = "Save",
            command = lambda : wordCloud.saveWordcloud(self)
        )
        button_exit = tk.Button(
            self.root,
            text = "Exit",
            command = lambda : wordCloud.exit(self)
        )
        name = tk.Label(text="Save Image As ")
        self.saveName = tk.Entry(self.root)
        title.pack()
        #selectFile.pack() 
        button_preview.pack()
        name.pack()
        self.saveName.pack()
        button_save.pack()
        button_exit.pack()
        self.root.mainloop()
    
    def selectImage(self):
        number = 1
        print(number)
        print (self.stopwords)
    
    def selectText(self):
        selectFile = filedialog.askopenfilename(
            initialdir = r"/Text/",
            title = "Select Text File",
            filetypes = (("text files", "txt"),)
            )
        self.textFile = selectFile
        return self.textFile
    
    def cloudShape(Self):
        print("test")
        self.image_mask = self.Image.copy()
        self.image_mask[image_mask.sum(axis=2)==0] = 255
        edges = np.mean([gaussian_gradient_magnitude(self.image[:, :, i]/255., 2) for i in range(3)], axis = 0)
        self.image_mask[edges > 0.8] = 255
        return self.image_mask
    
    def cloudRecolour(self):
        self.image_colours = ImageColorGenerator(self.Image)
        self.cloud.recolor(color_func=self.image_colours)
        return self.cloud
    
    def generateCloud(self):
        logging.info("Cloud Generation with the follow text file - " + self.textFile)
        # !! Prints the entire txt file. Update to just show file name
        self.cloud = WordCloud(
            mode = "RGBA",
            background_color=None,
            stopwords=self.stopwords,
            height = 1280,
            width = 1920,
            mask = self.image_mask,
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
        
    def saveWordcloud(self):
        self.outputImage = self.saveName.get()
        if self.outputImage == "":
            self.outputImage = "WordClouds\Clear Skies.png"
        else:
            self.outputImage = "WordClouds\\" + self.outputImage + ".png"
        print(self.outputImage)
        #Checks to make sure cloud has been generated
        if self.cloud is None:
            #if cloud has been created without using preview it will generate a word cloud
            wordCloud.generateCloud(self)
        else:
            logging.info("Cloud already generated")
        self.cloud.to_file(self.outputImage)
        #Resets the Cloud once saved
        self.cloud = None
    
    def exit(self):
        self.root.destroy()
        
    def testRun(self):
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        wordCloud.generateCloud(self)
        self.cloud.generate(self.textFile)
        output = r'WordClouds\test2.png' 
        self.cloud.to_file(output)
#logging.basicConfig(filename='Word Cloud.log', filemode='w', level=logging.DEBUG)

wordCloud()

#wordCloud.generateCloud(wordCloud.textFile)