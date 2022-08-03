from configparser import Interpolation
from matplotlib import image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk
from tkinter import messagebox, filedialog, IntVar, Checkbutton
import logging

class wordCloud:
    def __init__(self):
        self.directory = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        #Checks to make sure Folders exist and if not creates them
        if not os.path.exists(r'Pictures'):
            os.makedirs(r'Pictures')
        if not os.path.exists(r'Text'):
            os.makedirs(r'Text')
        if not os.path.exists(r'WordClouds'):
            os.makedirs(r'WordClouds')
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        self.outputImage = None
        self.Image = 'Pictures\\flag of the russian federation.png'
        self.stopwords = STOPWORDS
        self.image_mask = None
        self.cloud = None
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
        
        self.recolour = IntVar()
        checkRecolour = Checkbutton(
            self.root,
            text = "Recolour Text", 
            variable = self.recolour, 
            onvalue = 1, 
            offvalue = 0, 
            height=2, 
            width = 20)
        
        self.shapeCloud = IntVar()
        checkShape = Checkbutton(
            self.root,
            text = "Use Image Boundary Map",
            variable= self.shapeCloud,
            onvalue = 1, 
            offvalue = 0,
            height = 2,
            width = 20)
        
        name = tk.Label(text="Save Image As ")
        self.saveName = tk.Entry(self.root)
        self.saveName.insert(0, "Clear Skies")
        title.pack()
        #selectFile.pack() 
        button_preview.pack()
        checkRecolour.pack()
        checkShape.pack()
        name.pack()
        self.saveName.pack()
        button_save.pack()
        button_exit.pack()
        self.root.mainloop()
    
    def selectImage(self):
        selectImage = filedialog.askopenfilename(
            initialdir = r"Pictures",
            title = "Select Image File",
            filetypes = (("Image files", "png"),)
        )
        self.ImageName =selectImage
        return self.ImageName
    
    def selectText(self):
        selectFile = filedialog.askopenfilename(
            initialdir = r"/Text/",
            title = "Select Text File",
            filetypes = (("text files", "txt"),)
            )
        self.textFile = selectFile
        return self.textFile
    
    def checkboxStatus(self):
        logging.info('Checking whether tick boxes are selected')
        self.shapecloudCheck = self.shapeCloud.get()
        self.recolouredCheck = self.recolour.get()
        self.numberTicked = self.shapecloudCheck + self.recolouredCheck
        print(self.numberTicked)
        return self.numberTicked
    
    def cloudShape(self):
        if self.Image is None:
            logging.warn('No .png file selected')
            messagebox.showerror("Image File Error", "No Image File Selected")
        else:
            self.Image = np.array(Image.open(os.path.join(self.Image)))
            self.image_mask = self.Image.copy()
            self.image_mask[self.image_mask.sum(axis=2)==0] = 255
            edges = np.mean([gaussian_gradient_magnitude(self.image[:, :, i]/255., 2) for i in range(3)], axis = 0)
            self.image_mask[edges > 0.8] = 255
            return self.image_mask
    
    def cloudRecolour(self):
        if self.Image is None:
            logging.warn('No .png file selected')
            messagebox.showerror("Image File Error", "No Image File Selected")
        else:
            self.Image = np.array(Image.open(os.path.join(self.Image)))
            self.image_colours = ImageColorGenerator(self.Image)
            self.cloud.recolor(color_func=self.image_colours)
            return self.cloud
    
    def generateCloud(self):
        logging.info("Cloud Generation checking the Text File Selected")
        wordCloud.checkboxStatus(self)
        if self.textFile is None:
            logging.warn('No .txt file selected')
            messagebox.showerror("Text File Error", "No Text File Selected")
        else:
            logging.info("Text file found")
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
        wordCloud.generateCloud(self)
        if self.numberTicked == 0:
            fig, axes = plt.subplots(1,1)
            axes.imshow(self.cloud, interpolation="bilinear")
            axes.set_axis_off()
            
        elif self.numberTicked == 1:
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(self.cloud, interpolation="bilinear")
            if self.recolouredCheck == 1:
                wordCloud.cloudRecolour(self)
                axes[1].imshow(self.cloud, interpolation="bilinear")
                for ax in axes:
                    ax.set_axis_off()
            else:
                wordCloud.cloudShape(self)
                wordCloud.generateCloud(self)
                axes[1].imshow(self.cloud, interpolation="bilinear")
                for ax in axes:
                    ax.set_axis_off()
        plt.show()
        
    def saveWordcloud(self):
        self.outputImage = self.saveName.get()
        self.outputImage = "WordClouds\\{}.png".format(self.outputImage)
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