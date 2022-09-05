from time import asctime
from matplotlib import image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import os
import tkinter as tk
from tkinter import Button, Label, messagebox, filedialog, IntVar, Checkbutton, colorchooser, ttk
import logging
import PyPDF2


class wordCloud:
    def __init__(self):
        logging.info("Initialising WordCloud")
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
        self.colourSelected = "viridis"
        self.selectFile = r'Text\Corbyn Conference Speeches 2015-2019.txt'
        wordCloud.numberOfWords(self)
        wordCloud.userInterface(self)  
        
    def userInterface(self):
        self.root = tk.Tk()
        self.root.title("Word Cloud Generator")
        #self.root.configure(background="light green")
        self.root.geometry("800x600")
        title = tk.Label(text="Word Cloud Generator", font='sans 18 bold')
        button_selectText = tk.Button(
            self.root,
            text = "Select Text",
            width=11,
            height=2,
            background='light yellow',
            font='sans 12 bold',
            command = lambda : wordCloud.selectText(self)
        )
        head, tailText = os.path.split(self.selectFile)
        self.wordCount = tk.Label(text = "Selected text file is\n {}\n and contains {} words".format(tailText,  self.totalWordCount))
        button_selectImage = tk.Button(
            self.root,
            text = "Select Image",
            width=11,
            height=2,
            background='light yellow',
            font='sans 12 bold',
            command = lambda : wordCloud.selectImage(self)
        )
        logging.info("Default text file selected: {}".format(tailText))
        head, tailImage = os.path.split(self.Image)
        self.selectedImage = tk.Label(text = "Image selection is \n{}".format(tailImage))
        button_preview = tk.Button(
            self.root, 
            text = "Preview", 
            width=11,
            height=2,
            background='light green',
            font='sans 12 bold',
            command = lambda : wordCloud.previewCloud(self)
            )
        logging.info("Default image file selected: {}".format(tailImage))
        button_save = tk.Button(
            self.root,
            text = "Save",
            width=11,
            height=2,
            background='light green',
            font='sans 12 bold',
            command = lambda : wordCloud.saveWordcloud(self)
        )
        button_reset = tk.Button(
            self.root,
            text = "Reset Settings",
            width=11,
            height=2,
            background='orange',
            font='sans 12 bold',
            command = lambda : wordCloud.reset(self)
        )
        button_exit = tk.Button(
            self.root,
            text = "Exit",
            width=11,
            height=2,
            background='red',
            font='sans 12 bold',
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
        Types = ['Perceptually Uniform Sequential', 'Sequential', 'Sequential (2)', 'Diverging', 'Cyclic', 'Qualitative', 'Miscellaneous']
        self.colourSet1 = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        self.colourSet2 = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        self.colourSet3 = ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']
        self.colourSet4 = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        self.colourSet5 = ['twilight', 'twilight_shifted', 'hsv']
        self.colourSet6 = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']
        self.colourSet7 = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']
        self.colourType = ttk.Combobox(self.root, 
            value = Types, 
            state="readonly",
            width=30)
        self.colourType.current(0)
        self.colourRange = ttk.Combobox(self.root,
            value = self.colourSet1, 
            state="readonly",
            width=30)
        self.colourRange.current(0)
        self.colourType.bind('<<ComboboxSelected>>', lambda event: self.pickColour(self))
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
        name = tk.Label(text="Save as:", font='sans 10')
        self.saveName = tk.Entry(self.root, width=20, font='sans 10')
        self.saveName.insert(0, "Clear Skies")
        maxWords = tk.Label(text="Maxium Number of Words")
        self.numberOfWords = tk.Entry(self.root)
        self.numberOfWords.insert(0, 200)
        characterLength = tk.Label(text ="Minimum Word Character Length:")
        self.minWordLength = tk.Scale(from_=0, 
            to=15, 
            orient='horizontal',
            width=20,
            length=100)
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
        self.backgroundColourexample = Label(text = "          ", width=20)
        selectColour = Label(text="Select WordCloud Text Colours")
        
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        
        
        button_selectText.grid(column=0, row=1)
        self.wordCount.grid(column=0, row=2)
        button_selectImage.grid(column=0, row=3)
        self.selectedImage.grid(column=0, row=4)
        self.backgroundColourLabel.grid(column=0, row=10)
        self.backgroundColourexample.grid(column=0, row=11)
        button_selectBackgroundColour.grid(column=0, row=12)
        button_resetBackgroundColour.grid(column=0, row=13)
        
        title.grid(column=1, row=0, pady=8)
        button_preview.grid(column=1, row=1)
        name.grid(column=1, row=2, sticky="W", ipadx=20)
        self.saveName.grid(column=1, row=2, sticky="E", ipadx=15, padx = 15)
        button_save.grid(column=1, row=3)
        self.checkRecolour.grid(column=1, row= 5)
        self.checkShape.grid(column=1, row=6)
        self.colourType.grid(column=1, row =8)
        selectColour.grid(column=1, row=7)
        self.colourRange.grid(column=1, row=9)
        imageHeight.grid(column=1, row=10)
        self.heightInput.grid(column=1, row=11)
        imageWidth.grid(column=1,row=12)
        self.widthInput.grid(column=1, row=13)
        button_switchHeightWidth.grid(column=1, row=14)
        
        
        characterLength.grid(column=2, row=2)
        self.minWordLength.grid(column=2, row=3)
        maxWords.grid(column=2, row=4)
        self.numberOfWords.grid(column=2, row=5)
        self.includeNumbers.grid(column=2, row=6)
        self.checkRepeatWords.grid(column=2, row=7)
        stopWords.grid(column=2, row=9)
        self.addStopWords.grid(column=2, row=10)
        button_addStopWord.grid(column=2, row=11)
        self.addedStopWords.grid(column=2, row=12)
        button_resetStopWords.grid(column=2, row=13)
        button_exit.grid(column=2, row=14, sticky="SE", pady=8, padx =1)
        button_reset.grid(column=2, row=14, sticky="SW", pady=8)
        
        self.root.resizable(True, True)
        self.root.mainloop()
        
    def pickColour(event, self):
        colour = event.colourType.get()
        logging.info("Colour Type {} selected".format(colour))
        if colour == 'Perceptually Uniform Sequential':
            self.colourRange.config(values=self.colourSet1)
            self.colourRange.current(0)
        elif colour == 'Sequential':
            self.colourRange.config(values=self.colourSet2)
            self.colourRange.current(0)
        elif colour == 'Sequential (2)':
            self.colourRange.config(values=self.colourSet3)
            self.colourRange.current(0)
        elif colour == 'Diverging':
            self.colourRange.config(values=self.colourSet4)
            self.colourRange.current(0)
        elif colour == 'Cyclic':
            self.colourRange.config(values=self.colourSet5)
            self.colourRange.current(0)
        elif colour == 'Qualitative':
            self.colourRange.config(values=self.colourSet6)
            self.colourRange.current(0)
        elif colour == 'Miscellaneous':
            self.colourRange.config(values=self.colourSet7)
            self.colourRange.current(0)
    
    def selectImage(self):
        selectImage = filedialog.askopenfilename(
            initialdir = r"Pictures",
            title = "Select Image File",
            filetypes = (("Image files", "png"),)
        )
        self.Image =selectImage
        head, tail = os.path.split(self.Image)
        if self.Image == "":
            self.selectedImage.config(text = "No image selected")
            logging.info("No image Selected")
        else:
            self.selectedImage.config(text = "Image selection is \n{}".format(tail))
            logging.info("The selected image is {}".format(tail))
            return self.Image
        
    def selectText(self):
        self.selectFile = filedialog.askopenfilename(
            initialdir = r"/Text/",
            title = "Select Text File",
            filetypes = [("text files", "*.txt"), ("PDF files", '*.pdf')]
            )
        if self.selectFile.endswith('.txt'):
            self.textFile = open(os.path.join(self.directory, self.selectFile), encoding="utf-8").read()
        elif self.selectFile == "":
            self.wordCount.config(text="No text file selected")    
        else:
            wordCloud.pdfCoverter(self)
        head, tail = os.path.split(self.selectFile)
        if self.selectFile == "":
            logging.error("No text file selected")
        else:
            wordCloud.numberOfWords(self)
            self.wordCount.config(text="Selected text file is \n{}\nand contains {} words".format(tail,  self.totalWordCount))
            logging.info("Selected text file is {} and contains {} words".format(tail,  self.totalWordCount))
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
        wordCloud.checkboxAction(self)
        if numbersCheck == 1:
            self.number = True
        else:
            self.number = False
        logging.info("Include Numbers is set to {}".format(self.number))
        if repeatWordsCheck == 1:
            self.repeat = True
        else: 
            self.repeat = False
        logging.info("Include repeated words is set to {}".format(self.repeat))
        return self.numberTicked
        
    
    def cloudShape(self):
        if self.Image == "":
            logging.error('No .png file selected, Generating WordCloud Without Image Settings')
            messagebox.showerror("Image File Error", "No Image File Selected, Generating WordCloud Without Image Settings")
        else:
            self.processedImage = np.array(Image.open(os.path.join(self.Image)))
            self.processedImage = self.processedImage[::3, ::3]
            self.image_mask = self.processedImage.copy()
            self.image_mask[self.image_mask.sum(axis=2)==0] = 255
            edges = np.mean([gaussian_gradient_magnitude(self.processedImage[:, :, i]/255., 2) for i in range(3)], axis = 0)
            self.image_mask[edges > 0.8] = 255
            logging.info("Image mask has been generated from Image")
            return self.image_mask
    
    def cloudRecolour(self):
        if self.Image == "":
            logging.error('No .png file selected, Generating WordCloud Without Image Settings')
            messagebox.showerror("Image File Error", "No Image File Selected, Generating WordCloud Without Image Settings")
        else:
            self.newImage = np.array(Image.open(os.path.join(self.Image)))
            self.image_colours = ImageColorGenerator(self.newImage)
            self.textColourChange = True
            logging.info("Recolour using image has been selected")
            
    
    def recolourShape(self):
        if self.Image == "":
            logging.error('No .png file selected, Generating WordCloud Without Image Settings')
            messagebox.showerror("Image File Error", "No Image File Selected, Generating WordCloud Without Image Settings")
        else:
            self.processedImage = np.array(Image.open(os.path.join(self.Image)))
            self.processedImage = self.processedImage[::3, ::3]
            self.image_mask = self.processedImage.copy()
            self.image_mask[self.image_mask.sum(axis=2)==0] = 255
            edges = np.mean([gaussian_gradient_magnitude(self.processedImage[:, :, i]/255., 2) for i in range(3)], axis = 0)
            self.image_mask[edges > 0.8] = 255
            logging.info("Image mask has been generated from Image")
            self.image_colours = ImageColorGenerator(self.processedImage)
            self.textColourChange = True
            logging.info("Recolour using image has been selected")
    
    def maxWords(self):
        self.maxWords = self.numberOfWords.get()
        if self.maxWords.isdigit():
            self.maxWords = int(self.maxWords)
            return self.maxWords
        else:
            print (self.maxWords)
            messagebox.showerror("Max Word error", "Please input a number. The word cloud has been set to 200 as default")
            self.maxWords = 200
            logging.error("Max words needs to be a number. Using {} words as a default".format(self.maxWords))
            return self.maxWords
        
    def heightCheck(self):
        self.heightNumber = self.heightInput.get()        
        if self.heightNumber.isdigit():
            self.heightNumber = int(self.heightNumber)
            return self.heightNumber
        else:
            messagebox.showerror("Height setting", "Please input a number. The word cloud has been set to 1280 as default")
            self.heightNumber = 1280
            logging.error("Height setting needs to be a number. Using {} words as a default".format(self.heightNumber))
            return self.heightNumber
    
    def widthCheck(self):
        self.widthNumber = self.widthInput.get()
        if self.widthNumber.isdigit():
            self.widthNumber = int(self.widthNumber)
            return self.widthNumber
        else:
            messagebox.showerror("Width setting", "Please input a number. The word cloud has been set to 1920 as default")
            self.widthNumber = 1920
            logging.error("Width settings needs to be a number. Using {} words as a default".format(self.widthNumber))
            return self.widthNumber
        
    def switchHieghtWidth(self):
        wordCloud.heightCheck(self)
        wordCloud.widthCheck(self)
        self.widthInput.delete(0, 'end')
        self.heightInput.delete(0, 'end')
        self.widthInput.insert(0, self.heightNumber)
        self.heightInput.insert(0, self.widthNumber)
        logging.info("Switch Height and Width button pressed")
            
    def addingSTOPWORDS(self):
        addword = self.addStopWords.get()
        updatedStopWords = self.stopwords
        if addword is None:
            logging.info("No word provided")
        else:
            updatedStopWords.add(addword)
            logging.info("{} has been added to the list of stopwords".format(addword))
            self.stopwords = updatedStopWords
            self.addStopWords.delete(0,'end')
            wordCloud.addedStopWordsDisplay(self)
    
    def resetStopWords(self):
        self.stopwords = set(STOPWORDS)
        logging.info("Stopwords have been reset by the user")
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
        logging.info("{} has been selected as the WordCloud background colour".format(self.backgroundColour))
        self.backgroundColourLabel.config(text="Current Background Colour: ")
        self.backgroundColourexample.config(background=self.backgroundColour)
    
    def resetColourSelection(self):
        self.backgroundColour = None
        logging.info("Background colour has been reset to SystemButtonFace")
        self.backgroundColourLabel.config(text="Background Colour Selection")
        self.backgroundColourexample.config(background="SystemButtonFace")
        
    def addedStopWordsDisplay(self):
        list = set(self.stopwords)
        addedWords = [word for word in list if word not in STOPWORDS]
        addedWords = ", ".join([str(x) for x in addedWords])
        self.addedStopWords.config(text = "Words added: {}".format(addedWords))
        logging.info("Added stopwords displayed updated")
        
    def generateCloud(self):
        logging.info("Cloud Generation checking the Text File Selected")
        wordCloud.checkboxStatus(self)
        wordCloud.maxWords(self)
        wordCloud.heightCheck(self)
        wordCloud.widthCheck(self)
        self.colourSelected = self.colourRange.get()
        logging.info("Word Cloud colour selected - {}".format(self.colourSelected))
        word_length = self.minWordLength.get()
        if self.textFile == "":
            logging.error('No text file selected')
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
                repeat=self.repeat,
                colormap=self.colourSelected,
            )
            self.cloud.generate(self.textFile)
            #self.height = "1280"
            #self.width = "1920"
            logging.info("Generated Word Cloud")
            if self.textColourChange == True:
                logging.info("recolouring wordcloud based on image")
                self.cloud.recolor(color_func=self.image_colours)
                return self.cloud
            else:
                return self.cloud
    
    def checkboxAction(self):
        if self.numberTicked == 0:
            logging.info("Image settings are not ticked")
            self.image_mask = None
        elif self.numberTicked == 1:
            if self.recolouredCheck == 1:
                logging.info("Recolour Word Cloud using Image is ticked")
                self.image_mask = None
                wordCloud.cloudRecolour(self)
            else:
                logging.info("Reshape Word Cloud using Image is ticked")
                wordCloud.cloudShape(self)
        elif self.numberTicked == 2:
            logging.info("Both recolour and reshape word cloud are ticked")
            wordCloud.recolourShape(self)
        
    def previewCloud(self):   
        logging.info("Preview Cloud Selected")
        self.textColourChange = False
        wordCloud.generateCloud(self)
        fig, axes = plt.subplots(1,1)
        axes.imshow(self.cloud, interpolation="bilinear")
        axes.set_axis_off()
        plt.show()
        
    def saveWordcloud(self):
        self.outputImage = self.saveName.get()
        logging.info("Saving Word Cloud as {}".format(self.outputImage))
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
        self.textColourChange = False
    
    def reset(self):
        logging.info("Reset all settings has been pressed")
        self.minWordLength.set(3)
        self.widthInput.delete(0, 'end')
        self.heightInput.delete(0, 'end')
        self.heightInput.insert(0, 1280)
        self.widthInput.insert(0, 1920)
        self.stopwords = set(STOPWORDS)
        self.image_mask = None
        self.cloud = None
        self.backgroundColour = None
        self.backgroundColourLabel.config(text="Background Colour Selection")
        self.backgroundColourexample.config(background="SystemButtonFace")
        self.addedStopWords.config(text = "No words added")
        self.numberOfWords.delete(0, 'end')
        self.numberOfWords.insert(0, 200)
        self.textFile = open(os.path.join(self.directory, r'Text\Corbyn Conference Speeches 2015-2019.txt'), encoding="utf-8").read()
        self.Image = 'Pictures\\Cat_Silhouette_PNG_Transparent_Clip_Art_Image.png'
        self.selectFile = r'Text\Corbyn Conference Speeches 2015-2019.txt'
        wordCloud.numberOfWords(self)
        head, tail = os.path.split(self.Image)
        self.selectedImage.config(text = "Image selection is \n{}".format(tail))
        head, tail = os.path.split(self.selectFile)
        self.wordCount.config(text="Selected text file is \n{} \nand contains {} words".format(tail,  self.totalWordCount))
        self.checkRecolour.deselect()
        self.checkShape.deselect()
        self.includeNumbers.deselect()
        self.checkRepeatWords.deselect()
        self.textColourChange = False
        self.colourType.current(0)
        self.colourRange.config(value = self.colourSet1)
        self.colourRange.current(0)
        logging.info("All settings reset back to default values")
        
    
    def exit(self):
        logging.info("Exiting program")
        self.root.destroy()

logging.basicConfig(filename='Word Cloud.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

wordCloud()

#wordCloud.generateCloud(wordCloud.textFile)