# Wordcloud

## Summary

WordCloud generation project using the WordCloud module created by [amueller](https://github.com/amueller/). Initially, this project started out as a few scripts exploring the capabilities of the WordCloud modules and eventually turned into a more indepth project than I orginially planned.

## Requirements

Install the required modules using the requirements.txt file.

`pip install -r requirements.txt`

## How to use

The program runs with a UI created in tkinter.
![UI layout](example.PNG)

On the top left you can select the text file (either a txt or PDF file).
**Note: PDFs are more challenging to extract text from and as a result will show as having a far higher word count**

On the left you can select the image. This can be used to recolour text using the image or create the wordcloud within the boundaries of the image (White or Transparent backgrounds). In addition, you can tick both options to recolour within a set area.

In the bottom left there are additional options to set the background of the WordCloud. **By defualt the background generated is transparent**

To generate a preview of the WordCloud, click on the preview button in the top centre of the layout. This will open the WordCloud in a new window. If you are happy with the WordCloud you can save the WordCloud with the save button. **If you do not wish to preview the WordCloud the save button will run a WordCloud generation if one has not been previously run**.

In the middle of the UI you have the option to set the text colours. Two drop downs determine the text colours. **If recolour using image is ticked then this setting is ignored**

You can control the canvas size in the bottom middle of the UI. Input the size you wish. **Note: If recolour image is ticked the canvas will set to the size of the image if it is smaller than the specified area - so if you have 1920 by 1280, but the image size is 900 by 900, the canvas will automatically resize to 900 by 900**

On the right hand side of the UI you have options to limit the length of words included. This can be set to make sure all words used are equal to or greater than the number set in the slider. Under this you have the maximum number of words you wish to include in the WordCloud.

In addition, under maximum number of words you can select whether you want to allow words to be repeated and whether you want to include numbers.

The final key setting is STOPWORDS. You can add additional STOPWORDs. For example, if you were using text from a novel you may wish to remove word "said". You can add a range of STOPWORDS as required and reset back to the default STOPWORDS at a click of a button.

Finally, we have a reset button, that resets everything back to default values, and the exit button to close the program.
