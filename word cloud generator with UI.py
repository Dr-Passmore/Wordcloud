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
import PyPDF2


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
        self.textColourChange = False
        self.selectFile = r'Text\Corbyn Conference Speeches 2015-2019.txt'
        wordCloud.numberOfWords(self)
        wordCloud.userInterface(self)  
        
    def userInterface(self):
        self.root = tk.Tk()
        self.root.title("Word Cloud Generator")
        #self.root.configure(background="light green")
        self.root.geometry("1000x800")
        title = tk.Label(text="Word Cloud Generator")
        button_selectText = tk.Button(
            self.root,
            text = "Select Text",
            command = lambda : wordCloud.selectText(self)
        )
        head, tailText = os.path.split(self.selectFile)
        self.wordCount = tk.Label(text = "Selected text file is {} and contains {} words".format(tailText,  self.totalWordCount))
        button_selectImage = tk.Button(
            self.root,
            text = "Select Image",
            command = lambda : wordCloud.selectImage(self)
        )
        head, tailImage = os.path.split(self.Image)
        self.selectedImage = tk.Label(text = "Image selection is {}".format(tailImage))
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
        button_reset = tk.Button(
            self.root,
            text = "Reset Settings",
            command = lambda : wordCloud.reset(self)
        )
        button_exit = tk.Button(
            self.root,
            text = "Exit",
            command = lambda : wordCloud.exit(self)
        )
        button_addStopWord = tk.Button(
            self.root,
            text = 'Add STOPWORD',
            command = lambda : wordCloud.addingSTOPWORDS(self)
        )
        button_resetStopWords = tk.Button(
            self.root,
            text = "Reset STOPWORDs",
            command = lambda : wordCloud.resetStopWords(self) 
        )
        button_selectBackgroundColour = tk.Button(
            self.root,
            text = "Select Colour",
            command = lambda: wordCloud.colourSelection(self)
        )
        button_resetBackgroundColour = tk.Button(
            self.root,
            text = "Remove Background Colour",
            command = lambda: wordCloud.resetColourSelection(self)
        )
        button_switchHeightWidth = tk.Button(
            self.root,
            text = "Switch Height and Width",
            command = lambda: wordCloud.switchHieghtWidth(self)
        )
        self.recolour = IntVar()
        self.checkRecolour = Checkbutton(
            self.root,
            text = "Recolour Text Using Image", 
            variable = self.recolour, 
            onvalue = 1, 
            offvalue = 0, 
            height=1, 
            width = 30)
        self.shapeCloud = IntVar()
        self.checkShape = Checkbutton(
            self.root,
            text = "Use Image Boundary Map",
            variable= self.shapeCloud,
            onvalue = 1, 
            offvalue = 0,
            height = 1,
            width = 30)
        self.numbersIncluded = IntVar()
        self.includeNumbers = Checkbutton(
            self.root,
            text = "Include Numbers From Text File",
            variable = self.numbersIncluded,
            onvalue = 1,
            offvalue = 0,
            height = 1,
            width = 30)
        self.repeatWords = IntVar()
        self.checkRepeatWords = Checkbutton(
            self.root,
            text = "Allow repeating of Words",
            variable= self.repeatWords,
            onvalue= 1,
            offvalue= 0,
            height = 1,
            width= 30)
        name = tk.Label(text="Save Image As ")
        self.saveName = tk.Entry(self.root)
        self.saveName.insert(0, "Clear Skies")
        maxWords = tk.Label(text="Maxium Number of Words")
        self.numberOfWords = tk.Entry(self.root)
        self.numberOfWords.insert(0, 200)
        characterLength = tk.Label(text ="Word Character length Selector")
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
        self.addedStopWords = tk.Label(text = "No words added")
        self.backgroundColourLabel = tk.Label(text="Background Colour Selection")
        
        title.pack()
        #selectFile.pack() 
        button_selectText.pack()
        self.wordCount.pack()
        button_selectImage.pack()
        self.selectedImage.pack()
        button_preview.pack()
        self.checkRecolour.pack()
        self.checkShape.pack()
        self.includeNumbers.pack()
        self.checkRepeatWords.pack()
        characterLength.pack()
        self.minWordLength.pack()
        maxWords.pack()
        self.numberOfWords.pack()
        imageHeight.pack()
        self.heightInput.pack()
        imageWidth.pack()
        self.widthInput.pack()
        button_switchHeightWidth.pack()
        stopWords.pack()
        self.addStopWords.pack()
        button_addStopWord.pack()
        self.addedStopWords.pack()
        button_resetStopWords.pack()
        self.backgroundColourLabel.pack()
        button_selectBackgroundColour.pack()
        button_resetBackgroundColour.pack()
        name.pack()
        self.saveName.pack()
        button_save.pack()
        button_reset.pack()
        button_exit.pack()
        self.root.mainloop()
    
    def selectImage(self):
        selectImage = filedialog.askopenfilename(
            initialdir = r"Pictures",
            title = "Select Image File",
            filetypes = (("Image files", "png"),)
        )
        self.Image =selectImage
        head, tail = os.path.split(self.Image)
        self.selectedImage.config(text = "Image selection is {}".format(tail))
        return self.Image
    
    def selectText(self):
        self.selectFile = filedialog.askopenfilename(
            initialdir = r"/Text/",
            title = "Select Text File",
            filetypes = [("text files", "*.txt"), ("PDF files", '*.pdf')]
            )
        logging.info("The text file {} has been selected".format(self.selectFile))
        if self.selectFile.endswith('.txt'):
            self.textFile = open(os.path.join(self.directory, self.selectFile), encoding="utf-8").read()
        else:
            wordCloud.pdfCoverter(self)
        wordCloud.numberOfWords(self)
        head, tail = os.path.split(self.selectFile)
        self.wordCount.config(text="Selected text file is {} and contains {} words".format(tail,  self.totalWordCount))
        return self.textFile
    
    def pdfCoverter(self):
        logging.info('pdfConverter activated')
        pdfFile = open(self.selectFile,  'rb')
        pdfRead = PyPDF2.PdfFileReader(pdfFile)
        pdfPageNum = pdfRead.numPages
        self.textFile = ""
        for page in range(pdfPageNum):
            pg = pdfRead.getPage(page)
            self.textFile += pg.extract_text()
        logging.info('PDF text extracted')
        return self.textFile
    
    def checkboxStatus(self):
        logging.info('Checking whether tick boxes are selected')
        self.shapecloudCheck = self.shapeCloud.get()
        self.recolouredCheck = self.recolour.get()
        numbersCheck = self.numbersIncluded.get()
        repeatWordsCheck = self.repeatWords.get()
        self.numberTicked = self.shapecloudCheck + self.recolouredCheck
        if numbersCheck == 1:
            self.number = True
        else:
            self.number = False
        if repeatWordsCheck == 1:
            self.repeat = True
        else: 
            self.repeat = False
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
            self.textColourChange = True
            #self.cloud.recolor(color_func=self.image_colours)
    
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
            #wordCloud.generateCloud(self)
            self.image_colours = ImageColorGenerator(self.processedImage)
            #self.cloud.recolor(color_func=self.image_colours)
            self.textColourChange = True
    
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
        
    def switchHieghtWidth(self):
        wordCloud.heightCheck(self)
        wordCloud.widthCheck(self)
        self.widthInput.delete(0, 'end')
        self.heightInput.delete(0, 'end')
        self.widthInput.insert(0, self.heightNumber)
        self.heightInput.insert(0, self.widthNumber)
            
    def addingSTOPWORDS(self):
        addword = self.addStopWords.get()
        updatedStopWords = self.stopwords
        if addword is None:
            logging.info("No word provided")
        else:
            updatedStopWords.add(addword)
            self.stopwords = updatedStopWords
            self.addStopWords.delete(0,'end')
            wordCloud.addedStopWordsDisplay(self)
    
    def resetStopWords(self):
        self.stopwords = set(STOPWORDS)
        wordCloud.addedStopWordsDisplay(self)
            
    def numberOfWords(self):
        if self.selectFile.endswith('.txt'):
            text = open(self.selectFile, encoding="utf-8")
        else:
            text = open(self.selectFile, encoding="ISO8859-1")
        data = text.read() 
        words = data.split()
        logging.info("Text file selected contains {} words".format(len(words)))
        self.totalWordCount = len(words)
        
    def colourSelection(self):
        myColourSelector = colorchooser.askcolor()
        self.backgroundColour = myColourSelector[1]
        self.backgroundColourLabel.config(background=self.backgroundColour, text="Current Background Colour")
    
    def resetColourSelection(self):
        self.backgroundColour = None
        self.backgroundColourLabel.config(background="SystemButtonFace", text="Background Colour Selection")
        
    def addedStopWordsDisplay(self):
        list = set(self.stopwords)
        addedWords = [word for word in list if word not in STOPWORDS]
        addedWords = ", ".join([str(x) for x in addedWords])
        self.addedStopWords.config(text = "Words added: {}".format(addedWords))
        
    def generateCloud(self):
        logging.info("Cloud Generation checking the Text File Selected")
        wordCloud.checkboxAction(self)
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
                max_words= self.maxWords,
                include_numbers=self.number,
                repeat=self.repeat
            )
            self.cloud.generate(self.textFile)
            self.height = "1280"
            self.width = "1920"
            if self.textColourChange == True:
                self.cloud.recolor(color_func=self.image_colours)
                return self.cloud
            else:
                return self.cloud
    
    def checkboxAction(self):
        wordCloud.checkboxStatus(self)
        if self.numberTicked == 0:
            self.image_mask = None
        elif self.numberTicked == 1:
            if self.recolouredCheck == 1:
                self.image_mask = None
                wordCloud.cloudRecolour(self)
            else:
                wordCloud.cloudShape(self)
        elif self.numberTicked == 2:
            wordCloud.recolourShape(self)
        
    def previewCloud(self):   
        logging.info("Preview Cloud Selected")
        self.textColourChange = False
        wordCloud.checkboxAction(self)
        wordCloud.generateCloud(self)
        fig, axes = plt.subplots(1,1)
        axes.imshow(self.cloud, interpolation="bilinear")
        axes.set_axis_off()
        plt.show()
        
    def saveWordcloud(self):
        self.outputImage = self.saveName.get()
        self.outputImage = "WordClouds\\{}.png".format(self.outputImage)
        #Checks to make sure cloud has been generated
        if self.cloud is None:
            #if cloud has been created without using preview it will generate a word cloud
            wordCloud.checkboxAction(self)
            wordCloud.generateCloud(self)
        else:
            logging.info("Cloud already generated")
        self.cloud.to_file(self.outputImage)
        #Resets the Cloud once saved
        self.cloud = None
        self.textColourChange = False
    
    def reset(self):
        self.minWordLength.set(3)
        self.widthInput.delete(0, 'end')
        self.heightInput.delete(0, 'end')
        self.heightInput.insert(0, 1280)
        self.widthInput.insert(0, 1920)
        self.stopwords = set(STOPWORDS)
        self.image_mask = None
        self.cloud = None
        self.backgroundColour = None
        self.backgroundColourLabel.config(background="SystemButtonFace", text="Background Colour Selection")
        self.addedStopWords.config(text = "No words added")
        self.numberOfWords.delete(0, 'end')
        self.numberOfWords.insert(0, 200)
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        self.Image = 'Pictures\\Cat_Silhouette_PNG_Transparent_Clip_Art_Image.png'
        self.selectFile = r'Text\Corbyn Conference Speeches 2015-2019.txt'
        wordCloud.numberOfWords(self)
        head, tail = os.path.split(self.Image)
        self.selectedImage.config(text = "Image selection is {}".format(tail))
        head, tail = os.path.split(self.selectFile)
        self.wordCount.config(text="Selected text file is {} and contains {} words".format(tail,  self.totalWordCount))
        self.checkRecolour.deselect()
        self.checkShape.deselect()
        self.includeNumbers.deselect()
        self.checkRepeatWords.deselect()
        self.textColourChange = False
    
    def exit(self):
        self.root.destroy()

#logging.basicConfig(filename='Word Cloud.log', filemode='w', level=logging.DEBUG)

wordCloud()

#wordCloud.generateCloud(wordCloud.textFile)