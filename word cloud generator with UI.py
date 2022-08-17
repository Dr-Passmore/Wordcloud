from matplotlib import image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk
from tkinter import Button, Label, messagebox, filedialog, IntVar, Checkbutton, colorchooser
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
        self.Image = 'Pictures\\Cat_Silhouette_PNG_Transparent_Clip_Art_Image.png'
        self.stopwords = set(STOPWORDS)
        self.image_mask = None
        self.cloud = None
        self.backgroundColour = None
        self.selectFile = r'Text\Corbyn Conference Speeches 2015-2019.txt'
        wordCloud.numberOfWords(self)
        wordCloud.userInterface(self)  
        
    def userInterface(self):
        self.root = tk.Tk()
        self.root.title("Word Cloud Generator")
        #root.configure(background="light green")
        self.root.geometry("1000x800")
        title = tk.Label(text="Word Cloud Generator")
        button_selectText = tk.Button(
            self.root,
            text = "Select Text",
            command = lambda : wordCloud.selectText(self)
        )
        self.wordCount = tk.Label(text = "Selected text file {} contains {} words".format(self.selectFile,  self.totalWordCount))
        button_selectImage = tk.Button(
            self.root,
            text = "Select Image",
            command = lambda : wordCloud.selectImage(self)
        )
        self.selectedImage = tk.Label(text = "Image selection is {}".format(self.Image))
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
        button_addStopWord = tk.Button(
            self.root,
            text = 'Add STOPWORD',
            command= lambda : wordCloud.addingSTOPWORDS(self)
        )
        button_selectBackgroundColour = tk.Button(
            self.root,
            text = "Select Colour",
            command = lambda: wordCloud.colourSelection(self)
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
        maxWords = tk.Label(text="Maxium Number of Words")
        self.numberOfWords = tk.Entry(self.root)
        self.numberOfWords.insert(0, 200)
        self.minWordLength = tk.Scale(from_=0, to=15, orient='horizontal')
        self.minWordLength.set(3)
        imageHeight = tk.Label(text="Select image Height")
        self.heightInput = tk.Entry(self.root)
        self.heightInput.insert(0, 1280)
        imageWidth = tk.Label(text="Select image width")
        self.widthInput = tk.Entry(self.root)
        self.widthInput.insert(0, 1920)
        stopWords = tk.Label(text="Add words to ignore")
        self.addStopWords = tk.Entry(self.root)
        self.backgroundColourLabel = tk.Label(text="Background Colour Selection")
        
        title.pack()
        #selectFile.pack() 
        button_selectText.pack()
        self.wordCount.pack()
        button_selectImage.pack()
        self.selectedImage.pack()
        button_preview.pack()
        checkRecolour.pack()
        checkShape.pack()
        maxWords.pack()
        self.minWordLength.pack()
        self.numberOfWords.pack()
        imageHeight.pack()
        self.heightInput.pack()
        imageWidth.pack()
        self.widthInput.pack()
        stopWords.pack()
        self.addStopWords.pack()
        button_addStopWord.pack()
        self.backgroundColourLabel.pack()
        button_selectBackgroundColour.pack()
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
        self.Image =selectImage
        self.selectedImage.config(text = "Image selection is {}".format(self.Image))
        return self.Image
    
    def selectText(self):
        self.selectFile = filedialog.askopenfilename(
            initialdir = r"/Text/",
            title = "Select Text File",
            filetypes = (("text files", "txt"),)
            )
        logging.info("The text file {} has been selected".format(self.selectFile))
        self.textFile = open(os.path.join(self.directory, self.selectFile), encoding="utf-8").read()
        wordCloud.numberOfWords(self)
        self.wordCount.config(text="Selected text file {} contains {} words".format(self.selectFile,  self.totalWordCount))
        return self.textFile
    
    def checkboxStatus(self):
        logging.info('Checking whether tick boxes are selected')
        self.shapecloudCheck = self.shapeCloud.get()
        self.recolouredCheck = self.recolour.get()
        self.numberTicked = self.shapecloudCheck + self.recolouredCheck
        return self.numberTicked
    
    def cloudShape(self):
        if self.Image is None:
            logging.warn('No .png file selected')
            messagebox.showerror("Image File Error", "No Image File Selected")
        else:
            self.processedImage = np.array(Image.open(os.path.join(self.Image)))
            self.processedImage = self.processedImage[::3, ::3]
            self.image_mask = self.processedImage.copy()
            self.image_mask[self.image_mask.sum(axis=2)==0] = 255
            edges = np.mean([gaussian_gradient_magnitude(self.processedImage[:, :, i]/255., 2) for i in range(3)], axis = 0)
            self.image_mask[edges > 0.8] = 255
            return self.image_mask
    
    def cloudRecolour(self):
        if self.Image is None:
            logging.warn('No .png file selected')
            messagebox.showerror("Image File Error", "No Image File Selected")
        else:
            self.newImage = np.array(Image.open(os.path.join(self.Image)))
            self.image_colours = ImageColorGenerator(self.newImage)
            self.cloud.recolor(color_func=self.image_colours)
            return self.cloud
    
    def recolourShape(self):
        if self.Image is None:
            logging.warn('No .png file selected')
            messagebox.showerror("Image File Error", "No Image File Selected")
        else:
            self.processedImage = np.array(Image.open(os.path.join(self.Image)))
            self.processedImage = self.processedImage[::3, ::3]
            self.image_mask = self.processedImage.copy()
            self.image_mask[self.image_mask.sum(axis=2)==0] = 255
            edges = np.mean([gaussian_gradient_magnitude(self.processedImage[:, :, i]/255., 2) for i in range(3)], axis = 0)
            self.image_mask[edges > 0.8] = 255
            wordCloud.generateCloud(self)
            self.image_colours = ImageColorGenerator(self.processedImage)
            self.cloud.recolor(color_func=self.image_colours)
            return self.cloud
    
    def maxWords(self):
        self.maxWords = self.numberOfWords.get()
        if self.maxWords.isdigit():
            self.maxWords = int(self.maxWords)
            return self.maxWords
        else:
            print (self.maxWords)
            messagebox.showerror("Max Word error", "Please input a number. The word cloud has been set to 200 as default")
            self.maxWords = 200
            return self.maxWords
        
    def heightCheck(self):
        self.heightNumber = self.heightInput.get()        
        if self.heightNumber.isdigit():
            self.heightNumber = int(self.heightNumber)
            return self.heightNumber
        else:
            messagebox.showerror("Height setting", "Please input a number. The word cloud has been set to 1280 as default")
            self.heightNumber = 1280
            return self.heightNumber
    
    def widthCheck(self):
        self.widthNumber = self.widthInput.get()
        if self.widthNumber.isdigit():
            self.widthNumber = int(self.widthNumber)
            return self.widthNumber
        else:
            messagebox.showerror("Width setting", "Please input a number. The word cloud has been set to 1920 as default")
            self.widthNumber = 1920
            return self.widthNumber
            
    def addingSTOPWORDS(self):
        addword = self.addStopWords.get()
        updatedStopWords = self.stopwords
        if addword is None:
            logging.info("No word provided")
        else:
            updatedStopWords.add(addword)
            self.stopwords = updatedStopWords
            self.addStopWords.delete(0,'end')
            
    def numberOfWords(self):
        text = open(self.selectFile, encoding="utf-8")
        data = text.read()
        words = data.split()
        logging.info("Text file selected contains {} words".format(len(words)))
        self.totalWordCount = len(words)
        
    def colourSelection(self):
        myColourSelector = colorchooser.askcolor()
        self.backgroundColour = myColourSelector[1]
        self.backgroundColourLabel.config(background=self.backgroundColour, text="Current Background Colour")
        
    def generateCloud(self):
        logging.info("Cloud Generation checking the Text File Selected")
        wordCloud.checkboxStatus(self)
        wordCloud.maxWords(self)
        wordCloud.heightCheck(self)
        wordCloud.widthCheck(self)
        word_length = self.minWordLength.get()
        if self.textFile is None:
            logging.warn('No .txt file selected')
            messagebox.showerror("Text File Error", "No Text File Selected")
        else:
            logging.info("Text file found")
            self.cloud = WordCloud(
                mode = "RGBA",
                background_color=self.backgroundColour,
                stopwords=self.stopwords,
                height = self.heightNumber,
                width = self.widthNumber,
                mask = self.image_mask,
                min_word_length= word_length,
                max_words= self.maxWords
            )
            self.cloud.generate(self.textFile)
            self.height = "1280"
            self.width = "1920"
            return self.cloud
        
    def previewCloud(self):   
        logging.info("Preview Cloud Selected")
        wordCloud.checkboxStatus(self)
        
        if self.numberTicked == 0:
            self.image_mask = None
            wordCloud.generateCloud(self)
            fig, axes = plt.subplots(1,1)
            axes.imshow(self.cloud, interpolation="bilinear")
            axes.set_axis_off()
        elif self.numberTicked == 1:
            
            if self.recolouredCheck == 1:
                self.image_mask = None
                wordCloud.generateCloud(self)
                fig, axes = plt.subplots(1, 2)
                axes[0].imshow(self.cloud, interpolation="bilinear")
                axes[0].set_title('Default Colours')
                wordCloud.cloudRecolour(self)
                axes[1].imshow(self.cloud, interpolation="bilinear")
                axes[1].set_title('Recoloured Using Image')
                for ax in axes:
                    ax.set_axis_off()
            else:
                fig, axes = plt.subplots(1, 1)
                wordCloud.cloudShape(self)
                wordCloud.generateCloud(self)
                axes.imshow(self.cloud, interpolation="bilinear")
                axes.set_axis_off()
        elif self.numberTicked == 2:
            
            wordCloud.recolourShape(self)
            fig, axes = plt.subplots(1, 1)
            axes.imshow(self.cloud, interpolation="bilinear")
            axes.set_axis_off()
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